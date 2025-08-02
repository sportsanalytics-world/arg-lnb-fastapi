# Instrucciones para GPT Personalizado - API LNB Argentina

## 🎯 Objetivo
Esta API proporciona datos de jugadores de la Liga Nacional de Básquet (LNB) de Argentina. El endpoint principal `/datos` es flexible y permite múltiples tipos de consultas combinando parámetros.

## 📋 Endpoints Disponibles

### GET `/datos` - Endpoint Principal
**URL**: `https://arg-lnb-fastapi.onrender.com/datos`

**Parámetros disponibles**:
- `page` (int, default: 1): Número de página
- `limit` (int, default: 50, max: 100): Registros por página
- `team` (string): Filtrar por equipo
- `season` (int): Filtrar por temporada
- `position` (string): Filtrar por posición (G, F, C, PG, SG, SF, PF)
- `nationality` (string): Filtrar por nacionalidad
- `first_name` (string): Filtrar por nombre ajustado del jugador
- `last_name` (string): Filtrar por apellido ajustado del jugador
- `birthdate` (string, YYYY-MM-DD): Filtrar por fecha de nacimiento
- `height` (float): Filtrar por altura en cm
- `weight` (float): Filtrar por peso en kg
- `group_by` (string): Agrupar por 'player', 'team', o 'season'
- `include_stats` (boolean): Incluir estadísticas en la respuesta

## 🚨 REGLA FUNDAMENTAL: SIEMPRE USAR LIMIT

**IMPORTANTE**: Nunca hagas consultas sin el parámetro `limit`. El valor recomendado es entre 10-30 registros por consulta para evitar exceder los límites de tokens del GPT.

## 📊 Estrategias para Consultas Complejas

### 1. Consulta en Dos Pasos para Datos Grandes

**Paso 1**: Obtener estadísticas para entender el alcance
```bash
GET /datos?season=2023&include_stats=true&limit=1
```

**Paso 2**: Si hay muchos datos, usar paginación o filtros más específicos
```bash
GET /datos?season=2023&group_by=player&limit=20&page=1
GET /datos?season=2023&group_by=player&limit=20&page=2
# ... continuar según sea necesario
```

### 2. Filtros Específicos para Reducir Resultados

En lugar de consultas amplias, usa filtros combinados:
```bash
# ❌ Mal: Demasiados resultados
GET /datos?season=2023&group_by=player

# ✅ Bien: Filtros específicos
GET /datos?season=2023&position=C&group_by=player&limit=20
GET /datos?season=2023&team=Boca%20Juniors&group_by=player&limit=20
```

## 🎯 Ejemplos de Consultas Comunes

### Ejemplo 1: "¿Cuáles son los jugadores que nacieron tal día?"

**Estrategia**:
```bash
# Consulta directa con limit
GET /datos?birthdate=2000-01-27&group_by=player&include_stats=true&limit=20
```

**Procesamiento**: Si `stats.total_records > 20`, usar paginación:
```bash
GET /datos?birthdate=2000-01-27&group_by=player&limit=20&page=1
GET /datos?birthdate=2000-01-27&group_by=player&limit=20&page=2
# ... hasta procesar todos
```

### Ejemplo 2: "¿Cuáles son los jugadores que jugaron en un equipo determinado en una temporada específica?"

**Estrategia**:
```bash
GET /datos?team=Boca%20Juniors&season=2023&group_by=player&include_stats=true&limit=20
```

### Ejemplo 3: "¿Si un jugador jugó en diferentes equipos en una misma temporada?"

**Estrategia en dos pasos**:

**Paso 1**: Obtener estadísticas
```bash
GET /datos?season=2023&include_stats=true&limit=1
```

**Paso 2**: Si hay muchos jugadores, procesar por posición o usar paginación
```bash
# Opción A: Por posición
GET /datos?season=2023&position=C&group_by=player&limit=20

# Opción B: Paginación
GET /datos?season=2023&group_by=player&limit=20&page=1
GET /datos?season=2023&group_by=player&limit=20&page=2
# ... continuar
```

**Procesamiento de la respuesta**: Buscar jugadores donde `len(equipos) > 1`

## 🔄 Lógica de Procesamiento para Respuestas Grandes

### Algoritmo Recomendado:

```python
def procesar_consulta_compleja(parametros_base):
    # Paso 1: Obtener estadísticas
    stats_response = GET /datos?{parametros_base}&include_stats=true&limit=1
    total_records = stats_response['stats']['total_records']
    
    # Paso 2: Determinar estrategia
    if total_records <= 30:
        # Consulta directa
        response = GET /datos?{parametros_base}&limit=total_records
        return procesar_respuesta(response)
    
    elif total_records <= 100:
        # Usar paginación
        resultados = []
        page = 1
        limit = 20
        
        while len(resultados) < total_records:
            response = GET /datos?{parametros_base}&limit={limit}&page={page}
            resultados.extend(response['data'])
            page += 1
        
        return procesar_respuesta({'data': resultados})
    
    else:
        # Usar filtros más específicos
        return usar_filtros_especificos(parametros_base)
```

## 📝 Estructura de Respuestas

### Respuesta Normal (sin include_stats):
```json
[
  {
    "nombre_ajustado": "Juan Pablo",
    "apellido_ajustado": "Cantero",
    "equipos": ["Union SF", "Comunicaciones Mercedes"],
    "temporadas": [2023],
    "posiciones": ["PG", "C"],
    "altura": 182.0,
    "peso": 83.0,
    "nacionalidad": "Argentina",
    "fecha_nacimiento": "1982-09-19"
  }
]
```

### Respuesta con Estadísticas (include_stats=true):
```json
{
  "data": [...],
  "stats": {
    "total_records": 376,
    "total_pages": 19,
    "current_page": 1,
    "records_per_page": 20,
    "filters_applied": {...},
    "data_stats": {
      "unique_players": 376,
      "unique_teams": 20,
      "unique_seasons": 1
    }
  }
}
```

## ⚠️ Reglas Importantes

1. **SIEMPRE usar `limit`** (recomendado: 10-30)
2. **NUNCA hacer consultas sin limit**
3. **Usar `include_stats=true`** en la primera consulta para entender el alcance
4. **Implementar paginación** si `total_records > limit`
5. **Usar filtros específicos** cuando sea posible
6. **Procesar en lotes** para consultas grandes

## 🎯 Casos de Uso Específicos

### Para Búsquedas por Nombre:
```bash
GET /datos?first_name=Pablo&group_by=player&limit=20
```

### Para Estadísticas de Temporada:
```bash
GET /datos?season=2023&group_by=season&include_stats=true&limit=1
```

### Para Jugadores por Equipo:
```bash
GET /datos?team=Boca%20Juniors&group_by=player&limit=20
```

### Para Análisis de Posiciones:
```bash
GET /datos?season=2023&position=C&group_by=player&limit=20
```

## 🔧 Manejo de Errores

- Si recibes error 500, verifica que los parámetros sean válidos
- Si la respuesta es muy grande, reduce el `limit` o usa filtros más específicos
- Si no hay resultados, verifica la ortografía de nombres y equipos

## 📚 Notas Importantes

- Los campos `first_name` y `last_name` usan los nombres "ajustados" (únicos)
- Las fechas deben estar en formato YYYY-MM-DD
- Los equipos pueden contener espacios (usar URL encoding)
- Las posiciones válidas son: G, F, C, PG, SG, SF, PF

Recuerda: **La clave es procesar los datos en lotes manejables y siempre usar el parámetro `limit`**. 