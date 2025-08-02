#!/usr/bin/env python3
"""
Script de prueba para verificar que la API funciona correctamente
"""

import requests
import json
import sys
from typing import Dict, Any

def test_api_endpoints(base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Prueba todos los endpoints de la API
    
    Args:
        base_url: URL base de la API
        
    Returns:
        Dict con los resultados de las pruebas
    """
    results = {}
    
    # Test 1: Endpoint raíz
    print("🔍 Probando endpoint raíz...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            results["root"] = {"status": "✅ OK", "data": response.json()}
            print(f"✅ Endpoint raíz: OK - {response.json()}")
        else:
            results["root"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint raíz: ERROR - Status {response.status_code}")
    except Exception as e:
        results["root"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint raíz: ERROR - {str(e)}")
    
    # Test 2: Health check
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            results["health"] = {"status": "✅ OK", "data": response.json()}
            print(f"✅ Health check: OK - {response.json()}")
        else:
            results["health"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Health check: ERROR - Status {response.status_code}")
    except Exception as e:
        results["health"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Health check: ERROR - {str(e)}")
    
    # Test 3: Endpoint de información
    print("🔍 Probando endpoint de información...")
    try:
        response = requests.get(f"{base_url}/info")
        if response.status_code == 200:
            data = response.json()
            results["info"] = {
                "status": "✅ OK", 
                "total_records": data.get("total_records", 0),
                "columns": len(data.get("columns", [])),
                "filters": len(data.get("filters_available", {}))
            }
            print(f"✅ Endpoint info: OK - {data.get('total_records', 0)} registros totales")
            print(f"   Columnas: {len(data.get('columns', []))}, Filtros: {len(data.get('filters_available', {}))}")
        else:
            results["info"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint info: ERROR - Status {response.status_code}")
    except Exception as e:
        results["info"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint info: ERROR - {str(e)}")
    
    # Test 4: Endpoint de datos (paginación por defecto)
    print("🔍 Probando endpoint de datos (paginación por defecto)...")
    try:
        response = requests.get(f"{base_url}/datos")
        if response.status_code == 200:
            data = response.json()
            results["datos_default"] = {
                "status": "✅ OK", 
                "registros": len(data),
                "muestra": data[:2] if data else []
            }
            print(f"✅ Endpoint datos (default): OK - {len(data)} registros obtenidos")
            if data:
                print(f"   Muestra del primer registro: {list(data[0].keys())[:3]}...")
        else:
            results["datos_default"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint datos (default): ERROR - Status {response.status_code}")
    except Exception as e:
        results["datos_default"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint datos (default): ERROR - {str(e)}")
    
    # Test 5: Endpoint de datos con límite pequeño
    print("🔍 Probando endpoint de datos con límite pequeño...")
    try:
        response = requests.get(f"{base_url}/datos?limit=5")
        if response.status_code == 200:
            data = response.json()
            results["datos_limit"] = {
                "status": "✅ OK", 
                "registros": len(data),
                "limit_requested": 5
            }
            print(f"✅ Endpoint datos (limit=5): OK - {len(data)} registros obtenidos")
        else:
            results["datos_limit"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint datos (limit=5): ERROR - Status {response.status_code}")
    except Exception as e:
        results["datos_limit"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint datos (limit=5): ERROR - {str(e)}")
    
    # Test 6: Endpoint de datos con filtro por equipo
    print("🔍 Probando endpoint de datos con filtro por equipo...")
    try:
        response = requests.get(f"{base_url}/datos?team=Boca%20Juniors&limit=3")
        if response.status_code == 200:
            data = response.json()
            results["datos_filter"] = {
                "status": "✅ OK", 
                "registros": len(data),
                "filtro_aplicado": "team=Boca Juniors"
            }
            print(f"✅ Endpoint datos (filtro): OK - {len(data)} registros de Boca Juniors")
            if data:
                print(f"   Primer jugador: {data[0].get('First name', '')} {data[0].get('Last name', '')}")
        else:
            results["datos_filter"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint datos (filtro): ERROR - Status {response.status_code}")
    except Exception as e:
        results["datos_filter"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint datos (filtro): ERROR - {str(e)}")
    
    # Test 7: Endpoint de datos con filtro por temporada
    print("🔍 Probando endpoint de datos con filtro por temporada...")
    try:
        response = requests.get(f"{base_url}/datos?season=2023&limit=3")
        if response.status_code == 200:
            data = response.json()
            results["datos_season"] = {
                "status": "✅ OK", 
                "registros": len(data),
                "filtro_aplicado": "season=2023"
            }
            print(f"✅ Endpoint datos (temporada): OK - {len(data)} registros de 2023")
        else:
            results["datos_season"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint datos (temporada): ERROR - Status {response.status_code}")
    except Exception as e:
        results["datos_season"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint datos (temporada): ERROR - {str(e)}")
    
    return results

def main():
    """Función principal del script de prueba"""
    print("🚀 Iniciando pruebas de la API CSV desde Google Drive")
    print("=" * 60)
    
    # Verificar si se proporcionó una URL personalizada
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    print(f"📍 URL base: {base_url}")
    print()
    
    # Ejecutar pruebas
    results = test_api_endpoints(base_url)
    
    # Mostrar resumen
    print()
    print("=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for endpoint, result in results.items():
        status = result["status"]
        print(f"{endpoint.upper():<15} {status}")
    
    # Verificar si todas las pruebas pasaron
    all_passed = all("✅ OK" in result["status"] for result in results.values())
    
    print()
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ La API está funcionando correctamente")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("❌ Revisa los errores anteriores")
    
    print()
    print("📝 Para ver la documentación interactiva, visita:")
    print(f"   {base_url}/docs")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 