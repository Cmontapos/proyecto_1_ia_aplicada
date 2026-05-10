"""
Script para visualizar matrices 128x128 en la terminal
Muestra las matrices con símbolos visuales: █ para 1 (blanco), · para 0 (objeto)
Uso: python 3_visualizar_matrices.py
"""

import numpy as np
import os
from pathlib import Path

def imprimir_matriz_terminal(matriz, nombre="", usar_simbolos=True):
    """
    Imprime una matriz en la terminal con representación visual
    
    Args:
        matriz: Array NumPy de 128x128 con valores 0 y 1
        nombre: Nombre de la imagen (opcional)
        usar_simbolos: Si True usa █ y ·, si False usa 1 y 0
    """
    if usar_simbolos:
        # Símbolo para 1 (blanco): █
        # Símbolo para 0 (objeto): ·
        simbolo_1 = "█"
        simbolo_0 = "·"
    else:
        simbolo_1 = "1"
        simbolo_0 = "0"
    
    # Encabezado
    if nombre:
        print(f"\n{'='*65}")
        print(f"Matriz: {nombre}")
        print(f"{'='*65}")
    
    # Imprimir matriz
    for fila in matriz:
        linea = ""
        for valor in fila:
            linea += simbolo_1 if valor == 1 else simbolo_0
        print(linea)
    
    print()


def imprimir_matriz_comprimida(matriz, nombre="", escala=2):
    """
    Imprime una matriz de forma comprimida, cada N píxeles se representa como 1 símbolo
    Útil para ver la estructura general sin saturar la terminal
    
    Args:
        matriz: Array NumPy de 128x128
        nombre: Nombre de la imagen
        escala: Factor de compresión (ej: 2 = cada 2x2 píxeles = 1 símbolo)
    """
    if nombre:
        print(f"\n{'='*65}")
        print(f"Matriz Comprimida (escala {escala}x): {nombre}")
        print(f"{'='*65}")
    
    # Redimensionar matriz para compresión
    nueva_altura = matriz.shape[0] // escala
    nueva_ancho = matriz.shape[1] // escala
    
    matriz_comprimida = np.zeros((nueva_altura, nueva_ancho))
    
    for i in range(nueva_altura):
        for j in range(nueva_ancho):
            # Tomar el promedio del bloque
            bloque = matriz[i*escala:(i+1)*escala, j*escala:(j+1)*escala]
            matriz_comprimida[i, j] = 1 if bloque.mean() > 0.5 else 0
    
    # Imprimir
    for fila in matriz_comprimida.astype(int):
        print("".join(["█" if v == 1 else "·" for v in fila]))
    
    print()


def imprimir_estadisticas(matriz, nombre=""):
    """
    Imprime estadísticas de la matriz
    
    Args:
        matriz: Array NumPy
        nombre: Nombre de la imagen
    """
    total_pixeles = matriz.size
    pixeles_blancos = matriz.sum()
    pixeles_objetos = total_pixeles - pixeles_blancos
    
    porcentaje_blancos = (pixeles_blancos / total_pixeles) * 100
    porcentaje_objetos = (pixeles_objetos / total_pixeles) * 100
    
    print(f"\nEstadísticas de {nombre}:")
    print(f"  Total de píxeles: {total_pixeles}")
    print(f"  Píxeles blancos (1): {pixeles_blancos} ({porcentaje_blancos:.2f}%)")
    print(f"  Píxeles con objetos (0): {pixeles_objetos} ({porcentaje_objetos:.2f}%)")
    print(f"  Relación blanco/objeto: {pixeles_blancos/max(pixeles_objetos, 1):.2f}:1")


def cargar_y_visualizar():
    """
    Carga las matrices del archivo .npz y permite visualizarlas interactivamente
    """
    archivo = "src/datos_matrices.npz"
    
    if not os.path.exists(archivo):
        print(f"Error: No se encontró el archivo '{archivo}'")
        print("Primero debes ejecutar '2_imagen_a_matriz.py'")
        return
    
    # Cargar datos
    datos = np.load(archivo)
    matrices = datos['matrices']
    nombres = datos['nombres']
    
    print("="*65)
    print(f"VISUALIZACIÓN DE MATRICES 128x128")
    print("="*65)
    print(f"Total de matrices cargadas: {len(matrices)}\n")
    
    while True:
        print("\nOpciones:")
        print("  1 - Ver todas las matrices (completas)")
        print("  2 - Ver todas las matrices (comprimidas)")
        print("  3 - Ver matriz específica")
        print("  4 - Ver estadísticas")
        print("  5 - Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            print("\nMostrando todas las matrices (completas)...")
            print("Nota: Esto puede ser muy largo con muchas imágenes\n")
            for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
                print(f"Imagen {i+1}/{len(matrices)}")
                imprimir_matriz_terminal(matriz, nombre)
                input("Presiona Enter para continuar...")
        
        elif opcion == '2':
            print("\nMostrando todas las matrices (comprimidas)...")
            for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
                imprimir_matriz_comprimida(matriz, nombre, escala=4)
                imprimir_estadisticas(matriz, nombre)
        
        elif opcion == '3':
            print(f"\nDisponibles: {len(matrices)} matrices")
            try:
                indice = int(input("Número de matriz a visualizar (1-{}): ".format(len(matrices)))) - 1
                if 0 <= indice < len(matrices):
                    print("\n1 - Completa")
                    print("2 - Comprimida")
                    vista = input("Tipo de vista (1-2): ").strip()
                    
                    if vista == '1':
                        imprimir_matriz_terminal(matrices[indice], nombres[indice])
                    elif vista == '2':
                        imprimir_matriz_comprimida(matrices[indice], nombres[indice], escala=4)
                    
                    imprimir_estadisticas(matrices[indice], nombres[indice])
                else:
                    print("Índice inválido")
            except ValueError:
                print("Entrada inválida")
        
        elif opcion == '4':
            print("\n" + "="*65)
            print("ESTADÍSTICAS DE TODAS LAS MATRICES")
            print("="*65)
            for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
                print(f"\n{i+1}. {nombre}")
                imprimir_estadisticas(matriz, nombre)
        
        elif opcion == '5':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")


def generar_reporte_txt(archivo_salida="src/reporte_matrices.txt"):
    """
    Genera un archivo de texto con todas las matrices
    """
    archivo = "src/datos_matrices.npz"
    
    if not os.path.exists(archivo):
        print(f"Error: No se encontró '{archivo}'")
        return
    
    datos = np.load(archivo)
    matrices = datos['matrices']
    nombres = datos['nombres']
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("="*65 + "\n")
        f.write("REPORTE DE MATRICES 128x128\n")
        f.write("="*65 + "\n\n")
        
        for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
            f.write(f"\nImagen {i+1}/{len(matrices)}: {nombre}\n")
            f.write("-"*65 + "\n")
            
            # Matriz completa
            for fila in matriz:
                f.write("".join(["█" if v == 1 else "·" for v in fila]) + "\n")
            
            # Estadísticas
            total = matriz.size
            blancos = matriz.sum()
            objetos = total - blancos
            f.write(f"\nEstadísticas:\n")
            f.write(f"  Píxeles blancos (1): {blancos} ({(blancos/total)*100:.2f}%)\n")
            f.write(f"  Píxeles objetos (0): {objetos} ({(objetos/total)*100:.2f}%)\n")
            f.write("="*65 + "\n")
    
    print(f"✓ Reporte guardado en: {archivo_salida}")


if __name__ == "__main__":
    import sys
    
    # Opciones de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reporte':
            generar_reporte_txt()
        else:
            print("Uso: python 3_visualizar_matrices.py [--reporte]")
            print("  Sin argumentos: Modo interactivo")
            print("  --reporte: Genera archivo de texto con todas las matrices")
    else:
        cargar_y_visualizar()
