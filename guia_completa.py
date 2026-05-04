#!/usr/bin/env python3
"""
GUÍA COMPLETA: Pipeline de Preprocesamiento para Detección de Contaminación
===============================================================================

Este script guía el flujo completo:
1. Preprocesamiento de imágenes (blanco y negro, 128x128)
2. Conversión a matrices binarias (1s y 0s)
3. Visualización de matrices
4. Generación de dataset con etiquetas
5. Exportación de datos

Requisitos:
  pip install opencv-python numpy

Uso:
  python guia_completa.py

Estructura de carpetas esperada:
  ./
  ├── originales/          ← Coloca aquí tus imágenes
  ├── procesadas/          ← Se generan automáticamente
  ├── guia_completa.py
  ├── 1_preprocesar_imagenes.py
  ├── 2_imagen_a_matriz.py
  ├── 3_visualizar_matrices.py
  └── 4_generar_dataset.py
"""

import os
import subprocess
import sys
from pathlib import Path


def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_encabezado(titulo):
    """Muestra un encabezado formateado"""
    print("\n" + "="*70)
    print(titulo.center(70))
    print("="*70 + "\n")


def verificar_dependencias():
    """Verifica que están instaladas las dependencias necesarias"""
    print("Verificando dependencias...")
    
    try:
        import cv2
        print("✓ OpenCV instalado")
    except ImportError:
        print("✗ OpenCV no encontrado")
        print("  Instala con: pip install opencv-python")
        return False
    
    try:
        import numpy
        print("✓ NumPy instalado")
    except ImportError:
        print("✗ NumPy no encontrado")
        print("  Instala con: pip install numpy")
        return False
    
    return True


def crear_estructura_carpetas():
    """Crea la estructura de carpetas necesaria"""
    carpetas = ["imagenes_originales", "imagenes_procesadas"]
    
    for carpeta in carpetas:
        Path(carpeta).mkdir(exist_ok=True)
        print(f"✓ Carpeta '{carpeta}' lista")


def paso_1_preprocesamiento():
    """Ejecuta el preprocesamiento de imágenes"""
    mostrar_encabezado("PASO 1: PREPROCESAMIENTO DE IMÁGENES")
    
    print("Este paso:")
    print("  • Convierte imágenes a escala de grises")
    print("  • Redimensiona a 128×128 píxeles")
    print("  • Guarda las imágenes procesadas\n")
    
    # Verificar que hay imágenes
    archivos = list(Path("imagenes_originales").glob("*.[jp][pn]g"))
    archivos.extend(Path("imagenes_originales").glob("*.bmp"))
    archivos.extend(Path("imagenes_originales").glob("*.tiff"))
    
    if not archivos:
        print("⚠ No hay imágenes en 'imagenes_originales/'")
        print("Por favor, coloca tus imágenes y vuelve a ejecutar.\n")
        return False
    
    print(f"Encontradas {len(archivos)} imagen(es)\n")
    
    # Ejecutar preprocesamiento
    try:
        subprocess.run([sys.executable, "1_preprocesar_imagenes.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("✗ Error en el preprocesamiento")
        return False


def paso_2_matriz_binaria():
    """Convierte imágenes a matrices binarias"""
    mostrar_encabezado("PASO 2: CONVERSIÓN A MATRICES BINARIAS")
    
    print("Este paso:")
    print("  • Lee las imágenes 128×128 procesadas")
    print("  • Convierte a matriz binaria (1s y 0s)")
    print("  • Guarda en archivo comprimido (.npz)\n")
    
    # Verificar que hay imágenes procesadas
    archivos = list(Path("imagenes_procesadas").glob("*.png"))
    
    if not archivos:
        print("⚠ No hay imágenes procesadas")
        print("Primero ejecuta el PASO 1\n")
        return False
    
    print(f"Encontradas {len(archivos)} imagen(es) procesada(s)\n")
    
    try:
        subprocess.run([sys.executable, "2_imagen_a_matriz.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("✗ Error en conversión a matrices")
        return False


def paso_3_visualizar():
    """Visualiza las matrices"""
    mostrar_encabezado("PASO 3: VISUALIZACIÓN DE MATRICES")
    
    print("Este paso permite:")
    print("  • Ver las matrices en la terminal")
    print("  • Visualización completa o comprimida")
    print("  • Ver estadísticas de cada matriz\n")
    
    if not Path("datos_matrices.npz").exists():
        print("⚠ No existe 'datos_matrices.npz'")
        print("Primero ejecuta el PASO 2\n")
        return
    
    try:
        subprocess.run([sys.executable, "3_visualizar_matrices.py"])
    except KeyboardInterrupt:
        print("\nVisualización cancelada")


def paso_4_dataset():
    """Genera el dataset final"""
    mostrar_encabezado("PASO 4: GENERACIÓN DE DATASET")
    
    print("Este paso:")
    print("  • Convierte matrices a vectores fila (16384 elementos)")
    print("  • Añade etiquetas (1=con contaminación, 0=sin contaminación)")
    print("  • Genera dataset en múltiples formatos (.npz, .csv, .json)\n")
    
    if not Path("datos_matrices.npz").exists():
        print("⚠ No existe 'datos_matrices.npz'")
        print("Primero ejecuta el PASO 2\n")
        return False
    
    try:
        subprocess.run([sys.executable, "4_generar_dataset.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("✗ Error en generación de dataset")
        return False


def mostrar_flujo_automatico():
    """Ejecuta el flujo completo de forma automática"""
    mostrar_encabezado("EJECUCIÓN AUTOMÁTICA DEL PIPELINE COMPLETO")
    
    pasos = [
        ("Preprocesamiento", paso_1_preprocesamiento),
        ("Conversión a matrices", paso_2_matriz_binaria),
        ("Generación de dataset", paso_4_dataset),
    ]
    
    for nombre, funcion in pasos:
        if funcion():
            print(f"✓ {nombre} completado\n")
            input("Presiona Enter para continuar...")
        else:
            print(f"✗ {nombre} falló\n")
            return False
    
    mostrar_encabezado("PIPELINE COMPLETADO")
    print("Archivos generados:")
    print("  • imagenes_procesadas/         - Imágenes 128×128 en B&N")
    print("  • datos_matrices.npz           - Matrices binarias")
    print("  • dataset_con_etiquetas.npz    - Vectores + etiquetas (.npz)")
    print("  • dataset_con_etiquetas.csv    - Vectores + etiquetas (.csv)")
    print("  • dataset_info.json            - Información del dataset")
    print("  • etiquetas.json               - Archivo de etiquetas\n")
    
    return True


def menu_principal():
    """Menú principal interactivo"""
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("PIPELINE DE PREPROCESAMIENTO DE IMÁGENES")
        
        print("Selecciona qué deseas hacer:")
        print("\n  1 - Ejecutar todo el pipeline automáticamente")
        print("  2 - Paso 1: Preprocesamiento de imágenes")
        print("  3 - Paso 2: Conversión a matrices binarias")
        print("  4 - Paso 3: Visualizar matrices")
        print("  5 - Paso 4: Generar dataset")
        print("  6 - Crear estructura de carpetas")
        print("  7 - Verificar dependencias")
        print("  8 - Salir")
        
        opcion = input("\nSelecciona (1-8): ").strip()
        
        if opcion == '1':
            if mostrar_flujo_automatico():
                input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '2':
            paso_1_preprocesamiento()
            input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '3':
            if paso_2_matriz_binaria():
                input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '4':
            paso_3_visualizar()
            input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '5':
            if paso_4_dataset():
                input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '6':
            limpiar_pantalla()
            mostrar_encabezado("CREAR ESTRUCTURA DE CARPETAS")
            crear_estructura_carpetas()
            print("\n✓ Estructura de carpetas creada")
            input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '7':
            limpiar_pantalla()
            mostrar_encabezado("VERIFICAR DEPENDENCIAS")
            if verificar_dependencias():
                print("\n✓ Todas las dependencias están instaladas")
            else:
                print("\n✗ Falta instalar algunas dependencias")
            input("\nPresiona Enter para volver al menú...")
        
        elif opcion == '8':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")


if __name__ == "__main__":
    try:
        # Verificar dependencias
        if not verificar_dependencias():
            print("\nPor favor, instala las dependencias antes de continuar.")
            sys.exit(1)
        
        # Crear estructura de carpetas
        crear_estructura_carpetas()
        
        # Mostrar menú
        menu_principal()
    
    except KeyboardInterrupt:
        print("\n\nEjecución cancelada por el usuario")
        sys.exit(0)
