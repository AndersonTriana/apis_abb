# APIs de Gestión de Niños - ABB y AVL

Este proyecto contiene dos APIs REST para gestión de niños usando diferentes estructuras de datos:
- **API ABB**: Árbol Binario de Búsqueda (Puerto 8001)
- **API AVL**: Árbol AVL Auto-balanceado (Puerto 8000)

## 📋 Requisitos Previos

- Python 3.13+
- pip

## 🚀 Instalación y Ejecución

### API ABB (Puerto 8001)

```bash
# 1. Crear entorno virtual (si no existe)
cd api_abb
python3 -m venv .venv

# 2. Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar servidor
cd ..
api_abb/.venv/bin/python -m uvicorn api_abb.main:app --reload --host 0.0.0.0 --port 8001 --app-dir api_abb/src

# 5. Acceder a la documentación
# http://localhost:8001/docs
```

### API AVL (Puerto 8000)

```bash
# 1. Crear entorno virtual (si no existe)
cd api_avl
python3 -m venv .venv

# 2. Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar servidor
cd ..
api_avl/.venv/bin/python -m uvicorn api_avl.main:app --reload --host 0.0.0.0 --port 8000 --app-dir api_avl/src

# 5. Acceder a la documentación
# http://localhost:8000/docs
```

## 🧪 Ejecutar Tests

### Tests ABB
```bash
cd api_abb
PYTHONPATH=src .venv/bin/python -m pytest tests/ -v
```

### Tests AVL
```bash
cd api_avl
PYTHONPATH=src .venv/bin/python -m pytest tests/ -v
```

## 🐛 Ejecutar con VS Code (Debugger)

1. Abre el proyecto en VS Code
2. Ve a la pestaña "Run and Debug" (Ctrl+Shift+D)
3. Selecciona la configuración:
   - **FastAPI (Uvicorn) - api_abb** para ABB
   - **FastAPI (Uvicorn) - api_avl** para AVL
4. Presiona F5 o click en "Start Debugging"

## 📮 Colecciones de Postman

- **ABB**: `api_abb/postman/API_Arbol_ABB_Ninos.postman_collection.json`
- **AVL**: `api_avl/API_Arbol_AVL_Ninos.postman_collection.json`

Importa las colecciones en Postman para probar los endpoints.

## 📊 Arquitectura

Ambas APIs siguen la misma arquitectura en capas:

```
API Routes → Controller → Service → Model (ABB/AVL Tree)
```

## 🔗 Endpoints Principales

### ABB (http://localhost:8001)
- `POST /children` - Crear niño
- `GET /children?order={in|pre|post}` - Listar niños
- `GET /children/{documento}` - Obtener niño
- `PUT /children/{documento}` - Actualizar niño
- `DELETE /children/{documento}` - Eliminar niño
- `GET /health` - Health check

### AVL (http://localhost:8000)
- `POST /children/` - Crear niño
- `GET /children/?order={in|pre|post}` - Listar niños
- `GET /children/{document}` - Obtener niño
- `PUT /children/{document}` - Actualizar niño
- `DELETE /children/{document}` - Eliminar niño
- `GET /children/tree/info` - Info del árbol
- `GET /health` - Health check

## 📝 Notas

- **ABB**: Documento puede ser cualquier entero positivo
- **AVL**: Documento máximo de 6 dígitos (999999)
- Los datos se almacenan en memoria (se pierden al reiniciar)
- Ambas APIs pueden ejecutarse simultáneamente en diferentes puertos
