# Ultimate Library API - Python/FastAPI Version

Esta es la migración de la API de Node.js/Express a Python/FastAPI con funcionalidades mejoradas de autenticación y gestión de usuarios.

## 🚀 Características

- ✅ **Migración completa** desde Node.js/Express
- ✅ **FastAPI** con documentación automática (Swagger UI)
- ✅ **MongoDB** con Motor (driver asíncrono)
- ✅ **Autenticación JWT** con tokens Bearer
- ✅ **Gestión de usuarios** completa con roles
- ✅ **Soft delete** para usuarios
- ✅ **Validación de datos** con Pydantic
- ✅ **Paginación y búsqueda** en libros y usuarios
- ✅ **Deploy fácil en Vercel**

## 📁 Estructura del Proyecto

```
api/
├── __init__.py
├── main.py              # Punto de entrada principal
├── config.py            # Configuración de la aplicación
├── database.py          # Conexión a MongoDB
├── models/
│   ├── __init__.py
│   ├── book.py         # Modelos de Book
│   └── user.py         # Modelos de User
├── routers/
│   ├── __init__.py
│   ├── books.py        # CRUD de libros
│   └── users.py        # CRUD de usuarios + auth
├── auth/
│   ├── __init__.py
│   └── auth_utils.py   # Utilidades JWT y hash
└── utils/
    └── __init__.py
requirements.txt         # Dependencias Python
vercel.json             # Configuración para Vercel
.env.example            # Variables de entorno
.gitignore              # Archivos a ignorar
```

## 📚 API Endpoints

### Libros (Books) - Mantiene compatibilidad con Node.js
- `GET /api/v1/books` - Listar libros con paginación y búsqueda
- `GET /api/v1/books/{id}` - Obtener un libro específico
- `POST /api/v1/books` - Crear libro (requiere auth)
- `PUT /api/v1/books/{id}` - Actualizar libro (requiere auth)
- `DELETE /api/v1/books/{id}` - Eliminar libro (requiere auth)

### Autenticación
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Iniciar sesión (obtener token JWT)

### Usuarios
- `GET /api/v1/users/me` - Perfil del usuario actual
- `PUT /api/v1/users/me` - Actualizar perfil propio
- `PUT /api/v1/users/me/password` - Cambiar contraseña
- `GET /api/v1/users` - Listar usuarios (admin)
- `GET /api/v1/users/{id}` - Obtener usuario (admin)
- `PUT /api/v1/users/{id}` - Actualizar usuario (admin)
- `DELETE /api/v1/users/{id}` - Eliminar usuario (admin) - Soft delete

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` a `.env` y configura:

```env
# MongoDB
MONGODB_CONNECT_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
API_V1_PREFIX=/api/v1
PROJECT_NAME=Ultimate Library API
VERSION=1.0.0
DESCRIPTION=A FastAPI application for managing books and users

# Environment
ENVIRONMENT=development
PORT=8000
```

### 3. Ejecutar en desarrollo

```bash
# Desde el directorio raíz del proyecto
uvicorn api.main:app --reload --port 8000
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Deploy en Vercel

### 1. Instalar Vercel CLI

```bash
npm i -g vercel
```

### 2. Deploy

```bash
vercel --prod
```

### 3. Configurar variables de entorno en Vercel

En el dashboard de Vercel, agrega las mismas variables del archivo `.env`.

## 🔐 Autenticación

### Registro de usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "lastname": "Doe", 
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Usar token en requests

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📊 Modelo de Datos

### User Schema
```json
{
  "name": "string",
  "lastname": "string", 
  "email": "string",
  "password": "string",
  "phone": "string (opcional)",
  "birthday": "date (opcional)",
  "avatar": "string (opcional)",
  "role": "user|admin|moderator",
  "is_active": "boolean",
  "is_verified": "boolean", 
  "last_login": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime",
  "deleted_at": "datetime",
  "is_deleted": "boolean"
}
```

### Book Schema (compatible con Node.js)
```json
{
  "name": "string",
  "author": "string",
  "price": "number",
  "description": "string (opcional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🔄 Migración desde Node.js

La API mantiene **100% compatibilidad** con la versión de Node.js:

1. **Mismos endpoints** para books
2. **Misma estructura de respuesta JSON**
3. **Misma paginación** y parámetros de búsqueda
4. **Mismo formato** de errores

**Nuevas funcionalidades añadidas:**
- Sistema completo de usuarios
- Autenticación JWT
- Roles y permisos
- Soft delete
- Validaciones mejoradas

## 🎯 Diferencias clave vs Node.js

| Característica | Node.js | FastAPI |
|----------------|---------|---------|
| Framework | Express | FastAPI |
| Base de datos | Mongoose | Motor |
| Validación | Manual | Pydantic automática |
| Documentación | Manual | Swagger automático |
| Autenticación | ❌ | ✅ JWT |
| Usuarios | ❌ | ✅ CRUD completo |
| Tipos | JavaScript | Python + TypeHints |
| Performance | Buena | Excelente |

## 🧪 Testing

```bash
# Ejecutar tests (cuando los implementes)
pytest tests/
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:
- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/ultimate-library-fastapi/issues)

---

¡Happy coding! 🚀
