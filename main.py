#Importer les sessions, et l'export en HTML
from session import new_session, edit_session, delete_session
from export import export_html

#Créer le menu pour se déplacer
if __name__ == "__main__":
    while True:
        print("\nMenu principal")
        print("1 - Ajouter une séance")
        print("2 - Exporter en HTML")
        print("3 - Supprimer une séance")
        print("4 - Modifier une séance")
        print("5 - Quitter")

        choix = input("Choix : ").strip()

        if choix == "1":
            new_session()
        elif choix == "2":
            export_html()
        elif choix == "3":
            delete_session()
        elif choix == "4":
            edit_session()
        elif choix == "5":
            print("Au revoir")
            break
        else:
            print("Choix invalide.")

