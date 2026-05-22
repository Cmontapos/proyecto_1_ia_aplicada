# Model Card: Detector de Contaminación en Arroz

## 1. Información del Modelo

**Nombre del Modelo:** Clasificador de Contaminación en Arroz  
**Versión:** 1.0  
**Fecha de Creación:** 21/5/26  
**Autor(es):** Cristopher Montero Campos  
**Institución:** Universidad de Costa Rica  

---

## 2. Uso Previsto

### Uso Indicado
- Clasificación binaria de muestras de arroz como:
  - **Clase 0:** Sin contaminación (grano limpio)
  - **Clase 1:** Con contaminación (presencia de cuerpos extraños)
- Automatización de control de calidad en molinos de arroz
- Procesamiento de imágenes en línea de producción

### Uso NO Indicado (Out-of-Scope)
- Clasificación de otros tipos de granos (maíz, trigo)
- Identificación del tipo específico de contaminante
- Predicción de nivel de contaminación (solo binario)
- Procesamiento de imágenes con resolución muy alta (>200×200)
- Análisis de contaminación química

---

## 3. Sumario de Datos

### Recolección de Datos
- **Fuente:** Particularmente camarás de celular
- **Cantidad de Imágenes:** 447
  - Muestras limpias: 225
  - Muestras contaminadas: 222
- **Resolución Original:** Variadas
- **Resolución Final:** 128×128 píxeles (en escala de grises)
- **Período de Recolección:** Mayo/Abril 2025
- **Ubicación Geográfica:** San José Costa Rica

### Variaciones en los Datos
- **Iluminación:** Controlada  / Natural 
- **Cámaras Utilizadas:** Samsung S23 FE (Propietario)
- **Fondos:** Uniforme blanco
- **Distancia del Objetivo:** Constante (30-40 cm aprox)
- **Ampliación:** Sin ampliación

### Limitaciones del Dataset
1. **Tamaño limitado:** Dataset pequeño (< 500 imágenes idealmente)
2. **Sesgo de iluminación:** Mayormente luz controlada de luz de celular
3. **Sesgo de cámara:** Varios dispositivos de captura
4. **Variabilidad de contaminantes:** Solo granos visibles, no polvo fino
5. **Objetos pequeños:** Difícil detectar partículas < 2 píxeles
6. **Oclusión:** No maneja granos parcialmente cubiertos
7. **Desenfoque (blur):** Imágenes borrosas degradan rendimiento

---

## 4. Proceso de Etiquetado

### Herramienta Utilizada
- **Herramienta:** Etiquetado actumatico luego de procesar con etiquetas "limpia" o "sucia"
- **Script:** `4_generar_dataset.py`
- **Tiempo Estimado:** ~0.5 minuto por imagen

### Protocolo de Etiquetado
| Etiqueta | Significado | Criterios |
|----------|-------------|-----------|
| **0** | Sin contaminación | Grano de arroz limpio, sin cuerpos extraños visibles |
| **1** | Con contaminación | Presencia de ≥1 partícula extraña (piedra, polvo, otro grano) |

### Consistencia y Control de Calidad
- **Etiquetador(es):** Autor
- **Acuerdo Inter-Anotador:** 95%
- **Revisión:** Sí - Segunda revisión de anotaciones conflictivas
- **Resolución de Conflictos:** Se proceso cada imagen del dataset por aparte para evitar malas etiquetas

---

## 5. Métricas de Desempeño para mejor modelo SVM

### Métricas Utilizadas
- **Accuracy:** Porcentaje de predicciones correctas
- **Precision:** TP / (TP + FP) - Exactitud en detectar contaminación
- **Recall:** TP / (TP + FN) - Capacidad de no dejar pasar contaminación
- **F1-Score:** Media armónica de Precision y Recall
- **Matriz de Confusión:** Desglose detallado de errores

### Cómo se Calcularon
```python
# Ejemplo de evaluación
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
```

### División de Datos
- **Entrenamiento:** 80% (453 imagenes)
- **Validación:** 20% (114 imagenes)

### Resultados Obtenidos
| Métrica | Valor | Notas |
|---------|-------|-------|
| Accuracy | 77,2% | En conjunto de prueba |
| Precision | 79,7% | Pocas falsas alarmas |
| Recall | 84,3% | Detecta la mayoría de contaminación |


---

## 6. Notas Éticas y de Seguridad

### Posibles Sesgos

#### 1. **Sesgo por Iluminación**
- ⚠️ Problema: Modelo entrenado con luz controlada, falla con luz variable
- 🛡️ Mitigación: Incluir imágenes con diferentes iluminaciones

#### 2. **Sesgo por Cámara**
- ⚠️ Problema: Varios tipos de cámara
- 🛡️ Mitigación: Estandarizar las tomas

#### 3. **Sesgo por Fondo**
- ⚠️ Problema: Fondo uniforme blanco, no refleja ambiente real
- 🛡️ Mitigación: Usar fondos variados (natural, vidrio, papel)

#### 4. **Sesgo por Tipo de Contaminación**
- ⚠️ Problema: Solo granos visibles, no detecta contaminación química
- 🛡️ Nota: Limitación del método, requeriría técnicas diferentes

### Impacto en Usuarios
- **Positivo:** Reduce carga manual de inspección visual
- **Riesgo:** Falsos negativos → contaminación sale al mercado
- **Recomendación:** Usar como herramienta de apoyo, no decisión final

---

## 7. Limitaciones Conocidas

1. **Objetos Pequeños**
   - Particulas < 2 píxeles no se detectan confiablemente
   - Resolución 128×128 pierde detalle fino

2. **Oclusión**
   - Contaminante parcialmente cubierto por grano = no se detecta

3. **Desenfoque (Blur)**
   - Imágenes borrosas degradan significativamente el rendimiento
   - Requiere captura con buena resolución

4. **Generalizabilidad**
   - Modelo entrenado en arroz blanco, puede fallar con variedades rojas/negras
   - Datos de región específica, puede no generalizar a otras zonas

5. **Límite Binario Difuso**
   - Qué constituye "contaminación" vs "grano de otro tipo" es subjetivo
   - Etiquetas pueden tener inconsistencia humana

---

## 8. Reproducibilidad

### Ambiente y Hardware

**Sistema Operativo:** 
```
Linux Ubuntu
```

**Hardware:**
```
Procesador: I3 N305
Memoria RAM: 8 MB
GPU: N/A
Python: 3.8 o superior
```

### Dependencias Exactas
Ver `requirements.txt`:
```
opencv-python==4.8.1.78
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
matplotlib==3.7.2
```

### Instrucciones Paso a Paso

#### 1. **Preparar Ambiente**
```bash
# Clonar repositorio
git clone <tu-repo>
cd proyecto_1_ia_aplicada

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. **Preparar Datos**
```bash
# Coloca imágenes originales en:
mkdir -p imagenes_originales
# [Copiar archivos .jpg/.png aquí previamente etiquetados con limpia o sucia]


# Ejecutar preprocesamiento
python 1_preprocesar_imagenes.py
python 2_imagen_a_matriz.py
python 4_generar_dataset.py  # Etiquetar manualmente
```

#### 3. **Entrenar Modelo** (ver archivo `5_entrenar_modelo.py`)
```bash
python 5_entrenar_modelo.py --test-size 0.15 --model logistic
```

#### 4. **Evaluar**
```bash
python 6_evaluar_modelo.py --modelo modelos/modelo_final.pkl
```

#### 5. **Inferencia**
```bash
python 7_inferencia.py --imagen imagen_test.png --modelo modelos/modelo_final.pkl
```

### Seed Reproducible
```python
# Todos los scripts usan:
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
```

### Tiempo Estimado
- Preprocesamiento: 2-5 minutos (según cantidad de imágenes)
- Etiquetado: 1-2 minutos por imagen
- Entrenamiento: < 1 minuto
- Evaluación: < 30 segundos

---

## 9. Historial de Cambios

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | [Fecha] | Versión inicial, baseline con Logistic Regression |
| [TBD] | [TBD] | Posible mejora con Random Forest |

---

## 10. Contacto y Referencias

**Contacto:** cris04montero@gmail.com
**Repositorio:** https://github.com/Cmontapos/proyecto_1_ia_aplicada
**Documentación Relacionada:**
- `DATASET.md` - Detalles del dataset
- `README.md` - Instrucciones de uso
- `reports/informe_final.md` - Análisis detallado

---

**Última actualización:** 22/5/26
