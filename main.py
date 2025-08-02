from typing import List, Dict, Any, Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
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
async def obtener_datos(
    page: int = Query(default=1, ge=1, description="Número de página (empezando en 1)"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros por página (máximo 100)"),
    team: Optional[str] = Query(default=None, description="Filtrar por equipo"),
    season: Optional[int] = Query(default=None, description="Filtrar por temporada"),
    position: Optional[str] = Query(default=None, description="Filtrar por posición (G, F, C)"),
    nationality: Optional[str] = Query(default=None, description="Filtrar por nacionalidad"),
    first_name: Optional[str] = Query(default=None, description="Filtrar por nombre ajustado del jugador"),
    last_name: Optional[str] = Query(default=None, description="Filtrar por apellido ajustado del jugador"),
    birthdate: Optional[str] = Query(default=None, description="Filtrar por fecha de nacimiento (YYYY-MM-DD)"),
    height: Optional[float] = Query(default=None, description="Filtrar por altura en cm"),
    weight: Optional[float] = Query(default=None, description="Filtrar por peso en kg")
):
    """
    Endpoint que lee el archivo CSV desde Google Drive y devuelve los datos en formato JSON con paginación y filtros.
    
    Args:
        page: Número de página (empezando en 1)
        limit: Número de registros por página (máximo 100)
        team: Filtrar por equipo
        season: Filtrar por temporada
        position: Filtrar por posición
        nationality: Filtrar por nacionalidad
    
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
        
        # Aplicar filtros si se proporcionan
        if team:
            df = df[df['Team'].str.contains(team, case=False, na=False)]
            logger.info(f"Filtrado por equipo '{team}': {len(df)} registros")
            
        if season:
            df = df[df['Season'] == season]
            logger.info(f"Filtrado por temporada {season}: {len(df)} registros")
            
        if position:
            df = df[df['Position'].str.contains(position, case=False, na=False)]
            logger.info(f"Filtrado por posición '{position}': {len(df)} registros")
            
        if nationality:
            df = df[df['Nationality'].str.contains(nationality, case=False, na=False)]
            logger.info(f"Filtrado por nacionalidad '{nationality}': {len(df)} registros")
            
        if first_name:
            df = df[df['Adjusted first name'].str.contains(first_name, case=False, na=False)]
            logger.info(f"Filtrado por nombre ajustado '{first_name}': {len(df)} registros")
            
        if last_name:
            df = df[df['Adjusted last name'].str.contains(last_name, case=False, na=False)]
            logger.info(f"Filtrado por apellido ajustado '{last_name}': {len(df)} registros")
            
        if birthdate:
            df = df[df['Birthdate'].str.contains(birthdate, case=False, na=False)]
            logger.info(f"Filtrado por fecha de nacimiento '{birthdate}': {len(df)} registros")
            
        if height is not None:
            df = df[df['Height'] == height]
            logger.info(f"Filtrado por altura {height}cm: {len(df)} registros")
            
        if weight is not None:
            df = df[df['Weight'] == weight]
            logger.info(f"Filtrado por peso {weight}kg: {len(df)} registros")
        
        # Calcular paginación
        total_records = len(df)
        total_pages = (total_records + limit - 1) // limit
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        # Aplicar paginación
        df_paginated = df.iloc[start_idx:end_idx]
        
        # Convertir el DataFrame a una lista de diccionarios
        datos = df_paginated.to_dict(orient="records")
        
        logger.info(f"Datos paginados: página {page}/{total_pages}, registros {start_idx+1}-{min(end_idx, total_records)} de {total_records}")
        
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

@app.get("/info")
async def obtener_info():
    """
    Endpoint que devuelve información sobre los datos disponibles
    """
    try:
        logger.info("Obteniendo información sobre los datos")
        
        # Leer el archivo CSV desde la URL
        df = pd.read_csv(CSV_URL)
        
        # Obtener estadísticas básicas
        total_records = len(df)
        columns = list(df.columns)
        
        # Obtener valores únicos para filtros
        teams = sorted(df['Team'].dropna().unique().tolist())
        seasons = sorted(df['Season'].dropna().unique().tolist())
        positions = sorted(df['Position'].dropna().unique().tolist())
        nationalities = sorted(df['Nationality'].dropna().unique().tolist())
        
        return {
            "total_records": total_records,
            "columns": columns,
            "filters_available": {
                "teams": teams,
                "seasons": seasons,
                "positions": positions,
                "nationalities": nationalities
            },
            "pagination": {
                "default_page_size": 50,
                "max_page_size": 100
            }
        }
        
    except Exception as e:
        logger.error(f"Error al obtener información: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener información: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 