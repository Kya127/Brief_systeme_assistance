import mysql.connector
import bcrypt

connection = mysql.connector.connect(
    host="localhost",
    user="MariamHarouna",
    password="Simplon@2025",
    database="Helpdeskdb"
)

curseur = connection.cursor()
print("Connecté à MySQL avec succès")

# Saisie des informations de l'admin
print("Création de l'utilisateur admin")
nom_admin = input("Nom : ")
email_admin = input("Email : ")
mdp_admin = input("Mot de passe : ")

# Hachage du mot de passe avec bcrypt
mdp_hash = bcrypt.hashpw(mdp_admin.encode(), bcrypt.gensalt())

# Insertion dans la table Users
sql = "INSERT INTO Users (nom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s)"
val = (nom_admin, email_admin, mdp_hash, "Staff")
curseur.execute(sql, val)
connection.commit()

print("Admin créé avec succès !")