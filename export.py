#Tout les imports nécessaires pour faire fonctionner le code
import os
import webbrowser
import json
import pandas as pd
from session import base_data, TRAINING
from datetime import datetime, timedelta

def export_html():
    # Charger les données JSON
    data = base_data()
    if not data["sessions"]:
        print("Aucune séance enregistrée.")
        return

    # Calculer la date 7 jours avant aujourd'hui
    aujourd_hui = datetime.today()
    semaine_dernière = aujourd_hui - timedelta(days=7)

    # Calcul de la distance totale couru sur les 7 derniers jours
    distance_totale = 0.0
    for session in data["sessions"]:
        if session.get("type") == "course":
            try:
                session_date = datetime.strptime(session.get("date"), "%A %d %B %Y")
                if semaine_dernière <= session_date <= aujourd_hui:
                    distance_totale += float(session.get("distance", 0))
            except Exception:
                pass  # ignore les erreurs de parsing de date


    # Calcul du nombre de séances de salle sur les 7 derniers jours
    nb_salle = 0
    for session in data["sessions"]:
        if session.get("type") == "salle":
            try:
                session_date = datetime.strptime(session.get("date"), "%A %d %B %Y")
                if semaine_dernière <= session_date <= aujourd_hui:
                    nb_salle += 1
            except Exception:
                pass


    rows = []  # Liste de toutes les lignes du futur tableau

    for session in data["sessions"]:
        # Création d'une ligne vide avec les colonnes prévues
        row = {
            #"Done": "✅" if session.get("done") else "❌"
            #Pas envie d'avoir la colonne done finalement
            "Date": session.get("date", ""),
            "Course": "",  # Initialement vide
            "Salle": "",
            "Autre": ""
        }

        # Si c'est une séance de course, on remplit la colonne "Course"
        if session["type"] == "course":
            row["Course"] = (
                                f"<b>Distance :</b> {session.get('distance', '')} km<br>"
                                f"<b>Temps :</b> {session.get('time', '')}<br>"
                                f"<b>Allure :</b> {session.get('pace', '')} min/km<br>"
                                f"<b>Commentaires :</b> {session.get('commentaires', '')}"
                            )



        # Si c'est une séance de salle, on remplit la colonne "Salle"
        elif session["type"] == "salle":
            exercices = session.get("exercices", [])
            details = "<br><br>".join(
                f"<b>{exo['exercice']}</b><br>"
                f"Charge : {exo['charge']}<br>"
                f"Répétitions : {exo['repetitions']}<br>"
                f"Repos : {exo['repos']}"
                for exo in exercices
            )
            row["Salle"] = (
                f"{details}<br><br>"
                f"<b>Type :</b> {session.get('entrainement', '')}<br>"
                f"<b>Commentaires :</b> {session.get('commentaires', '')}"
)



        # Sinon, on place l’info dans la colonne "Autre"
        else:
            row["Autre"] = (
                f"<b>{session.get('type', '').capitalize()}</b><br>"
                f"{session.get('commentaires', '')}"
)

        rows.append(row)  # Ajout de la ligne complète à la liste

    # Création du DataFrame à partir de toutes les lignes
    df = pd.DataFrame(rows)

    # Chemin du fichier HTML
    fichier = "seances.html"

    # Export du tableau HTML (sans l'en-tête HTML complet)
    html_table = df.to_html(index=False, escape=False)

    # Contenu HTML complet avec lien CSS
    html_complet = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Tableau des séances</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Tableau des séances</h1>
        <h3 style='text-align:center'>
    Nombre de km courus cette semaine : {distance_totale:.2f} km
    </h3>
    <h3 style='text-align:center'>
    Nombre de séances de salle cette semaine : {nb_salle}
    </h3>

        {html_table}
    </body>
    </html>
    """


    # Écriture dans le fichier HTML
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(html_complet)

    print("Fichier 'seances.html' généré avec style.")
    webbrowser.open("file://" + os.path.realpath(fichier))
