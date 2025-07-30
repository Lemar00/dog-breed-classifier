# dog-breed-classifier

## Projet de Classification des Races de Chiens

Ce repository contient un projet de classification de races de chiens à l'aide de modèles de Deep Learning. Le projet est structuré comme suit :

---

## Structure du Repository

### 📁 notebooks/
Contient les différents notebooks Jupyter utilisés pour le développement et l'expérimentation.
- `train_dog_classifier.ipynb` : Notebook final regroupant le prétraitement des données, l'entraînement et l'évaluation des modèles, ainsi que le monitoring via MLFlow.

### 📁 src/
Contient les fonctions et modules utilisés pour le traitement des données et la construction des modèles :
- `make_model_densenet.py` : Création et entraînement du modèle **DenseNet**.
- `make_model_mobilenet.py` : Création et entraînement du modèle **MobileNetV2**.
- `make_model_vgg16.py` : Création et entraînement du modèle **VGG16**.
- `make_dataset.py` : Chargement et séparation du dataset (train/val/test).
- `eval_metrics.py` : Fonction d’évaluation des performances des modèles.

### 📁 settings/
Contient les paramètres de configuration pour l'entraînement :
- `config.py` : Fichier de configuration des hyperparamètres et chemins.

### 📁 api/
Représente le **backend FastAPI**. Il expose une API REST permettant de faire des prédictions à partir d'une image de chien.
- `main.py` : Fichier principal de l'API FastAPI avec l’endpoint `/predict`.
- `model_loader.py` : Chargement du modèle entraîné.
- `utils.py` : Fonctions utilitaires pour la prédiction (prétraitement d’image, etc.).

### 📁 frontend/
Représente l’**interface utilisateur** développée avec React (ou tout autre framework frontend).
- Permet à l’utilisateur d’uploader une image et de voir la race prédite par le modèle via l’API.

### 📄 run_dog_classification.sh
Script shell pour exécuter les différentes étapes de la pipeline ML.

### 📄 docker-compose.yml
Fichier de composition Docker permettant de démarrer facilement tous les services du projet :
- **backend (API)** : Serveur FastAPI exposant l’endpoint `/predict`.
- **frontend** : Interface web utilisateur.
- (optionnel) **MLflow** ou **PostgreSQL** si tu veux étendre la stack.

Ce fichier permet de démarrer l’ensemble du projet (backEnd et FrontEnd) avec une seule commande : ```bash docker-compose up --build


Le modèle entraîné est disponible sur Google Drive. Vous pouvez le télécharger en utilisant le lien ci-dessous :

[Télécharger le modèle entraîné (mobilenetv2_best.keras qui est notre best Model d'apres les metrics)](dans le dossier /Model)

### Instructions pour Utiliser le Modèle

1. Téléchargez le modèle dans ce dossier.
2. Placez le fichier `mobilenetv2_best.keras` dans le répertoire `/app`.

## Obtenir le Dataset

Le projet utilise le dataset Dog Classification de Stanford Dogs Dataset pour l'entraînement et la validation du modèle. Vous pouvez le télécharger à partir du lien suivant :

[**Télécharger le Dataset**](http://vision.stanford.edu/aditya86/ImageNetDogs/)

### Structure du Dataset

Le dataset contient des images classifiées en 36 catégories. Voici la répartition de quelque classes :

- **Afghan_hound**: 239 images
- **African_hunting_dog**: 169 images
- **Blenheim_spaniel**: 188 images
- **Borzoï**: 151 images
- **Brabancon_griffon**: 153 images
- **Cardigan**: 155 images


Chaque image est placée dans un répertoire correspondant à sa classe. Assurez-vous que la structure des dossiers reflète cette distribution pour un traitement correct des données.


## Instructions d'Utilisation

1. **Installation des Dépendances** : 
   Assurez-vous que vous avez toutes les dépendances nécessaires en installant les packages listés dans `requirements.txt` qui se trouve dans le dosssier /api :
   ```bash
   pip install -r requirements.txt

2. **Execution des notebooks** : 

   - **Jupyter** :  
   Pour exécuter les notebooks, vous pouvez utiliser Jupyter Notebook

   - **CLI**:  
  Pour obtenir une version des résultats de l'exécution du notebook, vous pouvez utiliser le fichier `run_dog_classification.sh`. Ce script utilise la bibliothèque `papermill` pour exécuter le notebook et sauvegarder les résultats dans le dossier `logs` (qui sera automatiquement créé si nécessaire).  

  a. Placez-vous dans le dossier `dog-breed-classifier`.  
  b. Exécutez les commandes suivantes :


        sh run_dog_classification.sh ou ./run_dog_classification.sh
