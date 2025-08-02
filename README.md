# API CSV desde Google Drive con FastAPI

Esta es una API REST construida con FastAPI que lee automáticamente un archivo CSV público alojado en Google Drive y expone su contenido en formato JSON.

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para APIs
- **Pandas**: Lectura eficiente de archivos CSV
- **CORS habilitado**: Permite acceso desde cualquier dominio
- **Tipado completo**: Usa type hints de Python
- **Documentación automática**: Swagger UI en `/docs`
- **Logging**: Registro de operaciones para debugging

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

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
- **Health check**: http://localhost:8000/health

## 📊 Endpoint Principal

### GET /datos

Lee el archivo CSV desde Google Drive y devuelve los datos en formato JSON.

**URL del CSV**: https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4n2VLM5ie-XRD3_ZzwoOfukCTZLoF_KgJRsCKDHVZ-OJ9ugG1hL5gc32Y24gUgngxkzX-FuYpBF7/pub?gid=20714965&single=true&output=csv

**Respuesta**: Lista de diccionarios con los datos del CSV

**Ejemplo de uso**:
```bash
curl http://localhost:8000/datos
```

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
├── README.md           # Este archivo
└── .gitignore          # Archivos a ignorar por Git
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

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.

---

**Nota**: Esta API lee el archivo CSV en tiempo real cada vez que se consulta el endpoint `/datos`, por lo que siempre obtendrás los datos más actualizados del archivo. 