"""
knn.py - Entrena KNN y encuentra mejor K
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import pickle
import os

def entrenar_knn():
    print("\n" + "="*70)
    print("K-NEAREST NEIGHBORS (KNN)")
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
    
    # Probar diferentes K
    print("\nProbando diferentes valores de K...")
    mejores_k = {}
    
    for k in [3, 5, 7, 9, 11]:
        modelo_temp = KNeighborsClassifier(n_neighbors=k)
        modelo_temp.fit(X_train, y_train)
        y_pred_temp = modelo_temp.predict(X_test)
        acc_temp = accuracy_score(y_test, y_pred_temp)
        mejores_k[k] = acc_temp
        print(f"  K={k}: Accuracy={acc_temp:.4f}")
    
    # Elegir mejor K
    mejor_k = max(mejores_k, key=mejores_k.get)
    print(f"\n✓ Mejor K: {mejor_k} (Accuracy: {mejores_k[mejor_k]:.4f})")
    
    # Entrenar con mejor K
    print(f"\nEntrenando KNN con K={mejor_k}...")
    modelo = KNeighborsClassifier(n_neighbors=mejor_k)
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
    print(f"K óptimo:  {mejor_k}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    
    print("\nMatriz de Confusión:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nReporte Detallado:")
    print(classification_report(y_test, y_pred))
    
    # Guardar modelo
    os.makedirs('modelos', exist_ok=True)
    with open('modelos/knn.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    print("\n✓ Modelo guardado: modelos/knn.pkl")
    
    return {
        'modelo': 'KNN',
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'hiperparametro': f'K={mejor_k}'
    }

if __name__ == "__main__":
    entrenar_knn()