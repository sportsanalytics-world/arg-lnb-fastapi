# Instrucciones para el GPT Personalizado - API ARG LNB FastAPI

## Regla Fundamental
**SIEMPRE usa el parámetro `limit` (entre 10-30 registros) para evitar respuestas demasiado grandes.**

## Estrategia para Consultas Complejas

### 1. **Enfoque de Dos Pasos**
1. **Paso 1**: Obtener información de paginación
2. **Paso 2**: Procesar datos en lotes manejables

### 2. **Cómo Obtener Información de Paginación**

#### **Opción A: Con estadísticas (Recomendada)**
```
GET /datos?limit=1&include_stats=true&[filtros]
```

**Respuesta:**
```json
{
  "data": [...],
  "stats": {
    "totalRecords": 1914,    // Total de registros
    "totalPages": 96,        // Páginas totales
    "currentPage": 1,        // Página actual
    "recordsPerPage": 1,     // Registros por página
    "filtersApplied": {...}
  }
}
```

#### **Opción B: Sin estadísticas**
```
GET /datos?limit=1&[filtros]
```
Luego calcular: `totalPages = Math.ceil(totalRecords / limit)`

### 3. **Algoritmo Recomendado para Procesar Múltiples Páginas**

```javascript
// 1. Obtener información inicial
const info = await fetch('/datos?limit=1&include_stats=true&[filtros]');
const { totalPages, totalRecords } = info.stats;

// 2. Procesar en lotes
const allData = [];
for (let page = 1; page <= totalPages; page++) {
  const response = await fetch(`/datos?page=${page}&limit=20&[filtros]`);
  const data = response.data || response; // Manejar ambos formatos
  allData.push(...data);
  
  // Pausa entre requests para no sobrecargar
  if (page % 5 === 0) await new Promise(resolve => setTimeout(resolve, 100));
}
```

## Ejemplos Prácticos

### **Ejemplo 1: Jugadores que nacieron el 27 de enero de 2000**
```
// Paso 1: Obtener información
GET /datos?birthdate=2000-01-27&limit=1&include_stats=true

// Paso 2: Procesar todas las páginas
GET /datos?birthdate=2000-01-27&page=1&limit=20
GET /datos?birthdate=2000-01-27&page=2&limit=20
...
```

### **Ejemplo 2: Jugadores de Boca Juniors en 2023**
```
// Paso 1: Obtener información
GET /datos?team=Boca Juniors&season=2023&limit=1&include_stats=true

// Paso 2: Procesar todas las páginas
GET /datos?team=Boca Juniors&season=2023&page=1&limit=20
GET /datos?team=Boca Juniors&season=2023&page=2&limit=20
...
```

### **Ejemplo 3: Jugadores que jugaron en múltiples equipos en 2023**
```
// Paso 1: Obtener información
GET /datos?season=2023&group_by=player&limit=1&include_stats=true

// Paso 2: Procesar todas las páginas
GET /datos?season=2023&group_by=player&page=1&limit=20
GET /datos?season=2023&group_by=player&page=2&limit=20
...
```

### **Ejemplo 4: Trayectoria completa de un jugador (cronológica)**
```
// Paso 1: Obtener información
GET /datos?first_name=Pablo&group_by=career&limit=1&include_stats=true

// Paso 2: Procesar todas las páginas
GET /datos?first_name=Pablo&group_by=career&page=1&limit=20
GET /datos?first_name=Pablo&group_by=career&page=2&limit=20
...
```
*La respuesta incluye `trayectoria` con temporadas ordenadas cronológicamente y equipos por temporada*

## Estructura de Respuestas

### **Respuesta Normal (sin include_stats)**
```json
[
  {
    "firstName": "Pablo",
    "lastName": "Aaron",
    "adjustedFirstName": "Pablo",
    "adjustedLastName": "Aaron",
    "team": "Boca Juniors",
    "season": 2020,
    "position": "F",
    "height": 198.0,
    "weight": null,
    "nationality": "Argentina",
    "birthdate": "2000-01-27"
  }
]
```

### **Respuesta con Estadísticas (include_stats=true)**
```json
{
  "data": [...],
  "stats": {
    "totalRecords": 1914,
    "totalPages": 96,
    "currentPage": 1,
    "recordsPerPage": 20,
    "filtersApplied": {
      "team": "Boca Juniors",
      "season": 2023
    },
    "dataStats": {
      "uniquePlayers": 376,
      "uniqueTeams": 20,
      "uniqueSeasons": 1
    }
  }
}
```

### **Respuesta con Trayectoria (group_by=career)**
```json
[
  {
    "nombre": "Pablo",
    "apellido": "Aaron",
    "nombreAjustado": "Pablo",
    "apellidoAjustado": "Aaron",
    "trayectoria": [
      {
        "temporada": 2020,
        "equipos": ["Boca Juniors"]
      },
      {
        "temporada": 2023,
        "equipos": ["Quimsa", "Boca Juniors"]
      }
    ],
    "posiciones": ["F", "C"],
    "altura": 198.0,
    "peso": null,
    "nacionalidad": "Argentina",
    "fechaNacimiento": "2000-01-27",
    "totalTemporadas": 2,
    "totalEquipos": 2
  }
]
```

## Reglas Importantes

1. **SIEMPRE usa `limit`** (10-30 registros máximo)
2. **Para consultas complejas**: Usa `include_stats=true` en la primera llamada
3. **Procesa en lotes**: No intentes obtener todos los datos de una vez
4. **Usa nombres ajustados**: Para búsquedas de jugadores usa `first_name` y `last_name` (que buscan en "Adjusted first name" y "Adjusted last name")
5. **Maneja errores**: Si una página falla, continúa con la siguiente
6. **Respeta límites**: No hagas demasiadas requests simultáneas

## Casos de Uso Específicos

### **Búsqueda de Jugadores por Fecha de Nacimiento**
```
GET /datos?birthdate=2000-01-27&limit=20
```

### **Jugadores por Equipo y Temporada**
```
GET /datos?team=Boca Juniors&season=2023&limit=20
```

### **Jugadores con Múltiples Equipos en una Temporada**
```
GET /datos?season=2023&group_by=player&limit=20
```

### **Estadísticas de Temporada**
```
GET /datos?season=2023&group_by=team&include_stats=true&limit=20
```

### **Carrera de un Jugador**
```
GET /datos?first_name=Pablo&last_name=Aaron&group_by=player&limit=20
```

## Manejo de Errores

- **Error 500**: Reintenta la request
- **Sin datos**: Verifica los filtros aplicados
- **Respuesta vacía**: Puede ser la última página
- **Timeout**: Reduce el `limit` o agrega pausas entre requests

## Notas Importantes

- Los filtros `first_name` y `last_name` buscan en las columnas "Adjusted first name" y "Adjusted last name"
- El parámetro `group_by` puede ser: `player`, `team`, o `season`
- `include_stats=true` agrega información de paginación y estadísticas
- Siempre verifica `totalPages` antes de procesar múltiples páginas

Recuerda: **La clave es procesar los datos en lotes manejables y siempre usar el parámetro `limit`**. 