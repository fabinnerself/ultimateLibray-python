#!/usr/bin/env python3
"""
Script simple para probar conexión MongoDB
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Prueba simple de conexión a MongoDB"""
    
    # Obtener URI de conexión
    mongodb_uri = os.getenv("MONGODB_CONNECT_URI", "")
    database_name = os.getenv("DATABASE_NAME", "ultimate_library")
    
    if not mongodb_uri:
        print("❌ Error: MONGODB_CONNECT_URI no está configurado")
        return False
    
    try:
        # Intentar importar pymongo
        try:
            from pymongo import MongoClient
        except ImportError:
            print("❌ Error: pymongo no está instalado")
            print("   Ejecuta: pip install pymongo")
            return False
        
        print("🚀 Probando conexión a MongoDB...")
        print(f"📊 Base de datos: {database_name}")
        print(f"🌐 Conectando a: {mongodb_uri[:50]}...")
        
        # Conectar a MongoDB
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Probar conexión
        client.admin.command('ping')
        print("✅ Conexión exitosa!")
        
        # Obtener base de datos
        db = client[database_name]
        
        # Verificar colecciones existentes
        collections = db.list_collection_names()
        print(f"📚 Colecciones existentes: {collections}")
        
        # Obtener/crear colección users
        users_collection = db.users
        
        # Crear usuario de prueba
        print("👤 Creando estructura de usuario...")
        
        test_user = {
            "name": "Test",
            "lastname": "User", 
            "email": "test@example.com",
            "hashed_password": "$2b$12$example.hash.for.testing.only",
            "phone": "+1234567890",
            "birthday": datetime(1990, 1, 15),
            "avatar": None,
            "role": "user",
            "is_active": True,
            "is_verified": False,
            "last_login": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": None,
            "is_deleted": False
        }
        
        # Verificar si existe usuario de prueba
        existing = users_collection.find_one({"email": "test@example.com"})
        
        if existing:
            print("⚠️  Usuario de prueba ya existe, actualizando...")
            users_collection.update_one(
                {"email": "test@example.com"},
                {"$set": {"updated_at": datetime.utcnow()}}
            )
        else:
            print("➕ Insertando usuario de prueba...")
            users_collection.insert_one(test_user)
        
        # Verificar resultado
        user_count = users_collection.count_documents({})
        print(f"📊 Total usuarios: {user_count}")
        
        # Mostrar usuario creado
        created_user = users_collection.find_one(
            {"email": "test@example.com"},
            {"hashed_password": 0}
        )
        
        if created_user:
            print("✅ Usuario verificado:")
            print(f"   📧 {created_user['email']}")
            print(f"   👤 {created_user['name']} {created_user['lastname']}")
            print(f"   🔰 Rol: {created_user['role']}")
            print(f"   📅 Creado: {created_user['created_at']}")
        
        # Crear índice único en email
        print("🔍 Creando índice único en email...")
        try:
            users_collection.create_index("email", unique=True)
            print("✅ Índice creado")
        except Exception as e:
            print(f"ℹ️  Índice ya existe")
        
        # Cerrar conexión
        client.close()
        
        print("\n🎉 ¡ÉXITO! Tu conexión MongoDB funciona perfectamente")
        print("✅ Base de datos configurada")
        print("✅ Colección users creada")
        print("✅ Estructura de usuario validada")
        print("✅ Índices configurados")
        
        print("\n🎯 Siguiente paso:")
        print("   Ejecuta: python start.py")
        print("   Y visita: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔧 Posibles causas:")
        print("1. URI de conexión incorrecta")
        print("2. Credenciales de MongoDB incorrectas")  
        print("3. IP no está en whitelist de MongoDB Atlas")
        print("4. Cluster de MongoDB inactivo")
        print("5. Problemas de conectividad de red")
        
        print("\n💡 Soluciones:")
        print("1. Verifica tu URI en MongoDB Atlas")
        print("2. Ve a Network Access y agrega tu IP (0.0.0.0/0 para todas)")
        print("3. Verifica que el cluster esté activo")
        
        return False

def main():
    """Función principal"""
    print("🔧 Test MongoDB - Ultimate Library API")
    print("=" * 40)
    
    success = test_connection()
    
    if not success:
        print("\n❌ Test falló. Revisa la configuración.")

if __name__ == "__main__":
    main()
