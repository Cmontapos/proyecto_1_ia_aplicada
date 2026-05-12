"""
Script para convertir imágenes a matriz de 1s y 0s
- 1 = píxel blanco
- 0 = píxel con objeto (arroz u otro)
Uso: python 2_imagen_a_matriz.py
"""

import cv2
import numpy as np
import os
from pathlib import Path
import json

def imagen_a_matriz(ruta_imagen, umbral=130):
    """
    Convierte una imagen en escala de grises a una matriz binaria
    
    Args:
        ruta_imagen: Ruta a la imagen de 128x128
        umbral: Valor de umbral para binarización (0-255)
                Píxeles > umbral serán 1 (blanco)
                Píxeles <= umbral serán 0 (objeto)
    
    Returns:
        Matriz binaria (128x128) o None si hay error
    """
    try:
        # Leer la imagen
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        
        if imagen is None:
            print(f"Error: No se pudo leer la imagen: {ruta_imagen}")
            return None
        
        # Verificar que sea 128x128
        if imagen.shape != (128, 128):
            print(f"Advertencia: Imagen no es 128x128, es {imagen.shape}")
        
        # Binarizar: 1 si píxel > umbral (blanco), 0 si <= umbral (objeto)
        matriz_binaria = (imagen > umbral).astype(int)
        
        return matriz_binaria
    
    except Exception as e:
        print(f"Error procesando {ruta_imagen}: {e}")
        return None


def procesar_carpeta_a_matrices(ruta_carpeta_entrada, ruta_archivo_salida):
    """
    Procesa todas las imágenes de una carpeta y genera una matriz de datos
    
    Args:
        ruta_carpeta_entrada: Carpeta con las imágenes de 128x128
        ruta_archivo_salida: Archivo donde guardar los datos (.npy o .csv)
    """
    print("="*60)
    print("CONVERSIÓN DE IMÁGENES A MATRICES BINARIAS")
    print("="*60)
    
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    matrices = []
    nombres_archivos = []
    
    # Procesar cada imagen
    for archivo in sorted(os.listdir(ruta_carpeta_entrada)):
        if archivo.lower().endswith(extensiones):
            ruta_completa = os.path.join(ruta_carpeta_entrada, archivo)
            print(f"Procesando: {archivo}...", end=" ")
            
            matriz = imagen_a_matriz(ruta_completa)
            
            if matriz is not None:
                matrices.append(matriz)
                nombres_archivos.append(archivo)
                print("✓ Convertida")
            else:
                print("✗ Error")
    
    if not matrices:
        print("No se procesaron imágenes.")
        return
    
    # Guardar en formato NumPy (.npy) - Más eficiente
    print(f"\nGuardando {len(matrices)} matriz(ces)...")
    
    # Crear estructura de datos
    datos = {
        'matrices': np.array(matrices),
        'nombres': nombres_archivos
    }
    
    # Guardar como .npz (comprimido)
    archivo_npz = ruta_archivo_salida.replace('.npy', '.npz')
    np.savez_compressed(archivo_npz, **datos)
    print(f"✓ Guardado: {archivo_npz}")
    
    print(f"\n{'='*60}")
    print(f"Estadísticas:")
    print(f"- Total de imágenes procesadas: {len(matrices)}")
    print(f"- Dimensiones de cada matriz: 128x128")
    print(f"- Total de píxeles por imagen: {128*128}")
    print(f"{'='*60}\n")
    
    return matrices, nombres_archivos


def cargar_matrices(ruta_archivo):
    """
    Carga las matrices guardadas previamente
    
    Args:
        ruta_archivo: Ruta al archivo .npz
    
    Returns:
        Tupla (matrices, nombres_archivos)
    """
    datos = np.load(ruta_archivo)
    return datos['matrices'], datos['nombres']


if __name__ == "__main__":
    # CONFIGURAR ESTAS RUTAS
    carpeta_entrada = "procesadas"  # Carpeta con imágenes 128x128
    archivo_salida = "src/datos_matrices.npz"    # Archivo para guardar matrices
    
    print("Ubicaciones:")
    print(f"- Entrada: {carpeta_entrada}")
    print(f"- Salida: {archivo_salida}\n")
    
    # Procesar carpeta
    matrices, nombres = procesar_carpeta_a_matrices(carpeta_entrada, archivo_salida)
    
    if matrices:
        # Mostrar información de la primera matriz
        print("\nInformación de la primera matriz:")
        print(f"Forma: {matrices[0].shape}")
        print(f"Valores únicos: {np.unique(matrices[0])}")
        print(f"Porcentaje de 1s (blancos): {(matrices[0].sum() / (128*128) * 100):.2f}%")
        print(f"Porcentaje de 0s (objetos): {(100 - matrices[0].sum() / (128*128) * 100):.2f}%")
