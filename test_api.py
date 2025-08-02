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
    
    # Test 3: Endpoint de datos
    print("🔍 Probando endpoint de datos...")
    try:
        response = requests.get(f"{base_url}/datos")
        if response.status_code == 200:
            data = response.json()
            results["datos"] = {
                "status": "✅ OK", 
                "registros": len(data),
                "muestra": data[:2] if data else []
            }
            print(f"✅ Endpoint datos: OK - {len(data)} registros obtenidos")
            if data:
                print(f"   Muestra del primer registro: {data[0]}")
        else:
            results["datos"] = {"status": "❌ ERROR", "status_code": response.status_code}
            print(f"❌ Endpoint datos: ERROR - Status {response.status_code}")
    except Exception as e:
        results["datos"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"❌ Endpoint datos: ERROR - {str(e)}")
    
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