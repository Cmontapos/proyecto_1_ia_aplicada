"""
Script MEJORADO: Ajusta 1 imagen → Aplica a Todas
1. Procesa primera imagen
2. Tú cambias contraste/escala de grises
3. Cuando dices OK, aplica a todas
"""

import cv2
import numpy as np
import os
from pathlib import Path


def aplicar_clahe(img_gris, clip=2.0, tile=8):
    """Aplica CLAHE para realzar detalles"""
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
    return clahe.apply(img_gris)


def aplicar_histogram(img_gris):
    """Ecualización de histograma"""
    return cv2.equalizeHist(img_gris)


def aplicar_gamma(img, gamma=1.0):
    """Corrección gamma para iluminación"""
    if gamma == 1.0:
        return img
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype(np.uint8)
    return cv2.LUT(img, table)


def aplicar_morph(img, kernel_size=0):
    """Limpieza morfológica para eliminar ruido"""
    if kernel_size == 0:
        return img
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def procesar_imagen(ruta_img, tipo_contraste='clahe', clahe_clip=2.0, gamma=1.0, morph=0):
    """Procesa 1 imagen con parámetros"""
    img = cv2.imread(ruta_img)
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar contraste
    if tipo_contraste == 'clahe':
        img_mejorada = aplicar_clahe(img_gris, clip=clahe_clip)
    elif tipo_contraste == 'histogram':
        img_mejorada = aplicar_histogram(img_gris)
    else:
        img_mejorada = img_gris
    
    # Aplicar gamma
    img_mejorada = aplicar_gamma(img_mejorada, gamma=gamma)
    
    # Aplicar morph
    img_mejorada = aplicar_morph(img_mejorada, kernel_size=morph)
    
    # Redimensionar a 128x128
    img_final = cv2.resize(img_mejorada, (128, 128))
    
    return img_final


def mostrar_preview(primera_imagen, tipo_contraste='clahe', clahe_clip=2.0, gamma=1.0, morph=0):
    """Muestra ANTES y DESPUÉS"""
    img_original = cv2.imread(primera_imagen)
    img_gris = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    img_gris_resized = cv2.resize(img_gris, (128, 128))
    
    img_procesada = procesar_imagen(primera_imagen, tipo_contraste, clahe_clip, gamma, morph)
    
    # Lado a lado
    comparacion = np.hstack([img_gris_resized, img_procesada])
    cv2.imwrite('preview.png', comparacion)
    
    print("\n" + "="*70)
    print("✓ PREVIEW GUARDADO: preview.png")
    print("="*70)
    print(f"Parámetros actuales:")
    print(f"  Tipo contraste: {tipo_contraste}")
    print(f"  CLAHE Clip: {clahe_clip}")
    print(f"  Gamma: {gamma}")
    print(f"  Morph: {morph}")
    print("="*70)
    print("Abre preview.png y mira si te gusta\n")


def menu_ajustes():
    """Menú para ajustar parámetros"""
    tipo_contraste = 'clahe'
    clahe_clip = 2.0
    gamma = 1.0
    morph = 0
    
    print("\n" + "="*70)
    print("AJUSTAR PARÁMETROS DE CONTRASTE")
    print("="*70)
    
    while True:
        print("\nOpciones:")
        print("1. Tipo de contraste (clahe/histogram/ninguno)")
        print(f"   Actual: {tipo_contraste}")
        print("\n2. CLAHE Clip (0.5-4.0) - Realza detalles pequeños")
        print(f"   Actual: {clahe_clip}")
        print("\n3. Gamma (0.5-2.0) - Iluminación")
        print(f"   Actual: {gamma}")
        print("   <1 aclara, >1 oscurece")
        print("\n4. Morph (0-7) - Elimina ruido")
        print(f"   Actual: {morph}")
        print("\n5. VER PREVIEW")
        print("6. ACEPTAR Y PROCESAR TODAS")
        print("7. CANCELAR")
        
        opcion = input("\nElige (1-7): ").strip()
        
        if opcion == '1':
            print("Opciones: clahe / histogram / ninguno")
            valor = input("Nuevo tipo: ").strip().lower()
            if valor in ['clahe', 'histogram', 'ninguno']:
                tipo_contraste = valor
                print(f"✓ Tipo = {tipo_contraste}")
            else:
                print("❌ Opción no válida")
        
        elif opcion == '2':
            try:
                valor = float(input("Nuevo CLAHE (0.5-4.0): "))
                if 0.5 <= valor <= 4.0:
                    clahe_clip = valor
                    print(f"✓ CLAHE = {clahe_clip}")
                else:
                    print("❌ Debe estar entre 0.5 y 4.0")
            except:
                print("❌ Valor inválido")
        
        elif opcion == '3':
            try:
                valor = float(input("Nuevo Gamma (0.5-2.0): "))
                if 0.5 <= valor <= 2.0:
                    gamma = valor
                    print(f"✓ Gamma = {gamma}")
                else:
                    print("❌ Debe estar entre 0.5 y 2.0")
            except:
                print("❌ Valor inválido")
        
        elif opcion == '4':
            try:
                valor = int(input("Nuevo Morph (0-7): "))
                if 0 <= valor <= 7:
                    morph = valor if valor % 2 == 1 else valor + 1
                    print(f"✓ Morph = {morph}")
                else:
                    print("❌ Debe estar entre 0 y 7")
            except:
                print("❌ Valor inválido")
        
        elif opcion == '5':
            primera_imagen = list(Path("originales").glob("*.[jp][pn]g"))[0]
            mostrar_preview(str(primera_imagen), tipo_contraste, clahe_clip, gamma, morph)
        
        elif opcion == '6':
            return tipo_contraste, clahe_clip, gamma, morph
        
        elif opcion == '7':
            return None, None, None, None
        
        else:
            print("❌ Opción no válida")


def procesar_todas(tipo_contraste, clahe_clip, gamma, morph):
    """Aplica parámetros a TODAS las imágenes"""
    carpeta_entrada = "originales"
    carpeta_salida = "procesadas"
    
    os.makedirs(carpeta_salida, exist_ok=True)
    
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    archivos = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith(extensiones)]
    
    print("\n" + "="*70)
    print("PROCESANDO TODAS LAS IMÁGENES...")
    print("="*70 + "\n")
    
    for i, archivo in enumerate(archivos, 1):
        ruta_completa = os.path.join(carpeta_entrada, archivo)
        
        img_procesada = procesar_imagen(ruta_completa, tipo_contraste, clahe_clip, gamma, morph)
        
        nombre_salida = Path(archivo).stem + "_128x128.png"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        
        cv2.imwrite(ruta_salida, img_procesada)
        
        print(f"[{i}/{len(archivos)}] ✓ {archivo}")
    
    print("\n" + "="*70)
    print(f"COMPLETADO: {len(archivos)} imágenes procesadas")
    print(f"Guardadas en: {carpeta_salida}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    carpeta_entrada = "originales"
    
    os.makedirs(carpeta_entrada, exist_ok=True)
    
    # Verificar imágenes
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    archivos = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith(extensiones)]
    
    if not archivos:
        print(f"❌ No hay imágenes en '{carpeta_entrada}/'")
        print("Coloca imágenes ahí y ejecuta nuevamente.")
    else:
        print("\n" + "="*70)
        print("PROCESADOR: Ajusta 1 → Aplica a Todas")
        print("="*70)
        print(f"\nEncontradas {len(archivos)} imagen(es)")
        print(f"Primera: {archivos[0]}")
        
        # Ajustar parámetros
        tipo_contraste, clahe_clip, gamma, morph = menu_ajustes()
        
        if tipo_contraste is not None:
            procesar_todas(tipo_contraste, clahe_clip, gamma, morph)
        else:
            print("\nCancelado")