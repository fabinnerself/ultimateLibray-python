#!/usr/bin/env python3
"""
Script para probar la API Ultimate Library
Asegúrate de que la API esté corriendo en http://localhost:8000
"""

import requests
import json
from datetime import date

# URL base de la API
BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

def test_api():
    """Prueba completa de la API"""
    
    print("🚀 Probando Ultimate Library API")
    print("=" * 40)
    
    # 1. Probar endpoint principal
    print("\n1. 🔍 Probando endpoint principal...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            print("✅ API principal funcionando:")
            print(f"   📝 Mensaje: {data.get('message', 'N/A')}")
            print(f"   🔖 Versión: {data.get('version', 'N/A')}")
            print(f"   🌍 Entorno: {data.get('environment', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        print("   Asegúrate de que la API esté corriendo con: python start.py")
        return False
    
    # 2. Probar health check
    print("\n2. ❤️  Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('status', 'N/A')}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
    
    # 3. Probar documentación
    print("\n3. 📖 Probando documentación...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Documentación disponible en: http://localhost:8000/docs")
        else:
            print(f"❌ Documentación no disponible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accediendo documentación: {e}")
    
    # 4. Probar registro de usuario
    print("\n4. 👤 Probando registro de usuario...")
    user_data = {
        "name": "Test",
        "lastname": "Usuario",
        "email": "test.usuario@example.com",
        "password": "TestPass123",
        "phone": "+1234567890",
        "birthday": "1995-01-15"
    }
    
    try:
        response = requests.post(
            f"{API_V1}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Usuario registrado exitosamente:")
            print(f"   📧 Email: {data['data'].get('email', 'N/A')}")
            print(f"   👤 Nombre: {data['data'].get('name', 'N/A')} {data['data'].get('lastname', 'N/A')}")
            print(f"   🔰 Rol: {data['data'].get('role', 'N/A')}")
        else:
            error_data = response.json()
            print(f"❌ Error registrando usuario: {response.status_code}")
            print(f"   📝 Detalle: {error_data.get('detail', error_data.get('msg', 'Error desconocido'))}")
    except Exception as e:
        print(f"❌ Error en registro: {e}")
    
    # 5. Probar login
    print("\n5. 🔐 Probando login...")
    login_data = {
        "email": "test.usuario@example.com",
        "password": "TestPass123"
    }
    
    try:
        response = requests.post(
            f"{API_V1}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data['data']['access_token']
            print("✅ Login exitoso:")
            print(f"   🎫 Token obtenido (primeros 20 chars): {token[:20]}...")
            print(f"   👤 Usuario: {data['data']['user']['name']} {data['data']['user']['lastname']}")
            
            # 6. Probar endpoint protegido
            print("\n6. 🛡️  Probando endpoint protegido...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(f"{API_V1}/users/me", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Endpoint protegido funcionando:")
                    print(f"   📧 Email: {data['data'].get('email', 'N/A')}")
                    print(f"   🔰 Rol: {data['data'].get('role', 'N/A')}")
                    print(f"   ✅ Activo: {data['data'].get('is_active', 'N/A')}")
                else:
                    print(f"❌ Error en endpoint protegido: {response.status_code}")
            except Exception as e:
                print(f"❌ Error accediendo endpoint protegido: {e}")
                
        else:
            error_data = response.json()
            print(f"❌ Error en login: {response.status_code}")
            print(f"   📝 Detalle: {error_data.get('detail', error_data.get('msg', 'Error desconocido'))}")
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
    
    # 7. Probar endpoint de books (sin autenticación)
    print("\n7. 📚 Probando listado de libros...")
    try:
        response = requests.get(f"{API_V1}/books")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de libros funcionando:")
            print(f"   📖 Total libros: {data.get('totalItems', 0)}")
            print(f"   📄 Página actual: {data.get('currentPage', 'N/A')}")
            print(f"   📊 Total páginas: {data.get('totalPages', 'N/A')}")
            
            if data.get('data') and len(data['data']) > 0:
                book = data['data'][0]
                print(f"   📚 Primer libro: {book.get('name', 'N/A')} - {book.get('author', 'N/A')}")
        else:
            print(f"❌ Error obteniendo libros: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en listado de libros: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Pruebas completadas!")
    print("\n📋 URLs útiles:")
    print(f"   🌐 API: {BASE_URL}")
    print(f"   📖 Docs: {BASE_URL}/docs")
    print(f"   🔍 ReDoc: {BASE_URL}/redoc")
    print(f"   ❤️  Health: {BASE_URL}/health")

def main():
    """Función principal"""
    try:
        # Verificar si requests está instalado
        import requests
        test_api()
    except ImportError:
        print("❌ Error: requests no está instalado")
        print("   Instálalo con: pip install requests")

if __name__ == "__main__":
    main()
