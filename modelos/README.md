# 📊 Modelos de Clasificación

Scripts para entrenar y comparar modelos de clasificación clásicos.

## 📋 Requisitos

```bash
pip install scikit-learn pandas numpy
```

## 🚀 Uso

### 1. Entrenar cada modelo individual

```bash
# Árbol de Decisión
python 1_arbol_decision.py

# Naive Bayes
python 2_naive_bayes.py

# KNN (encuentra K óptimo)
python 3_knn.py

# SVM (encuentra kernel óptimo)
python 4_svm.py
```

### 2. Comparar todos los modelos

```bash
python comparar_modelos.py
```

Muestra una tabla con Accuracy, Precision y Recall de todos.

## 📁 Estructura

```
modelos/
├── 1_arbol_decision.py      ← Entrena árbol
├── 2_naive_bayes.py         ← Entrena Naive Bayes
├── 3_knn.py                 ← Entrena KNN (optimiza K)
├── 4_svm.py                 ← Entrena SVM (optimiza kernel)
├── comparar_modelos.py      ← Compara todos
├── README.md                ← Este archivo
├── arbol_decision.pkl       ← Modelo guardado
├── naive_bayes.pkl          ← Modelo guardado
├── knn.pkl                  ← Modelo guardado
├── svm.pkl                  ← Modelo guardado
└── resultados/
    └── comparacion.csv      ← Resultados en CSV
```

## 📊 Qué hace cada script

### Árbol de Decisión
- max_depth=15 (ajusta para evitar overfitting)
- Muestra matriz de confusión
- Guarda modelo

### Naive Bayes
- GaussianNB por defecto
- Rápido de entrenar
- Buen baseline

### KNN
- Prueba K = 3, 5, 7, 9, 11
- Elige el K con mejor accuracy
- Entrena con K óptimo

### SVM
- Prueba kernels: linear, rbf, poly
- Elige el kernel con mejor accuracy
- Entrena con kernel óptimo

### Comparar Modelos
- Carga los 4 modelos guardados
- Evalúa en test set
- Muestra tabla comparativa
- Identifica el mejor
- Guarda resultados en CSV

## 📈 Salida Esperada

```
ÁRBOL DE DECISIÓN
Accuracy:  0.9200
Precision: 0.9100
Recall:    0.9300

NAIVE BAYES
Accuracy:  0.8800
Precision: 0.8600
Recall:    0.9000

KNN
K óptimo:  7
Accuracy:  0.9000
Precision: 0.8900
Recall:    0.9100

SVM
Kernel óptimo: rbf
Accuracy:  0.9500
Precision: 0.9400
Recall:    0.9600

🏆 MEJOR MODELO
Modelo: SVM
Accuracy: 0.9500
```

## 💾 Archivos Generados

- `arbol_decision.pkl` - Modelo entrenado
- `naive_bayes.pkl` - Modelo entrenado
- `knn.pkl` - Modelo entrenado
- `svm.pkl` - Modelo entrenado
- `resultados/comparacion.csv` - Tabla de comparación

## 🔧 Personalización

### Cambiar split train/test

En cada script, cambia:
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42  # 0.2 = 20% test
)
```

### Cambiar parámetros de modelos

**Árbol:**
```python
modelo = DecisionTreeClassifier(max_depth=10)  # Cambia aquí
```

**KNN:**
```python
for k in [3, 5, 7, 9, 11]:  # Agrega más valores
```

**SVM:**
```python
for kernel in ['linear', 'rbf', 'poly', 'sigmoid']:  # Agrega más
```

## 📝 Notas

- Primero ejecuta `python 4_generar_dataset.py` para crear el dataset
- Los modelos se guardan automáticamente en `.pkl`
- Puedes cargar un modelo guardado así:

```python
import pickle
with open('modelos/svm.pkl', 'rb') as f:
    modelo = pickle.load(f)

# Usar para predecir
prediccion = modelo.predict(nueva_imagen)
```

## ✅ Checklist

- [ ] Dataset generado (`src/dataset_con_etiquetas.npz`)
- [ ] Entrenaste árbol de decisión
- [ ] Entrenaste Naive Bayes
- [ ] Entrenaste KNN
- [ ] Entrenaste SVM
- [ ] Comparaste todos los modelos
- [ ] Identificaste el mejor