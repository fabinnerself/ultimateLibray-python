from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
import math

from ..models.user import (
    User, UserCreate, UserUpdate, UserPasswordUpdate, UserInDB, 
    UserResponse, Token, UserLogin
)
from ..database import get_user_collection
from ..auth.auth_utils import (
    get_password_hash, verify_password, create_access_token,
    authenticate_user, get_current_active_user, get_current_admin_user
)
from ..config import settings

router = APIRouter()

@router.post("/auth/register", response_model=dict)
async def register_user(user: UserCreate):
    """
    Register a new user
    """
    try:
        user_collection = await get_user_collection()
        
        # Check if user already exists
        existing_user = await user_collection.find_one({
            "email": user.email, 
            "is_deleted": False
        })
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Create user document
        user_dict = user.dict()
        del user_dict["password"]  # Remove plain password
        user_dict.update({
            "hashed_password": hashed_password,
            "is_active": True,
            "is_verified": False,
            "last_login": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": None,
            "is_deleted": False
        })
        
        # Insert user
        result = await user_collection.insert_one(user_dict)
        
        # Get created user (without password)
        created_user = await user_collection.find_one(
            {"_id": result.inserted_id},
            {"hashed_password": 0}
        )
        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]
        
        return {
            "msg": "User registered successfully",
            "data": created_user
        }
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.post("/auth/login", response_model=dict)
async def login_user(user_credentials: UserLogin):
    """
    Authenticate user and return JWT token
    """
    try:
        # Authenticate user
        user = await authenticate_user(user_credentials.email, user_credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is deactivated"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        # Update last login
        user_collection = await get_user_collection()
        await user_collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return {
            "msg": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "lastname": user.lastname,
                    "email": user.email,
                    "role": user.role
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.get("/users/me", response_model=dict)
async def get_current_user_profile(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get current user profile
    """
    user_data = {
        "id": str(current_user.id),
        "name": current_user.name,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "phone": current_user.phone,
        "birthday": current_user.birthday,
        "avatar": current_user.avatar,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "last_login": current_user.last_login,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }
    
    return {
        "msg": "Ok",
        "data": user_data
    }

@router.put("/users/me", response_model=dict)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Update current user profile
    """
    try:
        user_collection = await get_user_collection()
        
        # Build update data (only include fields that are not None)
        update_data = {}
        for field, value in user_update.dict(exclude_unset=True).items():
            if value is not None:
                # Check if email is being changed and if it's already taken
                if field == "email" and value != current_user.email:
                    existing_user = await user_collection.find_one({
                        "email": value,
                        "is_deleted": False,
                        "_id": {"$ne": ObjectId(current_user.id)}
                    })
                    if existing_user:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already in use"
                        )
                update_data[field] = value
        
        if not update_data:
            return {"msg": "No fields to update"}, 400
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Update user
        result = await user_collection.find_one_and_update(
            {"_id": ObjectId(current_user.id)},
            {"$set": update_data},
            return_document=True,
            projection={"hashed_password": 0}
        )
        
        result["id"] = str(result["_id"])
        del result["_id"]
        
        return {
            "msg": "Profile updated successfully",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.put("/users/me/password", response_model=dict)
async def change_password(
    password_update: UserPasswordUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Change user password
    """
    try:
        # Verify current password
        if not verify_password(password_update.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(password_update.new_password)
        
        # Update password
        user_collection = await get_user_collection()
        await user_collection.update_one(
            {"_id": ObjectId(current_user.id)},
            {
                "$set": {
                    "hashed_password": new_hashed_password,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {"msg": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.get("/users", response_model=dict)
async def get_users(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    order_by: str = Query("created_at", regex="^(name|lastname|email|created_at|updated_at)$"),
    sort_by: str = Query("desc", regex="^(asc|desc)$"),
    keyword: Optional[str] = Query(None, min_length=1),
    role: Optional[str] = Query(None, regex="^(admin|user|moderator)$"),
    is_active: Optional[bool] = Query(None),
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Get users with pagination and filters - Admin only
    """
    try:
        user_collection = await get_user_collection()
        
        # Calculate skip for pagination
        skip = (page - 1) * limit
        
        # Build query (exclude deleted users)
        query = {"is_deleted": False}
        
        if keyword:
            query["$or"] = [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"lastname": {"$regex": keyword, "$options": "i"}},
                {"email": {"$regex": keyword, "$options": "i"}}
            ]
        
        if role:
            query["role"] = role
            
        if is_active is not None:
            query["is_active"] = is_active
        
        # Set sort order
        sort_order = ASCENDING if sort_by == "asc" else DESCENDING
        
        # Execute query with pagination
        cursor = user_collection.find(
            query, 
            {"hashed_password": 0}  # Exclude password
        ).skip(skip).limit(limit).sort(order_by, sort_order)
        
        users = await cursor.to_list(length=limit)
        
        # Count total documents
        total_items = await user_collection.count_documents(query)
        
        # Convert ObjectId to string for JSON serialization
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
        
        # Build response
        response = {
            "msg": "Ok",
            "data": users,
            "totalItems": total_items,
            "totalPages": math.ceil(total_items / limit),
            "limit": limit,
            "currentPage": page
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.get("/users/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Get a user by ID - Admin only
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            return {"msg": "Invalid user ID"}, 400
            
        user_collection = await get_user_collection()
        user = await user_collection.find_one(
            {"_id": ObjectId(user_id), "is_deleted": False},
            {"hashed_password": 0}
        )
        
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            return {
                "msg": "Ok",
                "data": user
            }
        
        return {"msg": "User not found"}, 404
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Update a user by ID - Admin only
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            return {"msg": "Invalid user ID"}, 400
            
        user_collection = await get_user_collection()
        
        # Build update data
        update_data = {}
        for field, value in user_update.dict(exclude_unset=True).items():
            if value is not None:
                # Check if email is being changed and if it's already taken
                if field == "email":
                    existing_user = await user_collection.find_one({
                        "email": value,
                        "is_deleted": False,
                        "_id": {"$ne": ObjectId(user_id)}
                    })
                    if existing_user:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already in use"
                        )
                update_data[field] = value
        
        if not update_data:
            return {"msg": "No fields to update"}, 400
            
        update_data["updated_at"] = datetime.utcnow()
        
        # Update user
        result = await user_collection.find_one_and_update(
            {"_id": ObjectId(user_id), "is_deleted": False},
            {"$set": update_data},
            return_document=True,
            projection={"hashed_password": 0}
        )
        
        if not result:
            return {"msg": "User not found"}, 404
        
        result["id"] = str(result["_id"])
        del result["_id"]
        
        return {
            "msg": "User updated successfully",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Soft delete a user by ID - Admin only
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            return {"msg": "Invalid user ID"}, 400
            
        # Prevent admin from deleting themselves
        if str(current_user.id) == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
            
        user_collection = await get_user_collection()
        
        # Soft delete user
        result = await user_collection.update_one(
            {"_id": ObjectId(user_id), "is_deleted": False},
            {
                "$set": {
                    "is_deleted": True,
                    "deleted_at": datetime.utcnow(),
                    "is_active": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            return {"msg": "User not found"}, 404
        
        return {"msg": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as error:
        return {"msg": str(error)}, 500
