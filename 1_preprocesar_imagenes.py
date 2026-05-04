"""
Script para preprocesar imágenes: convertir a blanco y negro y redimensionar a 128x128
Uso: python 1_preprocesar_imagenes.py
"""

import cv2
import os
from pathlib import Path

def preprocesar_imagen(ruta_imagen, tamaño=(128, 128)):
    """
    Convierte una imagen a escala de grises y la redimensiona a 128x128
    
    Args:
        ruta_imagen: Ruta a la imagen a procesar
        tamaño: Tupla con las dimensiones deseadas (default: 128x128)
    
    Returns:
        Imagen procesada en escala de grises, o None si hay error
    """
    try:
        # Leer la imagen
        imagen = cv2.imread(ruta_imagen)
        
        if imagen is None:
            print(f"Error: No se pudo leer la imagen: {ruta_imagen}")
            return None
        
        # Convertir a escala de grises
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        # Redimensionar a 128x128
        imagen_redimensionada = cv2.resize(imagen_gris, tamaño)
        
        return imagen_redimensionada
    
    except Exception as e:
        print(f"Error procesando {ruta_imagen}: {e}")
        return None


def procesar_carpeta(ruta_carpeta_entrada, ruta_carpeta_salida):
    """
    Procesa todas las imágenes de una carpeta
    
    Args:
        ruta_carpeta_entrada: Carpeta con las imágenes originales
        ruta_carpeta_salida: Carpeta donde guardar las imágenes procesadas
    """
    # Crear carpeta de salida si no existe
    os.makedirs(ruta_carpeta_salida, exist_ok=True)
    
    # Extensiones de imagen válidas
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    # Contar imágenes procesadas
    contador = 0
    
    # Procesar cada imagen en la carpeta
    for archivo in os.listdir(ruta_carpeta_entrada):
        if archivo.lower().endswith(extensiones):
            ruta_completa = os.path.join(ruta_carpeta_entrada, archivo)
            print(f"Procesando: {archivo}...", end=" ")
            
            # Preprocesar imagen
            imagen_procesada = preprocesar_imagen(ruta_completa)
            
            if imagen_procesada is not None:
                # Guardar imagen procesada
                nombre_salida = Path(archivo).stem + "_128x128.png"
                ruta_salida = os.path.join(ruta_carpeta_salida, nombre_salida)
                cv2.imwrite(ruta_salida, imagen_procesada)
                print("✓ Guardado")
                contador += 1
            else:
                print("✗ Error")
    
    print(f"\n{'='*50}")
    print(f"Procesamiento completado: {contador} imágenes guardadas")
    print(f"Ubicación de salida: {ruta_carpeta_salida}")
    print(f"{'='*50}")


if __name__ == "__main__":
    # CONFIGURAR ESTAS RUTAS SEGÚN TUS CARPETAS
    carpeta_entrada = "originales"  # Carpeta con tus imágenes
    carpeta_salida = "procesadas"   # Carpeta donde se guardarán
    
    # Crear carpeta de entrada de ejemplo si no existe
    os.makedirs(carpeta_entrada, exist_ok=True)
    
    print("="*50)
    print("PREPROCESAMIENTO DE IMÁGENES")
    print("="*50)
    print(f"Carpeta entrada: {carpeta_entrada}")
    print(f"Carpeta salida: {carpeta_salida}")
    print(f"Tamaño final: 128x128 píxeles")
    print("="*50)
    
    # Verificar si hay imágenes en la carpeta
    archivos = [f for f in os.listdir(carpeta_entrada) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
    
    if not archivos:
        print(f"⚠ No se encontraron imágenes en '{carpeta_entrada}'")
        print("Por favor, coloca tus imágenes en esa carpeta y vuelve a ejecutar.")
    else:
        print(f"Encontradas {len(archivos)} imagen(es)\n")
        procesar_carpeta(carpeta_entrada, carpeta_salida)
