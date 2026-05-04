# Pipeline de Preprocesamiento para Detección de Contaminación

## 📋 Descripción General

Este proyecto procesa imágenes para crear un dataset para detectar contaminación (granos de arroz) en muestras. El flujo completo es:

1. **Preprocesamiento**: Imagen Original → Blanco y Negro → 128×128 píxeles
2. **Binarización**: Matriz 128×128 → Matriz de 1s (blanco) y 0s (objeto)
3. **Visualización**: Ver matrices en la terminal
4. **Dataset**: Vectores de 16,384 elementos + etiqueta (1=contaminación, 0=sin)

---

## 🛠 Instalación de Dependencias

```bash
pip install opencv-python numpy
```

---

## 📂 Estructura de Carpetas

```
proyecto/
├── imagenes_originales/          ← Coloca aquí tus imágenes
├── imagenes_procesadas/          ← Se crea automáticamente
├── 1_preprocesar_imagenes.py
├── 2_imagen_a_matriz.py
├── 3_visualizar_matrices.py
├── 4_generar_dataset.py
└── guia_completa.py              ← Ejecuta esto primero
```

---

## 🚀 Cómo Usar

### Opción 1: Guía Interactiva (RECOMENDADO)

```bash
python guia_completa.py
```

Te guiará paso a paso a través de todo el proceso.

### Opción 2: Scripts Individuales

#### **PASO 1: Preprocesamiento**
```bash
python 1_preprocesar_imagenes.py
```

**Qué hace:**
- Lee imágenes de `imagenes_originales/`
- Convierte a escala de grises
- Redimensiona a 128×128
- Guarda en `imagenes_procesadas/`

**Archivos de entrada:** `imagenes_originales/*.jpg`, `*.png`, etc.  
**Archivos de salida:** `imagenes_procesadas/*_128x128.png`

---

#### **PASO 2: Conversión a Matrices**
```bash
python 2_imagen_a_matriz.py
```

**Qué hace:**
- Lee imágenes 128×128 de `imagenes_procesadas/`
- Convierte cada píxel a 1 (blanco) o 0 (objeto)
- Guarda matrices en `datos_matrices.npz`

**Codificación:**
- `1` = píxel blanco (fondo limpio)
- `0` = píxel con objeto (grano de arroz u otro)

**Archivos de entrada:** `imagenes_procesadas/*.png`  
**Archivos de salida:** `datos_matrices.npz`

---

#### **PASO 3: Visualización de Matrices**
```bash
python 3_visualizar_matrices.py
```

**Características:**
- Ver todas las matrices (completas o comprimidas)
- Ver matriz específica
- Ver estadísticas
- Generar reporte en archivo de texto

**Símbolos visuales:**
- `█` = píxel blanco (1)
- `·` = píxel con objeto (0)

**Opciones adicionales:**
```bash
python 3_visualizar_matrices.py --reporte
```
Genera `reporte_matrices.txt` con todas las matrices

---

#### **PASO 4: Generar Dataset**
```bash
python 4_generar_dataset.py
```

**Qué hace:**
1. Convierte matrices 128×128 → vectores de 16,384 elementos
2. Solicita etiqueta para cada imagen:
   - `1` = Hay contaminación (arroz/grano presente)
   - `0` = Sin contaminación
3. Genera dataset en múltiples formatos

**Archivos de salida:**
- `dataset_con_etiquetas.npz` - Formato NumPy (recomendado para ML)
- `dataset_con_etiquetas.csv` - Excel/Pandas compatible
- `dataset_info.json` - Información del dataset
- `etiquetas.json` - Solo etiquetas (para reutilización)

**Formato del dataset:**
```
[pixel_0, pixel_1, pixel_2, ..., pixel_16383, etiqueta]
```

Cada fila tiene:
- 16,384 valores (0 o 1) representando la imagen
- 1 valor final (0 o 1) indicando si hay contaminación

---

## 📊 Archivos Generados

| Archivo | Descripción |
|---------|------------|
| `imagenes_procesadas/` | Imágenes 128×128 en B&N |
| `datos_matrices.npz` | Matrices binarias comprimidas |
| `dataset_con_etiquetas.npz` | Dataset en formato NumPy |
| `dataset_con_etiquetas.csv` | Dataset en CSV (Excel) |
| `dataset_info.json` | Estadísticas del dataset |
| `etiquetas.json` | Archivo de etiquetas |
| `reporte_matrices.txt` | Reporte visual de matrices |

---

## 💡 Ejemplos de Uso en Python

### Cargar Dataset

```python
import numpy as np

# Cargar dataset
datos = np.load('dataset_con_etiquetas.npz')
vectores = datos['vectores']      # Shape: (n_imágenes, 16384)
etiquetas = datos['etiquetas']    # Shape: (n_imágenes,)

# Acceder a primera imagen
imagen_1 = vectores[0]           # Array de 16384 elementos
etiqueta_1 = etiquetas[0]        # 0 o 1

print(f"Total de imágenes: {len(vectores)}")
print(f"Con contaminación: {etiquetas.sum()}")
print(f"Sin contaminación: {len(etiquetas) - etiquetas.sum()}")
```

### Cargar desde CSV

```python
import pandas as pd

df = pd.read_csv('dataset_con_etiquetas.csv')

# Separar características y etiquetas
X = df.iloc[:, :-1].values         # Primeras 16384 columnas
y = df.iloc[:, -1].values          # Última columna (etiqueta)
```

### Cargar Matrices

```python
import numpy as np

# Cargar matrices
datos = np.load('datos_matrices.npz')
matrices = datos['matrices']       # Shape: (n_imágenes, 128, 128)
nombres = datos['nombres']         # Nombres de archivos

# Acceder a primera matriz
matriz_1 = matrices[0]             # Array 128x128
print(matriz_1.shape)              # (128, 128)
```

---

## 🎯 Parámetros Importantes

### Preprocesamiento
- **Tamaño final:** 128×128 píxeles (configurable)
- **Escala de color:** Blanco y Negro (8-bit)

### Binarización
- **Umbral:** 127 (configurables en código)
- **Valor blanco:** 1
- **Valor objeto:** 0

### Dataset
- **Elementos por vector:** 16,384 (128 × 128)
- **Etiqueta 1:** Hay contaminación
- **Etiqueta 0:** Sin contaminación

---

## ⚙️ Personalización

### Cambiar tamaño de imagen

En `1_preprocesar_imagenes.py`, línea 17:
```python
imagen_redimensionada = cv2.resize(imagen_gris, (256, 256))  # Cambia aquí
```

### Cambiar umbral de binarización

En `2_imagen_a_matriz.py`, línea 30:
```python
matriz_binaria = (imagen > 200).astype(int)  # Cambia 200
```

---

## 🐛 Solución de Problemas

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### "No se encontraron imágenes en imagenes_originales"
- Copia tus imágenes a la carpeta `imagenes_originales/`
- Formatos válidos: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

### "No existe datos_matrices.npz"
- Primero ejecuta el PASO 2 (conversión a matrices)

### Las matrices se ven vacías
- Ajusta el umbral en `2_imagen_a_matriz.py`
- Verifica que las imágenes originales tengan buen contraste

---

## 📈 Flujo Visual del Proyecto

```
Imagen Original (cualquier tamaño)
        ↓
    [PASO 1]
Conversión B&N + Redimensión 128×128
        ↓
Imagen 128×128 en escala de grises
        ↓
    [PASO 2]
Binarización → Matriz 1s y 0s
        ↓
    [PASO 3 - Opcional]
Visualizar matrices en terminal
        ↓
    [PASO 4]
Vector fila 16384 elementos + Etiqueta
        ↓
DATASET FINAL ✓
```

---

## 👥 Para Trabajo en Grupo

1. **Alumno 1-3:** Preprocesen sus imágenes
2. **Alumno 4-6:** Ejecuten la binarización
3. **Todos:** Combinen datos en carpeta compartida
4. **Alumno 7+:** Generen dataset final consolidado

**Para compartir datos:**
- Copiar `datos_matrices.npz` → carpeta compartida
- O copiar `dataset_con_etiquetas.npz` si ya está etiquetado

---

## 📝 Notas Importantes

- ✅ Los datos se guardan en formatos estándar (NumPy, CSV)
- ✅ Compatible con scikit-learn, TensorFlow, PyTorch
- ✅ Apto para clustering, clasificación binaria, redes neuronales
- ✅ Etiquetado opcional: Puedes generar solo matrices sin etiquetar

---

## 📞 Ayuda

Si tienes problemas:
1. Verifica que instalaste las dependencias: `pip install opencv-python numpy`
2. Asegúrate de que tus imágenes están en `imagenes_originales/`
3. Ejecuta los pasos en orden: 1 → 2 → 4 (3 es opcional)
4. Lee los mensajes de error en la terminal

---

**¡Listo para empezar! Ejecuta: `python guia_completa.py`**
