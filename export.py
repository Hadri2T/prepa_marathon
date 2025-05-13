#Tout les imports nécessaires pour faire fonctionner le code
import os
import webbrowser
import json
import pandas as pd
from session import base_data, TRAINING

def export_html():
    # Charger les données JSON
    data = base_data()
    if not data["sessions"]:
        print("Aucune séance enregistrée.")
        return

    rows = []  # Liste de toutes les lignes du futur tableau

    for session in data["sessions"]:
        # Création d'une ligne vide avec les colonnes prévues
        row = {
            "Done": "✅" if session.get("done") else "❌",  # Emoji selon fait ou pas
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
    html_complete = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Tableau des séances</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Tableau des séances</h1>
        {html_table}
    </body>
    </html>
    """

    # Écriture dans le fichier HTML
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(html_complete)

    print("Fichier 'seances.html' généré avec style.")
    webbrowser.open("file://" + os.path.realpath(fichier))
