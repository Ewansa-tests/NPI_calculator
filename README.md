# API Calculatrice NPI

Ce projet implémente une API de calculatrice en Notation Polonaise Inversée (NPI) en utilisant Python et FastAPI. L'API permet aux utilisateurs d'évaluer des expressions mathématiques au format NPI et de stocker les expressions ainsi que leurs résultats dans une base de données SQLite. De plus, elle offre des points de terminaison pour récupérer les résultas de calcul au format CSV.

## Fonctionnalités

- **Endpoint de Calcul** : Évalue les expressions NPI postées à `/calculate`.
- **Intégration de la Base de Données** : Stocke l'historique des calculs dans une base de données SQLite (`calculator.db`).
- **Endpoint d'Exportation des Enregistrements** : Récupère les enregistrements de calcul au format CSV depuis `/recup`.
- **Gestion des Erreurs** : Fournit des messages d'erreur significatifs pour les expressions et jetons invalides.
- **Tests Unitaires** : Comprend des tests unitaires avec pytest pour assurer la fonctionnalité des opérations de calcul et de base de données.

## Technologies Utilisées

- **Python** : Langage de programmation utilisé pour la logique backend.
- **FastAPI** : Cadre web utilisé pour créer des API RESTful.
- **SQLite** : Base de données relationnelle légère utilisée pour le stockage des données.
- **pytest** : Cadre de test utilisé pour les tests unitaires.
- **Docker** : Outil de conteneurisation utilisé pour le déploiement.
