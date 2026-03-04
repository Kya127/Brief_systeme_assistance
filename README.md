Projet HelpDesk - Mini Système d'Assistance
Description
Ce projet est un mini système d'assistance universitaire permettant aux utilisateurs de créer des tickets, de suivre leur statut et aux administrateurs de gérer les apprenants et les tickets.

Fonctionnalités principales
- Gestion des utilisateurs : Connexion des apprenants et staff.  
- Création de tickets : les apprenants peuvent créer des demandes d'assistance.  
- Suivi des tickets :les utilisateurs peuvent vérifier le statut de leurs tickets.  
- Administration : 
  - Visualiser la liste des apprenants  
  - Lister tous les tickets  
  - Modifier le statut d'un ticket  
  - Supprimer un apprenant
  - Les inscriptions sont uniquement effectuées par le staff 
  - Sécurité : mots de passe stockés avec bcrypt pour le hachage.  

Outils et technologies utilisés
- Python 3 pour le développement  
- MySQL pour la base de données  
- mysql-connector-python pour la connexion à la base  
- bcrypt pour le hachage des mots de passe  
- Git / GitHub pour le versioning et le dépôt  

Fichiers importants
- main.py : code principal du programme  
- creer_admin.py : script pour créer un administrateur premier utilisateur sur la base de données qui inscrit chaque apprenant dans la base de donnée de la fabrique ou l'université
- helpdeskdb_dump.sql : dump de la base de données MySQL  
- .gitignore : pour exclure `venv/` et `.vscode/`  

---

> Ce mini-projet permet de simuler un système d'assistance simple pour la gestion des tickets et des utilisateurs dans un contexte universitaire.
