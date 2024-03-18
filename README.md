# Projet Data 3A Centrale Méditerranée - Création d'un salaires checker pour les offres de France Travail.

Dans ce repo, vous trouverez les fichiers et scripts permettant l'entrainement et l'industrialisation d'un modèle de prédiction de salaires basé sur l'API de France Travail (ex Pôle Emploi).

Le notebook `cleaning_and_modelisation.ipynb` est le pilier de cette modélisation et permet, à partir du fichier de données brutes `df_offresetsalaires.csv` d'entraîner le modèle et d'exporter les fichiers d'entrainement pour l'industrialisation du modèle (.csv et .pkl). Il contient également une rapide estimation des performances du modèle.

Les autres fichiers servent à la mise en production du modèle, à l'exception de `stop_words_french.txt` qui est utilisé pour le pré-traitement des descriptions.
