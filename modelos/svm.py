"""
svm.py - Entrena SVM y encuentra mejor kernel
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import joblib
import os

def entrenar_svm():
    print("\n" + "="*70)
    print("SUPPORT VECTOR MACHINE (SVM)")
    print("="*70 + "\n")
    
    # Cargar dataset
    try:
        datos = np.load('src/dataset_con_etiquetas.npz')
        X = datos['vectores']
        y = datos['etiquetas']
        print(f"✓ Dataset cargado: {len(X)} imágenes")
    except:
        print("❌ Error: No encontré src/dataset_con_etiquetas.npz")
        print("Primero ejecuta: python 4_generar_dataset.py")
        return
    
    # Dividir train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Probar diferentes kernels
    print("\nProbando diferentes kernels...")
    mejores_kernels = {}
    
    for kernel in ['linear', 'rbf', 'poly']:
        print(f"  Entrenando {kernel}...", end=" ")
        modelo_temp = SVC(kernel=kernel, random_state=42)
        modelo_temp.fit(X_train, y_train)
        y_pred_temp = modelo_temp.predict(X_test)
        acc_temp = accuracy_score(y_test, y_pred_temp)
        mejores_kernels[kernel] = acc_temp
        print(f"Accuracy={acc_temp:.4f}")
    
    # Elegir mejor kernel
    mejor_kernel = max(mejores_kernels, key=mejores_kernels.get)
    print(f"\n✓ Mejor kernel: {mejor_kernel} (Accuracy: {mejores_kernels[mejor_kernel]:.4f})")
    
    # Entrenar con mejor kernel
    print(f"\nEntrenando SVM con kernel={mejor_kernel}...")
    modelo = SVC(kernel=mejor_kernel, random_state=42)
    modelo.fit(X_train, y_train)
    print("✓ Modelo entrenado")
    
    # Predecir
    y_pred = modelo.predict(X_test)
    
    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print("\n" + "="*70)
    print("RESULTADOS")
    print("="*70)
    print(f"Kernel óptimo: {mejor_kernel}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    
    print("\nMatriz de Confusión:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nReporte Detallado:")
    print(classification_report(y_test, y_pred))
    
    # Guardar modelo
    os.makedirs('modelos', exist_ok=True)
    joblib.dump(modelo, 'modelos/svm.joblib')
    print("\n✓ Modelo guardado")
    
    return {
        'modelo': 'SVM',
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'hiperparametro': f'kernel={mejor_kernel}'
    }

if __name__ == "__main__":
    entrenar_svm()