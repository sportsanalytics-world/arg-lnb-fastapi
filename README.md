# API CSV desde Google Drive con FastAPI

Esta es una API REST construida con FastAPI que lee automáticamente un archivo CSV público alojado en Google Drive y expone su contenido en formato JSON.

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para APIs
- **Pandas**: Lectura eficiente de archivos CSV
- **CORS habilitado**: Permite acceso desde cualquier dominio
- **Tipado completo**: Usa type hints de Python
- **Documentación automática**: Swagger UI en `/docs`
- **Especificación OpenAPI 3.1.0**: Archivo `openapi.yaml` incluido
- **Logging**: Registro de operaciones para debugging
- **Paginación**: Soporte para paginación de resultados (máximo 100 registros por página)
- **Filtros avanzados**: Múltiples opciones de filtrado por equipo, temporada, posición, nacionalidad, nombre, apellido, fecha de nacimiento, altura y peso
- **Compatibilidad ChatGPT**: Especificación OpenAPI compatible con ChatGPT Customizado

## 📋 Requisitos

- Python 3.8 o superior (recomendado 3.11+)
- pip (gestor de paquetes de Python)
- Dependencias (instaladas automáticamente):
  - FastAPI >= 0.115.13
  - Uvicorn >= 0.32.1
  - Pandas >= 2.2.3
  - Requests >= 2.32.3
  - Gunicorn >= 23.0.0

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd ARG-LNB-FastAPI
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Ejecución Local

### Opción 1: Usando uvicorn directamente
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 2: Usando Python
```bash
python main.py
```

### Opción 3: Usando uvicorn con configuración personalizada
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info
```

## 🌐 Endpoints Disponibles

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **API Base**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Endpoint de datos**: http://localhost:8000/datos
- **Información de datos**: http://localhost:8000/info
- **Health check**: http://localhost:8000/health

## 📊 Endpoint Principal

### GET /datos

Lee el archivo CSV desde Google Drive y devuelve los datos en formato JSON con paginación y filtros.

**URL del CSV**: https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4n2VLM5ie-XRD3_ZzwoOfukCTZLoF_KgJRsCKDHVZ-OJ9ugG1hL5gc32Y24gUgngxkzX-FuYpBF7/pub?gid=20714965&single=true&output=csv

**Parámetros de consulta**:
- `page` (int, opcional): Número de página (default: 1)
- `limit` (int, opcional): Registros por página (default: 50, máximo: 100)
- `team` (string, opcional): Filtrar por equipo
- `season` (int, opcional): Filtrar por temporada
- `position` (string, opcional): Filtrar por posición (G, F, C)
- `nationality` (string, opcional): Filtrar por nacionalidad
- `first_name` (string, opcional): Filtrar por nombre ajustado del jugador
- `last_name` (string, opcional): Filtrar por apellido ajustado del jugador
- `birthdate` (string, opcional): Filtrar por fecha de nacimiento (YYYY-MM-DD)
- `height` (float, opcional): Filtrar por altura en cm
- `weight` (float, opcional): Filtrar por peso en kg

**Respuesta**: Lista de diccionarios con los datos del CSV paginados

**Ejemplos de uso**:
```bash
# Obtener primera página (50 registros por defecto)
curl http://localhost:8000/datos

# Obtener segunda página con 20 registros
curl "http://localhost:8000/datos?page=2&limit=20"

# Filtrar por equipo
curl "http://localhost:8000/datos?team=Boca%20Juniors"

# Filtrar por temporada y posición
curl "http://localhost:8000/datos?season=2023&position=F"

# Combinar filtros y paginación
curl "http://localhost:8000/datos?team=Argentina&season=2023&page=1&limit=10"

# Buscar por nombre
curl "http://localhost:8000/datos?first_name=Pablo&limit=5"

# Buscar por apellido
curl "http://localhost:8000/datos?last_name=Aaron&limit=3"

# Buscar por fecha de nacimiento
curl "http://localhost:8000/datos?birthdate=2000-01-27&limit=5"

# Buscar por altura específica
curl "http://localhost:8000/datos?height=190&limit=3"

# Buscar por peso específico
curl "http://localhost:8000/datos?weight=85&limit=3"
```

### GET /info

Devuelve información sobre los datos disponibles, incluyendo filtros y estadísticas.

**Respuesta**: Información sobre columnas, filtros disponibles y configuración de paginación

**Ejemplo de uso**:
```bash
curl http://localhost:8000/info
```

## 📋 Especificación OpenAPI

El proyecto incluye un archivo `openapi.yaml` con la especificación completa de la API en formato OpenAPI 3.1.0. Esta especificación incluye:

- **Documentación completa** de todos los endpoints
- **Esquemas de datos** para request/response
- **Ejemplos de uso** para cada endpoint
- **Parámetros de consulta** con validaciones
- **Códigos de respuesta** y manejo de errores

### Uso de la especificación OpenAPI:

1. **Para ChatGPT y otros LLMs**: Usa el archivo `openapi.yaml` para configurar conectores
2. **Para desarrollo**: Importa la especificación en herramientas como Postman
3. **Para documentación**: La especificación se puede usar para generar documentación automática

### Endpoints documentados:

- `GET /` - Información de la API
- `GET /datos` - Datos del CSV con paginación y filtros
- `GET /info` - Información sobre los datos disponibles
- `GET /health` - Verificación de salud

## 🚀 Despliegue

### Render

1. **Conecta tu repositorio a Render:**
   - Ve a [render.com](https://render.com) y crea una cuenta
   - Haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub/GitLab

2. **Configuración automática (recomendado):**
   - Render detectará automáticamente el archivo `render.yaml`
   - El servicio se configurará automáticamente

3. **Configuración manual (si es necesario):**
   - **Name**: `arg-lnb-fastapi` (o el nombre que prefieras)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (para empezar)

4. **Variables de entorno (opcionales):**
   - No necesarias para este proyecto
   - Si quieres cambiar la URL del CSV, puedes agregar:
     - `CSV_URL`: Nueva URL del archivo CSV

### Fly.io

1. Instala Fly CLI
2. Ejecuta:
   ```bash
   fly launch
   fly deploy
   ```

### Railway

1. Conecta tu repositorio a Railway
2. Railway detectará automáticamente que es una aplicación Python
3. El archivo `requirements.txt` se instalará automáticamente

### Heroku

1. Crea un archivo `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Despliega usando Heroku CLI o GitHub integration

## 🔧 Configuración

### Variables de Entorno

Puedes configurar las siguientes variables de entorno:

- `CSV_URL`: URL del archivo CSV (por defecto usa la URL especificada)
- `LOG_LEVEL`: Nivel de logging (INFO, DEBUG, WARNING, ERROR)

### Personalización

Para cambiar la URL del CSV, modifica la variable `CSV_URL` en `main.py`:

```python
CSV_URL = "tu-nueva-url-del-csv"
```

## 📝 Estructura del Proyecto

```
ARG-LNB-FastAPI/
├── main.py              # Archivo principal de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── openapi.yaml         # Especificación OpenAPI 3.0
├── README.md           # Este archivo
├── .gitignore          # Archivos a ignorar por Git
├── render.yaml         # Configuración para Render
├── Dockerfile          # Configuración para Docker
├── docker-compose.yml  # Configuración para desarrollo local
├── test_api.py         # Script de pruebas
└── start.sh            # Script de inicio para Render
```

## 🐛 Troubleshooting

### Error al leer el CSV
- Verifica que la URL del CSV sea accesible públicamente
- Asegúrate de que el archivo esté en formato CSV válido
- Revisa los logs para más detalles del error

### Error de CORS
- La aplicación ya tiene CORS configurado para permitir todos los orígenes
- Si necesitas restringir orígenes, modifica `allow_origins` en `main.py`

### Error de puerto en uso
- Cambia el puerto en el comando de ejecución:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8001
  ```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🔒 Información Legal

- **[Política de Privacidad](privacy-policy.md)** - Cómo manejamos la información y datos
- **[Términos de Servicio](terms-of-service.md)** - Términos de uso de la API

### Cumplimiento con ChatGPT Customizado

Esta API está diseñada para ser compatible con ChatGPT Customizado y cumple con todos los requisitos de privacidad y términos de servicio necesarios para la integración.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.

---

**Nota**: Esta API lee el archivo CSV en tiempo real cada vez que se consulta el endpoint `/datos`, por lo que siempre obtendrás los datos más actualizados del archivo. 