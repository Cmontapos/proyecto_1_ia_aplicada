"""
4_generar_dataset.py - MEJORADO
Lee automáticamente si es limpia o sucia del nombre del archivo
"""

import numpy as np
import os
import json
import csv
from pathlib import Path


def cargar_matrices(archivo="src/datos_matrices.npz"):
    """Carga las matrices guardadas"""
    if not os.path.exists(archivo):
        print(f"Error: No se encontró '{archivo}'")
        print("Primero ejecuta '2_imagen_a_matriz.py'")
        return None, None
    
    datos = np.load(archivo)
    return datos['matrices'], datos['nombres']


def extraer_etiqueta_del_nombre(nombre_archivo):
    """
    Extrae etiqueta del nombre del archivo
    imagen_1_limpia.png → 0
    imagen_2_sucia.png → 1
    """
    nombre_lower = nombre_archivo.lower()
    
    if 'limpia' in nombre_lower:
        return 0
    elif 'sucia' in nombre_lower:
        return 1
    else:
        # Si no tiene palabra clave, pedir manualmente
        print(f"⚠ '{nombre_archivo}' - No tiene clasificación en nombre")
        print("  ¿Es limpia o sucia? (0=limpia / 1=sucia): ", end="")
        try:
            return int(input().strip())
        except:
            return 0  # Por defecto limpia


def crear_vectores_fila(matrices, nombres):
    """Convierte matrices en vectores fila y extrae etiquetas del nombre"""
    vectores = []
    etiquetas_finales = []
    
    print("\n" + "="*70)
    print("GENERACIÓN DE VECTORES FILA (16384 elementos + etiqueta)")
    print("="*70 + "\n")
    
    for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
        # Convertir matriz a vector fila
        vector = matriz.flatten()
        vectores.append(vector)
        
        # Extraer etiqueta del nombre
        etiqueta = extraer_etiqueta_del_nombre(nombre)
        etiquetas_finales.append(etiqueta)
        
        clasificacion = "SUCIA (contaminada)" if etiqueta == 1 else "LIMPIA"
        print(f"{i+1}. {nombre}")
        print(f"   ✓ Clasificación: {clasificacion}\n")
    
    return np.array(vectores), np.array(etiquetas_finales)


def guardar_dataset(vectores, etiquetas, prefijo="src/dataset"):
    """Guarda el dataset en múltiples formatos"""
    print("\n" + "="*70)
    print("GUARDANDO DATASET")
    print("="*70)
    
    # 1. NumPy comprimido (.npz)
    archivo_npz = f"{prefijo}_con_etiquetas.npz"
    np.savez_compressed(archivo_npz, vectores=vectores, etiquetas=etiquetas)
    print(f"✓ Guardado: {archivo_npz}")
    
    # 2. CSV (para compatibilidad con Excel, Pandas, etc.)
    archivo_csv = f"{prefijo}_con_etiquetas.csv"
    with open(archivo_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        encabezado = [f"pixel_{i}" for i in range(vectores.shape[1])] + ["etiqueta"]
        writer.writerow(encabezado)
        for vector, etiqueta in zip(vectores, etiquetas):
            fila = list(vector) + [etiqueta]
            writer.writerow(fila)
    print(f"✓ Guardado: {archivo_csv}")
    
    # 3. JSON (para inspección)
    datos_json = {
        "numero_imágenes": len(vectores),
        "tamaño_cada_vector": vectores.shape[1],
        "total_limpias": int((etiquetas == 0).sum()),
        "total_sucias": int((etiquetas == 1).sum()),
        "clases": {
            "limpia": int((etiquetas == 0).sum()),
            "sucia": int((etiquetas == 1).sum())
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
    print(f"Imágenes LIMPIAS: {int((etiquetas==0).sum())} ({int((etiquetas==0).sum())/len(vectores)*100:.1f}%)")
    print(f"Imágenes SUCIAS: {int((etiquetas==1).sum())} ({int((etiquetas==1).sum())/len(vectores)*100:.1f}%)")
    print("="*70 + "\n")


def cargar_dataset(archivo="src/dataset_con_etiquetas.npz"):
    """Carga un dataset guardado previamente"""
    if not os.path.exists(archivo):
        print(f"Error: No se encontró '{archivo}'")
        return None, None
    
    datos = np.load(archivo)
    return datos['vectores'], datos['etiquetas']


def mostrar_muestra_dataset():
    """Muestra una muestra del dataset en formato tabla"""
    vectores, etiquetas = cargar_dataset()
    
    if vectores is None:
        return
    
    print("\n" + "="*70)
    print("MUESTRA DEL DATASET (primeras 5 imágenes)")
    print("="*70 + "\n")
    
    for i in range(min(5, len(vectores))):
        vector = vectores[i]
        etiqueta = etiquetas[i]
        clasificacion = "SUCIA" if etiqueta == 1 else "LIMPIA"
        
        print(f"Imagen {i+1}:")
        print(f"  Vector: [{vector[0]}, {vector[1]}, {vector[2]}, ..., {vector[-2]}, {vector[-1]}]")
        print(f"  Etiqueta: {etiqueta} ({clasificacion})")
        print(f"  Píxeles blancos: {int(vector.sum())}/16384\n")


def menu_principal():
    """Menú principal para el usuario"""
    while True:
        print("\n" + "="*70)
        print("GENERACIÓN DE DATASET (CON CLASIFICACIÓN AUTOMÁTICA)")
        print("="*70)
        print("\nOpciones:")
        print("  1 - Generar vectores y dataset (CLASIFICACIÓN AUTOMÁTICA DEL NOMBRE)")
        print("  2 - Mostrar muestra del dataset")
        print("  3 - Ver información del dataset")
        print("  4 - Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            # Cargar matrices
            matrices, nombres = cargar_matrices()
            if matrices is None:
                continue
            
            # Crear vectores (clasificación automática)
            vectores, etiquetas_finales = crear_vectores_fila(matrices, nombres)
            
            # Guardar dataset
            guardar_dataset(vectores, etiquetas_finales)
        
        elif opcion == '2':
            mostrar_muestra_dataset()
        
        elif opcion == '3':
            vectores, etiquetas = cargar_dataset()
            if vectores is not None:
                print("\n" + "="*70)
                print("INFORMACIÓN DEL DATASET")
                print("="*70)
                print(f"Total de imágenes: {len(vectores)}")
                print(f"Elementos por vector: {vectores.shape[1]}")
                print(f"Imágenes LIMPIAS: {int((etiquetas==0).sum())} ({int((etiquetas==0).sum())/len(vectores)*100:.1f}%)")
                print(f"Imágenes SUCIAS: {int((etiquetas==1).sum())} ({int((etiquetas==1).sum())/len(vectores)*100:.1f}%)")
                print("="*70)
        
        elif opcion == '4':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")


if __name__ == "__main__":
    menu_principal()