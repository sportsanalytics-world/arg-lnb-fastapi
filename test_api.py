#!/usr/bin/env python3
"""
Script de pruebas para la API CSV desde Google Drive
"""

import requests
import json
import sys

# Configuración
base_url = "http://localhost:8000"
results = {}

def test_endpoint(name, url, expected_status=200):
    """Función auxiliar para probar endpoints"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            results[name] = {"status": "✅ OK", "data": response.json() if response.content else None}
            return True
        else:
            results[name] = {"status": "❌ ERROR", "status_code": response.status_code}
            return False
    except Exception as e:
        results[name] = {"status": "❌ ERROR", "error": str(e)}
        return False

def print_result(name, success, message=""):
    """Imprimir resultado de prueba"""
    status = "✅" if success else "❌"
    print(f"{status} {name}: {'OK' if success else 'ERROR'} - {message}")

print("🚀 Iniciando pruebas de la API CSV desde Google Drive")
print("=" * 60)
print(f"📍 URL base: {base_url}")
print()

# Test 1: Endpoint raíz
print("🔍 Probando endpoint raíz...")
success = test_endpoint("root", f"{base_url}/")
if success:
    data = results["root"]["data"]
    print_result("Endpoint raíz", True, data.get("message", "API funcionando"))

# Test 2: Endpoint de salud
print("🔍 Probando endpoint de salud...")
success = test_endpoint("health", f"{base_url}/health")
if success:
    data = results["health"]["data"]
    print_result("Endpoint salud", True, data.get("status", "healthy"))

# Test 3: Endpoint de información
print("🔍 Probando endpoint de información...")
success = test_endpoint("info", f"{base_url}/info")
if success:
    data = results["info"]["data"]
    total_records = data.get("total_records", 0)
    total_columns = data.get("total_columns", 0)
    print_result("Endpoint info", True, f"{total_records} registros, {total_columns} columnas")

# Test 4: Endpoint de datos básico
print("🔍 Probando endpoint de datos básico...")
success = test_endpoint("datos_basic", f"{base_url}/datos?limit=3")
if success:
    data = results["datos_basic"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos básico", True, f"{len(data)} registros")

# Test 5: Endpoint de datos con filtro por temporada
print("🔍 Probando endpoint de datos con filtro por temporada...")
success = test_endpoint("datos_season", f"{base_url}/datos?season=2023&limit=3")
if success:
    data = results["datos_season"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (filtro temporada)", True, f"{len(data)} registros para 2023")

# Test 6: Endpoint de datos con filtro por nombre ajustado
print("🔍 Probando endpoint de datos con filtro por nombre ajustado...")
success = test_endpoint("datos_first_name", f"{base_url}/datos?first_name=Pablo&limit=3")
if success:
    data = results["datos_first_name"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (nombre ajustado)", True, f"{len(data)} registros para 'Pablo'")

# Test 7: Endpoint de datos con filtro por apellido ajustado
print("🔍 Probando endpoint de datos con filtro por apellido ajustado...")
success = test_endpoint("datos_last_name", f"{base_url}/datos?last_name=Garcia&limit=3")
if success:
    data = results["datos_last_name"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (apellido ajustado)", True, f"{len(data)} registros para 'Garcia'")

# Test 8: Endpoint de datos con filtro por fecha de nacimiento
print("🔍 Probando endpoint de datos con filtro por fecha de nacimiento...")
success = test_endpoint("datos_birthdate", f"{base_url}/datos?birthdate=2000-01-27&limit=3")
if success:
    data = results["datos_birthdate"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (fecha nacimiento)", True, f"{len(data)} registros para 2000-01-27")

# Test 9: Endpoint de datos con filtro por altura
print("🔍 Probando endpoint de datos con filtro por altura...")
success = test_endpoint("datos_height", f"{base_url}/datos?height=198&limit=3")
if success:
    data = results["datos_height"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (altura)", True, f"{len(data)} registros para altura 198cm")

# Test 10: Endpoint de datos con filtro por peso
print("🔍 Probando endpoint de datos con filtro por peso...")
success = test_endpoint("datos_weight", f"{base_url}/datos?weight=85&limit=3")
if success:
    data = results["datos_weight"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (peso)", True, f"{len(data)} registros para peso 85kg")

# Test 11: Endpoint de datos con múltiples filtros
print("🔍 Probando endpoint de datos con múltiples filtros...")
success = test_endpoint("datos_multiple", f"{base_url}/datos?season=2023&position=C&limit=3")
if success:
    data = results["datos_multiple"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (múltiples filtros)", True, f"{len(data)} registros para temporada 2023, posición C")

# Test 12: Endpoint de datos agrupados por jugador
print("🔍 Probando endpoint de datos agrupados por jugador...")
success = test_endpoint("datos_group_player", f"{base_url}/datos?first_name=Pablo&group_by=player&limit=3")
if success:
    data = results["datos_group_player"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (agrupado por jugador)", True, f"{len(data)} jugadores únicos")

# Test 13: Endpoint de datos agrupados por equipo
print("🔍 Probando endpoint de datos agrupados por equipo...")
success = test_endpoint("datos_group_team", f"{base_url}/datos?season=2023&group_by=team&limit=3")
if success:
    data = results["datos_group_team"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (agrupado por equipo)", True, f"{len(data)} equipos")

# Test 14: Endpoint de datos agrupados por temporada
print("🔍 Probando endpoint de datos agrupados por temporada...")
success = test_endpoint("datos_group_season", f"{base_url}/datos?group_by=season&limit=3")
if success:
    data = results["datos_group_season"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (agrupado por temporada)", True, f"{len(data)} temporadas")

# Test 15: Endpoint de datos con estadísticas
print("🔍 Probando endpoint de datos con estadísticas...")
success = test_endpoint("datos_with_stats", f"{base_url}/datos?season=2023&include_stats=true&limit=3")
if success:
    data = results["datos_with_stats"]["data"]
    if isinstance(data, dict) and 'stats' in data:
        stats = data['stats']
        total_records = stats.get('total_records', 0)
        print_result("Endpoint datos (con estadísticas)", True, f"{total_records} registros totales")

# Test 16: Endpoint de datos con agrupación y estadísticas
print("🔍 Probando endpoint de datos con agrupación y estadísticas...")
success = test_endpoint("datos_group_stats", f"{base_url}/datos?first_name=Pablo&group_by=player&include_stats=true&limit=3")
if success:
    data = results["datos_group_stats"]["data"]
    if isinstance(data, dict) and 'stats' in data:
        stats = data['stats']
        total_records = stats.get('total_records', 0)
        print_result("Endpoint datos (agrupado + estadísticas)", True, f"{total_records} jugadores únicos")

# Test 17: Endpoint de datos con trayectoria completa (career)
print("🔍 Probando endpoint de datos con trayectoria completa...")
success = test_endpoint("datos_career", f"{base_url}/datos?first_name=Pablo&group_by=career&limit=3")
if success:
    data = results["datos_career"]["data"]
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    print_result("Endpoint datos (trayectoria completa)", True, f"{len(data)} jugadores con trayectoria")

# Test 18: Endpoint de datos con trayectoria completa y estadísticas
print("🔍 Probando endpoint de datos con trayectoria completa y estadísticas...")
success = test_endpoint("datos_career_stats", f"{base_url}/datos?first_name=Pablo&group_by=career&include_stats=true&limit=3")
if success:
    data = results["datos_career_stats"]["data"]
    if isinstance(data, dict) and 'stats' in data:
        stats = data['stats']
        total_records = stats.get('total_records', 0)
        print_result("Endpoint datos (trayectoria + estadísticas)", True, f"{total_records} jugadores con trayectoria")

print()
print("=" * 60)
print("📊 RESUMEN DE PRUEBAS")
print("=" * 60)

# Contar resultados
total_tests = len(results)
passed_tests = sum(1 for result in results.values() if result["status"] == "✅ OK")
failed_tests = total_tests - passed_tests

for test_name, result in results.items():
    status = result["status"]
    print(f"{test_name.upper():<25} {status}")

print()
print(f"✅ Pruebas exitosas: {passed_tests}/{total_tests}")
print(f"❌ Pruebas fallidas: {failed_tests}/{total_tests}")

if failed_tests > 0:
    print("\n⚠️  Algunas pruebas fallaron")
    print("❌ Revisa los errores anteriores")
else:
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")

print()
print("📝 Para ver la documentación interactiva, visita:")
print(f"   {base_url}/docs")
print()
print("📝 Para ver la especificación OpenAPI, visita:")
print(f"   {base_url}/openapi.json") 