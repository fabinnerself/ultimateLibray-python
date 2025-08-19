from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
import math

from ..models.book import Book, BookCreate, BookUpdate
from ..models.user import UserInDB
from ..database import get_book_collection
from ..auth.auth_utils import get_current_active_user

router = APIRouter()

@router.get("/books", response_model=dict)
async def get_books(
    limit: int = Query(5, ge=1, le=100),
    page: int = Query(1, ge=1),
    order_by: str = Query("name", regex="^(name|author|price|created_at|updated_at)$"),
    sort_by: str = Query("asc", regex="^(asc|desc)$"),
    keyword: Optional[str] = Query(None, min_length=1)
):
    """
    Get books with pagination and search - maintains the same structure as Node.js API
    """
    try:
        book_collection = await get_book_collection()
        
        # Calculate skip for pagination
        skip = (page - 1) * limit
        
        # Build query
        query = {}
        if keyword:
            query["name"] = {"$regex": keyword, "$options": "i"}
        
        # Set sort order
        sort_order = ASCENDING if sort_by == "asc" else DESCENDING
        
        # Execute query with pagination
        cursor = book_collection.find(query).skip(skip).limit(limit).sort(order_by, sort_order)
        books = await cursor.to_list(length=limit)
        
        # Count total documents
        total_items = await book_collection.count_documents(query)
        
        # Convert ObjectId to string for JSON serialization
        for book in books:
            book["id"] = str(book["_id"])
            del book["_id"]
        
        # Build response - same structure as Node.js
        response = {
            "msg": "Ok",
            "data": books,
            "totalItems": total_items,
            "totalPages": math.ceil(total_items / limit),
            "limit": limit,
            "currentPage": page
        }
        
        return response
        
    except Exception as error:
        return {"msg": str(error)}, 500

@router.get("/books/{book_id}", response_model=dict)
async def get_book(book_id: str):
    """
    Get a single book by ID - maintains the same structure as Node.js API
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(book_id):
            return {"msg": "Invalid book ID"}, 400
            
        book_collection = await get_book_collection()
        book = await book_collection.find_one({"_id": ObjectId(book_id)})
        
        if book:
            book["id"] = str(book["_id"])
            del book["_id"]
            return {
                "msg": "Ok",
                "data": book
            }
        
        return {"msg": "Not Found"}, 404
        
    except Exception as error:
        return {"msg": str(error)}, 500

@router.post("/books", response_model=dict)
async def create_book(
    book: BookCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Create a new book - requires authentication
    """
    try:
        book_collection = await get_book_collection()
        
        # Convert to dict and add timestamps
        book_dict = book.dict()
        book_dict["created_at"] = datetime.utcnow()
        book_dict["updated_at"] = datetime.utcnow()
        
        # Insert book
        result = await book_collection.insert_one(book_dict)
        
        # Get the created book
        created_book = await book_collection.find_one({"_id": result.inserted_id})
        created_book["id"] = str(created_book["_id"])
        del created_book["_id"]
        
        return {
            "msg": "Ok",
            "data": created_book
        }
        
    except Exception as error:
        return {"msg": str(error)}, 500

@router.put("/books/{book_id}", response_model=dict)
async def update_book(
    book_id: str,
    book_update: BookUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Update a book by ID - requires authentication
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(book_id):
            return {"msg": "Invalid book ID"}, 400
            
        book_collection = await get_book_collection()
        
        # Build update data (only include fields that are not None)
        update_data = {}
        for field, value in book_update.dict(exclude_unset=True).items():
            if value is not None:
                update_data[field] = value
        
        if not update_data:
            return {"msg": "No fields to update"}, 400
            
        update_data["updated_at"] = datetime.utcnow()
        
        # Update book
        result = await book_collection.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            return {"msg": "Not Found"}, 404
        
        result["id"] = str(result["_id"])
        del result["_id"]
        
        return {
            "msg": "Ok",
            "data": result
        }
        
    except Exception as error:
        return {"msg": str(error)}, 500

@router.delete("/books/{book_id}", response_model=dict)
async def delete_book(
    book_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Delete a book by ID - requires authentication
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(book_id):
            return {"msg": "Invalid book ID"}, 400
            
        book_collection = await get_book_collection()
        
        # Delete book
        result = await book_collection.delete_one({"_id": ObjectId(book_id)})
        
        if result.deleted_count == 0:
            return {"msg": "Not Found"}, 404
        
        return {"msg": "Ok"}
        
    except Exception as error:
        return {"msg": str(error)}, 500
