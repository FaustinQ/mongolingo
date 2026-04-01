# 🐉 Mongolingo - React App

Mongolingo est une application React développée dans le cadre du module R4.03. Ce projet utilise MongoDB pour la persistance des données.

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé sur votre machine Ubuntu :
* **Node.js** (v18 ou supérieur recommandé)
* **npm** (installé par défaut avec Node.js)
* **Git**

## 🚀 Installation sur Ubuntu

Suivez ces étapes pour cloner et lancer le projet localement.

### 1. Cloner le projet
Ouvrez votre terminal et récupérez le dépôt :
```bash
git clone https://github.com/FaustinQ/mongolingo.git
cd mongolingo
```

### 2. Gestion des variables d'environnements
Par mesure de sécurité, les identifiants de connexion ne sont pas inclus dans le dépôt. Vous devez créer votre propre fichier .env :
```bash
# Copier le template d'exemple
cp .env.example .env

# Éditer le fichier avec les bons accès
nano .env
```

### 3. Installation des dépendances
Installez l'ensemble des bibliothèques nécessaires au projet :
```bash
npm install
```


### 4. Lancement de l'application
Installez l'ensemble des bibliothèques nécessaires au projet :
```bash
npm start
```
L'application s'ouvrira automatiquement à l'adresse suivante : http://localhost:3000.

✍️ Auteur
   FaustinQ - Étudiant en BUT Informatique
