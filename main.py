import mysql.connector
import re
import bcrypt

print("Connexion à la base de données...")

connection = mysql.connector.connect(
    host="localhost",
    user="MariamHarouna",
    password="Simplon@2025",
    database="helpdeskdb"
)

curseur = connection.cursor()
print("Connecté à MySQL avec succès")


def creer_ticket(utilisateur):
    user_id = utilisateur["id"]
    titre = input("Titre : ")
    description = input("Description : ")
    urgence = input("Niveau d'urgence : ")

    requete = """
        INSERT INTO ticket (user_id,titre, description, niveau_urgence)
        VALUES (%s, %s, %s, %s)
    """
    curseur.execute(requete, (user_id,titre, description, urgence))
    connection.commit()
    print("Ticket crée avec succès.")

def lister_ticket_x(id):
    query = "SELECT nom,titre,description,niveau_urgence,statut FROM Users u JOIN ticket t ON u.id = t.user_id WHERE t.user_id = %s "
    curseur.execute(query,(id,))
    resultat = curseur.fetchall()
    if not resultat:
       print(f"Aucun ticket trouvé pour cet identifiant {id}")
       return False
    
    print("\n--- MES TICKETS ---")
    for t in resultat:
        print(f"Nom:{t[0]} |Titre: {t[1]} | Description:{t[2]} | Niveau d'urgence:{t[3]} | Statut:{t[4]}")



def lister_tous_les_ticket():
    query = "SELECT t.id , u.nom,t.titre,t.description,t.niveau_urgence,t.statut FROM Users u JOIN ticket t ON u.id = t.user_id WHERE u.role = 'Apprenant' ORDER BY u.nom "
    curseur.execute(query)
    resultat = curseur.fetchall()
    if not resultat:
       print("Aucun ticket en demande pour le moment.")
       return False
    print("\n--- LISTE DES TICKETS ---")
    
    utilisateur_actuel = None

    for id, nom, titre, description, niveau, statut in resultat:

        if nom != utilisateur_actuel:
            utilisateur_actuel = nom
            print(f"\n Utilisateur : {nom}")
            print("-" * 40)
            
        print(f" Id ticket:       |{id}")
        print(f" Titre        | {titre}")
        print(f" Description  | {description}")
        print(f" Urgence      | {niveau}")
        print(f" Statut       | {statut}")
        print("------------------------------")

    return True
   
# FONCTION RECHERCHE
def suivi_demande(id):
    query = "SELECT id,titre, statut FROM ticket where id = %s "
    curseur.execute(query,(id,))
    resultat = curseur.fetchone()
    if resultat:
     print(f"ID:{resultat[0]} | Titre:{resultat[1]} | Statut:{resultat[2]}")
    else:
       print("Aucun ticket de cet identifiant")


def modifier_statut_ticket():
    nom = input("Entrez votre nom:")
    id_ticket = int(input("ID du ticket : "))
    statut = input("Nouveau statut:")
    query = "UPDATE Users u JOIN ticket t ON u.id = t.user_id  SET t.statut = %s  WHERE u.nom = %s AND t.id = %s "
    curseur.execute(query, (statut, nom, id_ticket))
    connection.commit()
    return curseur.rowcount > 0
    #print("Statut mise à jour.")

def Afficher_apprenants():
   query = "SELECT id, nom FROM Users WHERE role = 'Apprenant' "
   curseur.execute(query)
   resultat = curseur.fetchall()
   for r in resultat:
       print(f"\n ID:{r[0]} | Nom:{r[1]} |")
      



def supprimer_users():
    id = int(input("ID de l'apprenant à supprimer : "))
    requete = "DELETE FROM Users WHERE id = %s"
    curseur.execute(requete, (id,))
    connection.commit()
    print("Apprenant(e) supprimé(e).")



def logout():
   global utilisateur_connecte
   
   utilisateur_connecte = None
   print("Déconnexion reussie !")
   return


# ====================================== FONCTION INSCRIPTION ==================================
def inscription():
 print("\n===== INSCRIPTION =====")

 while True: 
  nom = input("Entrer votre nom: ").strip()
  if not all(c.isalpha() or c in " -'" for c in nom):
    print(f"Nom '{nom}' invalide. Seules les lettres, espaces, '-' et apostrophe (') sont autorisés.")
  else:
    break  
 
 while True:  
  
  email= input("Entrez votre email: ")

  pattern = r"^(?=(?:.*[a-z]){3,})[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
  if not re.match(pattern, email.lower()):
    print("Adresse email invalide.")
  else:
     break

 password = input("Saisir un mode de passe: ")

 hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


 query = "INSERT INTO Users (nom ,email,mot_de_passe) VALUES (%s,%s,%s) "
 curseur.execute(query,(nom,email,hashed))
 connection.commit()
 print("Inscription reussie !")



   

#==================================== FONCTION MENU ADMINISTRATEUR ======================================
def menu_staff(utilisateur):
   
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Voir la liste des apprenants")
        print("2. Lister tous les tickets")
        print("3. Modifier etat ticket")
        print("4. Suivi statut d'une demande")
        print("5. Supprimer un apprenant")
        print("6. Inscrire nouveau apprenant")
        print("0. Déconnexion")
       

        choix = input("Votre choix : ")
        match choix:

         case "1":
            Afficher_apprenants()
         case "2":
            lister_tous_les_ticket()
         case "3":
            modifier_statut_ticket()
         case "4":   
            id = input("Entrez identifiant du ticket: ")
            suivi_demande(id)
         case "5":
           supprimer_users()  
         case "6":
           inscription()    
         case "0":
            logout()
            break
         case _:
            print("Choix invalide.")


#==================================== FONCTION MENU UTILISATEUR ======================================


def menu_user(utilisateur):
    while True:
        print("\n===== MENU ASSISTANCE =====")
        print("1. Créer un ticket")
        print("2. Suivi etat de demande") 
        print("3. Historique des demandes")
        print("0. Déconnexion")

        choix =  input("Votre choix : ")

        match choix :
           
         case "1":
            creer_ticket(utilisateur)
         case"2":
            id = input("Entrez l'identifiant du ticket: ")
            suivi_demande(id)
         case "3":
            lister_ticket_x(utilisateur["id"])    
         case"0":
           logout()  
           break
         case _:
            print("Choix invalide.")



# FONCTION AUTHENTIFICATION COMMENCE ICI 

def login():
 
 while True:    
    print("\n===== CONNEXION =====")

    email = input("Entrez votre email: ").strip()
    password = input("Mot de passe: ").strip()

    query = "SELECT id, nom, mot_de_passe, role FROM Users WHERE email = %s"
    curseur.execute(query, (email,))
    resultat = curseur.fetchone()

    if not resultat:
        print("Email incorrect.")
        return None

    user_id = resultat[0]
    nom = resultat[1]
    hashed_password = resultat[2]
    role = resultat[3]

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        print("Connexion réussie!")

        return {
            "id": user_id,
            "nom": nom,
            "role": role
        }

    else:
        print("Mot de passe incorrect")
        return None

#=========================================  MENU PRINCIPALE ===============================================

while True:
 utilisateur_connecte = None
 print("\n===== BIENVENUE AU SERVICE D'ASSISTANCE UNIVERSITAIRE =====")
 print("\n1.CONNECTEZ-VOUS")
 print("0.Quitter")

 choix = input("Entrez une option:")

 match choix:

  case "1":
   utilisateur_connecte = login()
   if utilisateur_connecte :
      if utilisateur_connecte["role"] == "Staff":
         menu_staff(utilisateur_connecte)
      elif utilisateur_connecte["role"] == "Apprenant":
         menu_user(utilisateur_connecte)   
  case "0":
    print("À bientot")
    break
  case _:
    print("Saisie invalide!") 

 # FONCTION AUTHENTIFICATION TERMINE ICI 
      


#curseur.close()
#connection.close()

