#!/bin/bash

# Script para crear 100 niños en la API ABB
# Uso: ./crear_100_ninos.sh

API_URL="http://localhost:8001"

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arrays de datos para generar niños
NOMBRES_MASCULINO=(
    "Juan" "Carlos" "Pedro" "Luis" "Miguel" "José" "Diego" "Andrés" "Felipe" "Santiago"
    "Sebastián" "Mateo" "Daniel" "David" "Alejandro" "Nicolás" "Samuel" "Gabriel" "Martín" "Tomás"
)

NOMBRES_FEMENINO=(
    "María" "Ana" "Laura" "Sofía" "Valentina" "Isabella" "Camila" "Daniela" "Gabriela" "Natalia"
    "Paula" "Carolina" "Andrea" "Juliana" "Catalina" "Mariana" "Lucía" "Elena" "Victoria" "Emilia"
)

APELLIDOS=(
    "García" "Rodríguez" "Martínez" "López" "González" "Pérez" "Sánchez" "Ramírez" "Torres" "Flores"
    "Rivera" "Gómez" "Díaz" "Cruz" "Morales" "Reyes" "Gutiérrez" "Ortiz" "Jiménez" "Hernández"
    "Vargas" "Castro" "Ruiz" "Álvarez" "Romero" "Mendoza" "Silva" "Rojas" "Medina" "Aguilar"
)

CIUDADES=(
    "Bogotá" "Medellín" "Cali" "Barranquilla" "Cartagena" "Cúcuta" "Bucaramanga" "Pereira"
    "Santa Marta" "Ibagué" "Pasto" "Manizales" "Neiva" "Villavicencio" "Armenia"
)

ACUDIENTES=(
    "Padre" "Madre" "Abuelo" "Abuela" "Tío" "Tía" "Tutor Legal"
)

NOTAS=(
    "Alérgico al maní"
    "Alérgico a la lactosa"
    "Requiere atención especial"
    "Usa lentes"
    "Practica deportes"
    "Toca un instrumento musical"
    "Le gusta leer"
    "Es muy activo"
    "Prefiere actividades al aire libre"
    "Ninguna observación especial"
)

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Creando 100 niños en la API ABB${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Verificar que la API esté funcionando
echo -e "${YELLOW}Verificando conexión con la API...${NC}"
if curl -s "${API_URL}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API disponible en ${API_URL}${NC}"
else
    echo -e "${RED}✗ Error: No se puede conectar a la API en ${API_URL}${NC}"
    echo -e "${RED}  Asegúrate de que el servidor esté corriendo${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Iniciando creación de niños...${NC}"
echo ""

# Contadores
CREADOS=0
ERRORES=0

# Crear 100 niños
for i in {1..100}; do
    # Generar documento único (empezando desde 1000000000)
    DOCUMENTO=$((1000000000 + i))
    
    # Determinar género (50% masculino, 50% femenino)
    if [ $((i % 2)) -eq 0 ]; then
        GENERO="Masculino"
        NOMBRE_IDX=$((RANDOM % ${#NOMBRES_MASCULINO[@]}))
        NOMBRE="${NOMBRES_MASCULINO[$NOMBRE_IDX]}"
    else
        GENERO="Femenino"
        NOMBRE_IDX=$((RANDOM % ${#NOMBRES_FEMENINO[@]}))
        NOMBRE="${NOMBRES_FEMENINO[$NOMBRE_IDX]}"
    fi
    
    # Seleccionar apellido aleatorio
    APELLIDO_IDX=$((RANDOM % ${#APELLIDOS[@]}))
    APELLIDO="${APELLIDOS[$APELLIDO_IDX]}"
    
    # Nombre completo
    NOMBRE_COMPLETO="${NOMBRE} ${APELLIDO}"
    
    # Edad aleatoria entre 5 y 18 años
    EDAD=$((5 + RANDOM % 14))
    
    # Ciudad aleatoria
    CIUDAD_IDX=$((RANDOM % ${#CIUDADES[@]}))
    CIUDAD="${CIUDADES[$CIUDAD_IDX]}"
    
    # Acudiente aleatorio
    ACUDIENTE_IDX=$((RANDOM % ${#ACUDIENTES[@]}))
    ACUDIENTE_TIPO="${ACUDIENTES[$ACUDIENTE_IDX]}"
    ACUDIENTE="${ACUDIENTE_TIPO} de ${NOMBRE}"
    
    # Notas aleatorias (50% de probabilidad de tener notas)
    if [ $((RANDOM % 2)) -eq 0 ]; then
        NOTAS_IDX=$((RANDOM % ${#NOTAS[@]}))
        NOTA="${NOTAS[$NOTAS_IDX]}"
        NOTAS_JSON="\"${NOTA}\""
    else
        NOTAS_JSON="null"
    fi
    
    # Crear JSON
    JSON_DATA=$(cat <<EOF
{
  "documento": ${DOCUMENTO},
  "nombre": "${NOMBRE_COMPLETO}",
  "edad": ${EDAD},
  "ciudad": "${CIUDAD}",
  "genero": "${GENERO}",
  "acudiente": "${ACUDIENTE}",
  "notas": ${NOTAS_JSON}
}
EOF
)
    
    # Enviar request a la API
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/children" \
        -H "Content-Type: application/json" \
        -d "${JSON_DATA}")
    
    # Extraer código de estado HTTP
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    
    # Verificar respuesta
    if [ "$HTTP_CODE" -eq 201 ]; then
        CREADOS=$((CREADOS + 1))
        echo -e "${GREEN}✓${NC} [${CREADOS}/100] ${NOMBRE_COMPLETO} (${GENERO}, ${EDAD} años, ${CIUDAD})"
    else
        ERRORES=$((ERRORES + 1))
        echo -e "${RED}✗${NC} [Error] ${NOMBRE_COMPLETO} - HTTP ${HTTP_CODE}"
    fi
    
    # Pequeña pausa para no saturar la API (opcional)
    # sleep 0.1
done

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Resumen de Creación${NC}"
echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Niños creados exitosamente: ${CREADOS}${NC}"
if [ $ERRORES -gt 0 ]; then
    echo -e "${RED}Errores: ${ERRORES}${NC}"
fi
echo ""

# Obtener estadísticas de la API
echo -e "${YELLOW}Obteniendo reporte por ciudad...${NC}"
echo ""

REPORTE=$(curl -s "${API_URL}/reports/children-by-city")

if [ $? -eq 0 ]; then
    echo "$REPORTE" | python3 -m json.tool 2>/dev/null || echo "$REPORTE"
else
    echo -e "${RED}No se pudo obtener el reporte${NC}"
fi

echo ""
echo -e "${GREEN}¡Proceso completado!${NC}"
