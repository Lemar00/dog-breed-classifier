#!/bin/bash

# Définition de la date d'exécution et des répertoires de log
EXECUTION_DATE=$(date "+%Y%m%d-%H%M")
YEAR=$(date "+%Y")
MONTH=$(date "+%m")

# Définition du répertoire de projet et des logs
PROJECT_DIR=$PWD
LOGS_DIR=${PROJECT_DIR}/logs/${YEAR}/${MONTH}

# Création des répertoires de logs si nécessaire
mkdir -p ${LOGS_DIR}

# Affichage du message de début
echo "=========================== Start Dog classification training ==========================="

# Exécution du notebook avec Papermill
papermill notebooks/dog_predict.ipynb \
"${LOGS_DIR}/${EXECUTION_DATE}-dog_predict-artifact.ipynb" \
-k python39 --report-mode --log-output --no-progress-bar

# Vérification du succès de l'exécution
if [ $? != 0 ]; then
  echo "ERROR: failure during training!"
  exit 1
fi

# Affichage du message de succès
echo "============================== SUCCESS: Done Dog classification training =============================="