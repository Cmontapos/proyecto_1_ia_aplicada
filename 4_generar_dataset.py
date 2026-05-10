"""
Script para generar el conjunto de datos final
Convierte matrices 128x128 en vectores fila de 16384 elementos + etiqueta
Etiqueta: 1 = hay contaminación (arroz), 0 = no hay contaminación
Uso: python 4_generar_dataset.py
"""

import numpy as np
import os
import json
import csv
from pathlib import Path


def cargar_matrices(archivo="src/datos_matrices.npz"):
    """
    Carga las matrices guardadas
    """
    if not os.path.exists(archivo):
        print(f"Error: No se encontró '{archivo}'")
        print("Primero ejecuta '2_imagen_a_matriz.py'")
        return None, None
    
    datos = np.load(archivo)
    return datos['matrices'], datos['nombres']


def crear_vectores_fila(matrices, nombres, etiquetas=None):
    """
    Convierte matrices 128x128 en vectores fila
    
    Args:
        matrices: Array con matrices de 128x128
        nombres: Lista de nombres de archivos
        etiquetas: Dict con etiquetas {nombre_archivo: 0 o 1}
                   Si es None, pide interactivamente al usuario
    
    Returns:
        Tupla (vectores, etiquetas_finales)
    """
    vectores = []
    etiquetas_finales = []
    
    print("="*70)
    print("GENERACIÓN DE VECTORES FILA (16384 elementos + etiqueta)")
    print("="*70 + "\n")
    
    for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
        # Convertir matriz a vector fila
        vector = matriz.flatten()  # Convierte 128x128 a 16384 elementos
        vectores.append(vector)
        
        # Obtener etiqueta
        if etiquetas is None:
            # Pedir etiqueta interactivamente
            print(f"Imagen {i+1}/{len(matrices)}: {nombre}")
            print(f"  Píxeles blancos: {vector.sum()}/16384")
            print("  ¿Contiene CONTAMINACIÓN (arroz/grano)?")
            respuesta = input("  Ingresa 1 (SÍ, hay contaminación) o 0 (NO, sin contaminación): ").strip()
            
            etiqueta = 1 if respuesta == '1' else 0
        else:
            etiqueta = etiquetas.get(nombre, 0)
        
        etiquetas_finales.append(etiqueta)
        print(f"  ✓ Etiqueta: {etiqueta}\n")
    
    return np.array(vectores), np.array(etiquetas_finales)


def guardar_dataset(vectores, etiquetas, prefijo="dataset"):
    """
    Guarda el dataset en múltiples formatos
    """
    print("\n" + "="*70)
    print("GUARDANDO DATASET")
    print("="*70)
    
    # 1. NumPy comprimido (.npz)
    archivo_npz = f"src/{prefijo}_con_etiquetas.npz"
    np.savez_compressed(archivo_npz, vectores=vectores, etiquetas=etiquetas)
    print(f"✓ Guardado: {archivo_npz}")
    
    # 2. CSV (para compatibilidad con Excel, Pandas, etc.)
    archivo_csv = f"src/{prefijo}_con_etiquetas.csv"
    with open(archivo_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        # Encabezado con nombres de columnas
        encabezado = [f"pixel_{i}" for i in range(vectores.shape[1])] + ["etiqueta"]
        writer.writerow(encabezado)
        # Datos
        for vector, etiqueta in zip(vectores, etiquetas):
            fila = list(vector) + [etiqueta]
            writer.writerow(fila)
    print(f"✓ Guardado: {archivo_csv}")
    
    # 3. JSON (para inspección)
    datos_json = {
        "numero_imágenes": len(vectores),
        "tamaño_cada_vector": vectores.shape[1],
        "total_etiquetas": int(etiquetas.sum()),
        "clases": {
            "sin_contaminacion": int((etiquetas == 0).sum()),
            "con_contaminacion": int((etiquetas == 1).sum())
        }
    }
    
    archivo_json = f"{prefijo}_info.json"
    with open(archivo_json, 'w') as f:
        json.dump(datos_json, f, indent=2)
    print(f"✓ Guardado: {archivo_json}")
    
    print("\n" + "="*70)
    print("INFORMACIÓN DEL DATASET")
    print("="*70)
    print(f"Total de imágenes: {len(vectores)}")
    print(f"Elementos por vector: {vectores.shape[1]} (128×128)")
    print(f"Imágenes CON contaminación: {int(etiquetas.sum())} ({int(etiquetas.sum())/len(vectores)*100:.1f}%)")
    print(f"Imágenes SIN contaminación: {int((etiquetas==0).sum())} ({int((etiquetas==0).sum())/len(vectores)*100:.1f}%)")
    print("="*70 + "\n")


def cargar_dataset(archivo="src/dataset_con_etiquetas.npz"):
    """
    Carga un dataset guardado previamente
    """
    if not os.path.exists(archivo):
        print(f"Error: No se encontró '{archivo}'")
        return None, None
    
    datos = np.load(archivo)
    return datos['vectores'], datos['etiquetas']


def mostrar_muestra_dataset():
    """
    Muestra una muestra del dataset en formato tabla
    """
    vectores, etiquetas = cargar_dataset()
    
    if vectores is None:
        return
    
    print("\n" + "="*70)
    print("MUESTRA DEL DATASET (primeras 5 imágenes)")
    print("="*70 + "\n")
    
    for i in range(min(5, len(vectores))):
        vector = vectores[i]
        etiqueta = etiquetas[i]
        
        print(f"Imagen {i+1}:")
        print(f"  Vector: [{vector[0]}, {vector[1]}, {vector[2]}, ..., {vector[-2]}, {vector[-1]}]")
        print(f"  Etiqueta: {etiqueta} {'(CON contaminación)' if etiqueta == 1 else '(SIN contaminación)'}")
        print(f"  Píxeles blancos: {int(vector.sum())}/16384\n")


def crear_archivo_etiquetas_interactivo():
    """
    Crea un archivo JSON con las etiquetas de forma interactiva
    """
    archivo_matrices = "src/datos_matrices.npz"
    
    if not os.path.exists(archivo_matrices):
        print(f"Error: No se encontró '{archivo_matrices}'")
        return
    
    datos = np.load(archivo_matrices)
    nombres = datos['nombres']
    
    etiquetas = {}
    
    print("="*70)
    print("CREACIÓN DE ARCHIVO DE ETIQUETAS")
    print("="*70 + "\n")
    
    for i, nombre in enumerate(nombres):
        print(f"Imagen {i+1}/{len(nombres)}: {nombre}")
        print("  ¿Contiene CONTAMINACIÓN (arroz/grano)?")
        respuesta = input("  (1=SÍ / 0=NO): ").strip()
        
        etiquetas[nombre] = 1 if respuesta == '1' else 0
        print()
    
    # Guardar etiquetas
    archivo_etiquetas = "src/etiquetas.json"
    with open(archivo_etiquetas, 'w') as f:
        json.dump(etiquetas, f, indent=2)
    
    print(f"✓ Etiquetas guardadas en: {archivo_etiquetas}")
    
    return etiquetas


def menu_principal():
    """
    Menú principal para el usuario
    """
    while True:
        print("\n" + "="*70)
        print("GENERACIÓN DE DATASET PARA DETECCIÓN DE CONTAMINACIÓN")
        print("="*70)
        print("\nOpciones:")
        print("  1 - Crear etiquetas interactivamente (archivo JSON)")
        print("  2 - Generar vectores y dataset con etiquetas")
        print("  3 - Mostrar muestra del dataset")
        print("  4 - Ver información del dataset")
        print("  5 - Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            crear_archivo_etiquetas_interactivo()
        
        elif opcion == '2':
            # Cargar matrices
            matrices, nombres = cargar_matrices()
            if matrices is None:
                continue
            
            # Intentar cargar etiquetas de archivo
            etiquetas = None
            if os.path.exists("etiquetas.json"):
                with open("etiquetas.json") as f:
                    etiquetas = json.load(f)
                print("✓ Etiquetas cargadas desde archivo")
            
            # Crear vectores
            vectores, etiquetas_finales = crear_vectores_fila(matrices, nombres, etiquetas)
            
            # Guardar dataset
            guardar_dataset(vectores, etiquetas_finales)
        
        elif opcion == '3':
            mostrar_muestra_dataset()
        
        elif opcion == '4':
            vectores, etiquetas = cargar_dataset()
            if vectores is not None:
                print("\n" + "="*70)
                print("INFORMACIÓN DEL DATASET")
                print("="*70)
                print(f"Total de imágenes: {len(vectores)}")
                print(f"Elementos por vector: {vectores.shape[1]}")
                print(f"CON contaminación: {int(etiquetas.sum())} ({int(etiquetas.sum())/len(vectores)*100:.1f}%)")
                print(f"SIN contaminación: {int((etiquetas==0).sum())} ({int((etiquetas==0).sum())/len(vectores)*100:.1f}%)")
                print("="*70)
        
        elif opcion == '5':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--info':
            vectores, etiquetas = cargar_dataset()
            if vectores is not None:
                print(f"Imágenes: {len(vectores)}")
                print(f"Con contaminación: {int(etiquetas.sum())}")
                print(f"Sin contaminación: {int((etiquetas==0).sum())}")
        elif sys.argv[1] == '--muestra':
            mostrar_muestra_dataset()
        else:
            print("Uso: python 4_generar_dataset.py [--info|--muestra]")
    else:
        menu_principal()
