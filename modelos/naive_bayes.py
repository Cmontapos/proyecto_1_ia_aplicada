"""
naive_bayes.py - Entrena Naive Bayes
"""

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import pickle
import os

def entrenar_naive_bayes():
    print("\n" + "="*70)
    print("NAIVE BAYES")
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
    
    # Entrenar
    print("\nEntrenando...")
    modelo = GaussianNB()
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
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    
    print("\nMatriz de Confusión:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nReporte Detallado:")
    print(classification_report(y_test, y_pred))
    
    # Guardar modelo
    os.makedirs('modelos', exist_ok=True)
    with open('modelos/naive_bayes.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    print("\n✓ Modelo guardado: modelos/naive_bayes.pkl")
    
    return {
        'modelo': 'Naive Bayes',
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }

if __name__ == "__main__":
    entrenar_naive_bayes()