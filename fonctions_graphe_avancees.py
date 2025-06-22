def creer_graphe_vide(n):
    return [[0] * n for _ in range(n)]

def ajouter_arete(MA, u, v):
    MA[u][v] = 1
    MA[v][u] = 1

def afficher_matrice(MA):
    print("\nMatrice d'adjacence :")
    for ligne in MA:
        print(" ".join(map(str, ligne)))

def afficher_voisins(MA, sommet):
    voisins = [i for i, val in enumerate(MA[sommet]) if val == 1]
    print(f"Les voisins de {sommet} sont : {voisins}")

def degre_sommet(MA, sommet):
    deg = sum(MA[sommet])
    print(f"Le degré du sommet {sommet} est : {deg}")

def ordre_graphe(MA):
    print(f"L'ordre du graphe est : {len(MA)} sommets.")

def taille_graphe(MA):
    taille = sum(sum(ligne) for ligne in MA) // 2
    print(f"La taille du graphe est : {taille} arêtes.")

def menu_terminal():
    MA = []
    while True:
        print("\n=== MENU GRAPHE ===")
        print("1. Créer une matrice vide")
        print("2. Ajouter une arête")
        print("3. Afficher la matrice")
        print("4. Afficher les voisins d’un sommet")
        print("5. Afficher le degré d’un sommet")
        print("6. Afficher l’ordre du graphe")
        print("7. Afficher la taille du graphe")
        print("0. Quitter")

        choix = input("Votre choix : ")
        if choix == "1":
            n = int(input("Nombre de sommets : "))
            MA = creer_graphe_vide(n)
            print(f" Matrice {n}x{n} créée.")
        elif choix == "2":
            if not MA:
                print(" Créez d'abord une matrice.")
                continue
            u = int(input("Sommet u : "))
            v = int(input("Sommet v : "))
            if 0 <= u < len(MA) and 0 <= v < len(MA):
                ajouter_arete(MA, u, v)
                print(f" Arête ({u}, {v}) ajoutée.")
            else:
                print(" Sommets invalides.")
        elif choix == "3":
            if not MA:
                print(" Aucune matrice à afficher.")
            else:
                afficher_matrice(MA)
        elif choix == "4":
            if not MA:
                print(" Aucune matrice.")
                continue
            s = int(input("Sommet : "))
            if 0 <= s < len(MA):
                afficher_voisins(MA, s)
            else:
                print(" Sommet invalide.")
        elif choix == "5":
            s = int(input("Sommet : "))
            if 0 <= s < len(MA):
                degre_sommet(MA, s)
            else:
                print(" Sommet invalide.")
        elif choix == "6":
            ordre_graphe(MA)
        elif choix == "7":
            taille_graphe(MA)
        elif choix == "0":
            print(" Fin du programme.")
            break
        else:
            print(" Choix invalide.")

menu_terminal()
