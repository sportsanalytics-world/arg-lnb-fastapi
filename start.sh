#!/bin/bash
# Script de inicio para Render
# Este script se ejecuta cuando Render inicia el servicio

echo "🚀 Iniciando API CSV desde Google Drive..."
echo "📊 Puerto: $PORT"
echo "🐍 Python version: $(python --version)"

# Ejecutar la aplicación
exec uvicorn main:app --host 0.0.0.0 --port $PORT 