from typing import List, Dict, Any
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API CSV desde Google Drive",
    description="API REST que lee automáticamente un archivo CSV desde Google Drive y lo expone en formato JSON",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite acceso desde cualquier dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# URL del archivo CSV en Google Drive
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4n2VLM5ie-XRD3_ZzwoOfukCTZLoF_KgJRsCKDHVZ-OJ9ugG1hL5gc32Y24gUgngxkzX-FuYpBF7/pub?gid=20714965&single=true&output=csv"

@app.get("/")
async def root():
    """
    Endpoint raíz que devuelve información sobre la API
    """
    return {
        "message": "API CSV desde Google Drive",
        "version": "1.0.0",
        "endpoints": {
            "datos": "/datos - Obtiene los datos del CSV en formato JSON",
            "docs": "/docs - Documentación interactiva de la API"
        }
    }

@app.get("/datos", response_model=List[Dict[str, Any]])
async def obtener_datos():
    """
    Endpoint que lee el archivo CSV desde Google Drive y devuelve los datos en formato JSON.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los datos del CSV
        
    Raises:
        HTTPException: Si hay un error al leer el archivo CSV
    """
    try:
        logger.info("Iniciando lectura del archivo CSV desde Google Drive")
        
        # Leer el archivo CSV desde la URL
        df = pd.read_csv(CSV_URL)
        
        logger.info(f"CSV leído exitosamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        
        # Convertir el DataFrame a una lista de diccionarios
        datos = df.to_dict(orient="records")
        
        logger.info(f"Datos convertidos a JSON. Total de registros: {len(datos)}")
        
        return datos
        
    except Exception as e:
        logger.error(f"Error al leer el archivo CSV: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer el archivo CSV: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud de la API
    """
    return {"status": "healthy", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 