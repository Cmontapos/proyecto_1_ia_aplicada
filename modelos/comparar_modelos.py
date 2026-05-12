"""
comparar_modelos.py - Compara todos los modelos entrenados
"""

import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

def cargar_dataset():
    """Carga el dataset"""
    try:
        datos = np.load('src/dataset_con_etiquetas.npz')
        X = datos['vectores']
        y = datos['etiquetas']
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except:
        print("❌ Error: No encontré src/dataset_con_etiquetas.npz")
        return None

def cargar_modelo(ruta):
    """Carga un modelo guardado"""
    try:
        with open(ruta, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def evaluar_modelo(modelo, X_test, y_test, nombre):
    """Evalúa un modelo"""
    try:
        y_pred = modelo.predict(X_test)
        return {
            'Modelo': nombre,
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred),
            'Recall': recall_score(y_test, y_pred)
        }
    except:
        return None

def comparar_modelos():
    print("\n" + "="*70)
    print("COMPARACIÓN DE TODOS LOS MODELOS")
    print("="*70 + "\n")
    
    # Cargar dataset
    resultado = cargar_dataset()
    if resultado is None:
        return
    
    X_train, X_test, y_train, y_test = resultado
    
    # Cargar modelos
    modelos = {
        'Árbol de Decisión': 'modelos/arbol_decision.pkl',
        'Naive Bayes': 'modelos/naive_bayes.pkl',
        'KNN': 'modelos/knn.pkl',
        'SVM': 'modelos/svm.pkl'
    }
    
    resultados = []
    modelos_cargados = 0
    
    for nombre, ruta in modelos.items():
        if not os.path.exists(ruta):
            print(f"⚠ {nombre} no encontrado: {ruta}")
            continue
        
        print(f"Evaluando {nombre}...", end=" ")
        modelo = cargar_modelo(ruta)
        
        if modelo is None:
            print("❌ Error al cargar")
            continue
        
        resultado_eval = evaluar_modelo(modelo, X_test, y_test, nombre)
        if resultado_eval:
            resultados.append(resultado_eval)
            modelos_cargados += 1
            print("✓")
    
    if not resultados:
        print("\n❌ No hay modelos entrenados")
        print("Ejecuta primero:")
        print("  python modelos/1_arbol_decision.py")
        print("  python modelos/2_naive_bayes.py")
        print("  python modelos/3_knn.py")
        print("  python modelos/4_svm.py")
        return
    
    # Crear tabla
    df = pd.DataFrame(resultados)
    df = df.sort_values('Accuracy', ascending=False)
    
    print("\n" + "="*70)
    print("RESULTADOS COMPARATIVOS")
    print("="*70 + "\n")
    print(df.to_string(index=False))
    
    # Mejor modelo
    mejor = df.iloc[0]
    print("\n" + "="*70)
    print("🏆 MEJOR MODELO")
    print("="*70)
    print(f"Modelo: {mejor['Modelo']}")
    print(f"Accuracy:  {mejor['Accuracy']:.4f}")
    print(f"Precision: {mejor['Precision']:.4f}")
    print(f"Recall:    {mejor['Recall']:.4f}")
    print("="*70 + "\n")
    
    # Guardar resultados
    os.makedirs('modelos/resultados', exist_ok=True)
    df.to_csv('modelos/resultados/comparacion.csv', index=False)
    print("✓ Resultados guardados en: modelos/resultados/comparacion.csv")

if __name__ == "__main__":
    comparar_modelos()