# 🐉 Mongolingo - React App

Mongolingo est une application React développée dans le cadre du module R4.03. Ce projet utilise MongoDB pour la persistance des données.

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé sur votre machine Ubuntu :
* **Node.js** (v18 ou supérieur recommandé)
* **npm** (installé par défaut avec Node.js)
* **Git**
* **Python3/pip**

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
Et les pré-requis pour le back-end
```bash
sudo apt install python3-uvicorn python3-fastapi python3-dotenv python3-pymongo python3-motor python3-dnspython
```

Des fois, pydantic n'est pas a jour sur Ubuntu, il faut alors faire:
```bash
pip install --upgrade pydantic --break-system-packages
```


### 4. Lancement de l'application
D'abord il faut lancer le back-end:
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Puis le front end dans un autre terminal:
```bash
npm start
```
L'application s'ouvrira automatiquement à l'adresse suivante : http://localhost:3000.

✍️ Auteur
   FaustinQ - Étudiant en BUT Informatique
