# Tout les fonctions liées à mes séances de sport

# stocker les séances en format JSON, et pouvoir entrer des dates
import json
from datetime import datetime
import pandas as pd
import os
import webbrowser
import locale
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
from datetime import datetime, timedelta


# Variable constante dans laquelle est stockées les séances
TRAINING = "training_data.json"

#Dictionnaire pour entrer/modifier mes entrainements de salles
ENTRAINEMENTS_SALLE = {
    "A": [
        {"exercice": "Développé couché", "repos": "120s"},
        {"exercice": "Tirage horizontal", "repos": "90s"},
        {"exercice": "Élévations latérales", "repos": "60s"},
        {"exercice": "Superstet", "repos" : "30s"}
    ],
    "B": [
        {"exercice": "Squat", "repos": "120s"},
        {"exercice": "Fentes", "repos": "90s"},
        {"exercice": "Mollets debout", "repos": "60s"},
        {"exercice": "Superstet", "repos" : "30s"}
    ],
    "C": [
        {"exercice": "Soulevé de terre", "repos": "120s"},
        {"exercice": "Hip thrust", "repos": "90s"},
        {"exercice": "Crunchs", "repos": "60s"},
        {"exercice": "Superstet", "repos" : "30s"}
    ]
}

"""
Definition de la fonction de base :
- Vérifie si le fichier training_data.json existe
    - Si oui, lire le contenu et le convertir en dict
    - Si non, le créer automatiquement avec une liste dans un dict
- Empêche que le programme plante
    - Evite le FileNotFoundError
"""
def base_data():
    try:
        with open(TRAINING, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"sessions": []}
        with open(TRAINING, "w") as file_new:
            json.dump(data, file_new, indent=2)
    return data

"""
Définition de la fonction pour une nouvelle session de sport:
    - Pour toutes les sessions : demander le type, la date, un commentaire, et si je l'ai faite ou pas
    - Pour la course : ajouter le temps et le nombre de kilomètres et en déduire l'allure
    - Pour la salle : les exercices
    - Pour les autres : juste le type
"""
def new_session():

    #Utiliser exit pour retourner au menu
    session_type = input("Type de séance : ").lower()
    if session_type == "exit" or session_type == "":
        print("Ajout annulé.")
        return

    while True:
        raw_date = input("Date : ").strip().lower()

        if raw_date in ["", "auj"]:
            date_obj = datetime.today()
            break
        elif raw_date == "hier":
            date_obj = datetime.today() - timedelta(days=1)
            break
        else:
            try:
                date_obj = datetime.strptime(raw_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Format invalide. Utilise jj-mm-aaaa, ou 'auj' / 'hier'")

    date = date_obj.strftime("%A %d %B %Y")


    commentaires = input("Commentaires : ")
    #done = input("Séance faite ? ").lower() == "y"
    #Pas envie d'avoir la colonne done finalement

    if session_type == "course":
        while True:
            distance_input = input("Distance : ")
            try:
                distance = float(distance_input)
                break
            except ValueError:
                print("Entrée invalide. Entrer un nombre sans unité")

        while True:
            time_str = input("Temps (hh:mm:ss) : ")
            try:
                h, m, s = map(int, time_str.strip().split(":"))
                break
            except ValueError:
                print("Format hh:mm:ss nécessaire")

        minutes = h * 60 + m + s / 60
        pace = round(minutes / distance, 2)

        if minutes > 90:
            allure = "Sortie longue"
        elif pace > 5.30:
            allure = "EF"
        else:
            allure = "Fractionné"



        session = {
            #"done": done,
            #Pas envie d'avoir la colonne done finalement
            "date": date,
            "type": "course",
            "distance": distance,
            "time": time_str,
            "pace": pace,
            "commentaires": f"{allure}, {commentaires}"
        }

    elif session_type == "salle":

        #Demander quel entrainement je fais aujourd'hui
        entrainement = input("Entrainement du jour ? : ").upper()
        #Mettre A, B ou C

        if entrainement not in ENTRAINEMENTS_SALLE:
            print("Entrainement non reconnu")
            return

        # Liste pour stocker les exercices avec charges et répétitions
        exercices = []

        # Parcourt chaque exercice prévu dans l'entraînement choisi
        for exercice in ENTRAINEMENTS_SALLE[entrainement]:
            #Enter la charge et le nombre de répétitions
            charge = input(f"{exercice['exercice']} - Charge : ")
            repetitions = input(f"{exercice['exercice']} - Répétitions : ")

            #Ajoute l'exercice à la liste
            exercices.append({
                "exercice": exercice["exercice"],
                "charge": charge,
                "repetitions": repetitions,
                "repos": exercice["repos"]
            })

        session = {
            #"done": done,
            #Pas envie d'avoir la colonne done finalement
            "date": date,
            "type": "salle",
            "exercices": exercices,
            "entrainement": entrainement,
            "commentaires": commentaires
        }

    else:
        session = {
            #"done": done,
            #Pas envie d'avoir la colonne done finalement
            "date": date,
            "type": session_type,
            "commentaires": commentaires
        }

    data = base_data()
    data["sessions"].append(session)
    with open(TRAINING, "w") as write_file:
        json.dump(data, write_file, indent=2)
    print("Séance ajoutée.")

"""
Fonction pour supprimer une session de sport si jamais je fais une erreur
"""
def delete_session():
    data = base_data()
    sessions = data["sessions"]
    if not sessions:
        print("Aucune séance à supprimer.")
        return
    print("\nListe des séances enregistrées :\n")
    for i, session in enumerate(sessions):
        desc = f"{session.get('date', '')} – {session.get('type', '').capitalize()} – {session.get('commentaires', '')[:30]}"
        print(f"{i+1}. {desc}")
    try:
        choix = int(input("\nNuméro de la séance à supprimer : "))
        if choix == 0:
            print("Suppression annulée.")
            return
        elif 1 <= choix <= len(sessions):
            confirm = input(f"Supprimer la séance n°{choix} ? (y/n) : ").lower()
            if confirm == "y":
                sessions.pop(choix - 1)
                with open(TRAINING, "w") as f:
                    json.dump(data, f, indent=2)
                print("Séance supprimée avec succès.")
            else:
                print("Suppression annulée.")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Entrée non valide.")

"""
Fonction pour afficher les séances dans un tableau HTML
"""
def export_html():
    data = base_data()
    if not data["sessions"]:
        print("Aucune séance enregistrée.")
        return
    df = pd.DataFrame(data["sessions"])
    fichier = "seances.html"
    df.to_html(fichier, index=False)
    print("Fichier 'seances.html' généré.")
    webbrowser.open("file://" + os.path.realpath(fichier))

"""
Fonction pour modifier une session de sport en cas d'erreur
"""
def edit_session():
    data = base_data()
    sessions = data["sessions"]
    if not sessions:
        print("Aucune séance à modifier.")
        return
    print("\nListe des séances enregistrées :\n")
    for i, session in enumerate(sessions):
        desc = f"{session.get('date', '')} – {session.get('type', '').capitalize()} – {session.get('commentaires', '')[:30]}"
        print(f"{i+1}. {desc}")
    try:
        choix = int(input("\nNuméro de la séance à modifier : "))
        if choix == 0:
            print("Modification annulée.")
            return
        elif 1 <= choix <= len(sessions):
            session = sessions[choix - 1]
            print("\nModification des champs : (laisser vide pour conserver la valeur actuelle)\n")
            for key in session:
                current = session[key]
                if isinstance(current, list) and key == "exercices":
                    print("\nListe d'exercices actuelle :")
                    for idx, ex in enumerate(current):
                        print(f"{idx + 1}. {ex['exercice']} – Charge: {ex['charge']} – Répétitions: {ex['repetitions']} – Repos: {ex['repos']}")
                    print("\nQue veux-tu faire ?")
                    print("1 - Modifier un exercice")
                    print("2 - Supprimer un exercice")
                    print("3 - Ajouter un exercice")
                    print("4 - Passer")
                    action = input("Choix : ").strip()
                    if action == "1":
                        ex_num = int(input("Numéro de l'exercice à modifier : ")) - 1
                        if 0 <= ex_num < len(current):
                            exo = current[ex_num]
                            for field in ["exercice", "charge", "repetitions", "repos"]:
                                val = input(f"{field} (actuel : {exo[field]}) : ")
                                if val:
                                    exo[field] = val
                    elif action == "2":
                        ex_num = int(input("Numéro de l'exercice à supprimer : ")) - 1
                        if 0 <= ex_num < len(current):
                            del current[ex_num]
                            print("Exercice supprimé.")
                    elif action == "3":
                        nom = input("Exercice : ")
                        charge = input("Charge : ")
                        repetitions = input("Répétitions : ")
                        repos = input("Repos : ")
                        current.append({
                            "exercice": nom,
                            "charge": charge,
                            "repetitions": repetitions,
                            "repos": repos
                        })
                        print("Exercice ajouté.")
                    else:
                        print("Aucun changement sur les exercices.")
                    continue
                new_value = input(f"{key} (actuel : {current}) : ")
                if new_value != "":
                    if isinstance(current, bool):
                        session[key] = new_value.lower() == "y"
                    elif isinstance(current, float):
                        try:
                            session[key] = float(new_value)
                        except ValueError:
                            print(f"Valeur invalide pour {key}, inchangée.")
                    else:
                        session[key] = new_value
            with open(TRAINING, "w") as f:
                json.dump(data, f, indent=2)
            print("Séance modifiée avec succès.")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Entrée non valide.")
