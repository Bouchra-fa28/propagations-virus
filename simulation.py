import networkx as nx
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import messagebox

import tkinter.simpledialog as simpledialog
from matplotlib.patches import Patch

import tkinter.simpledialog as simpledialog
from matplotlib.patches import Patch

plt.ion()  # permet d’afficher les graphiques en temps réel

N = 50  #nombre de noeuds
G = nx.erdos_renyi_graph(N, 0.05) #cree un graph aleatoire , Chaque paire de nœuds a 5% de chance d’avoir une arête

edge_weights = {} # dictionnaire stocker les poids des arêtes


states = {node: "sain" for node in G.nodes} #initialisation d'etat des sommets a sain
color_map = {'sain': 'green', 'infecté': 'red', 'immunisé': '#0098F7'}
patient_zero = random.choice(list(G.nodes))
states[patient_zero] = "infecté" #patient zero est infecté
step_counter = [0]       #comteur de jours
infection_jours = {patient_zero: 0}  #dictionnaire calcule combien de jours le pation est infectee


nb_malades_a_vie = int(0.2 * N) # Sélection des 20% à rester infectés à vie
malades_a_vie = set(random.sample(list(G.nodes), nb_malades_a_vie))


fig, ax = plt.subplots(figsize=(6,6)) #cree la figur
pos = nx.spring_layout(G) #Calcule la position des nœuds dans l’espace

# supprimer les malades à vie
def supprimer_malades_a_vie():
    global G, states, infection_jours
    for node in malades_a_vie:
        if node in G:
            G.remove_node(node)
            states.pop(node, None)
            infection_jours.pop(node, None)
    messagebox.showinfo("Suppression", f"{len(malades_a_vie)} malades à vie supprimés.")
    afficher_etape(G, states, pos, step_counter[0])


#Identifier et vacciner les personnes les plus connectées dans le graphe
def vacciner_super_propagateurs(G, states, nb_vaccins=(0.20 * N)):#20% seront non immunises
    degres = sorted(G.degree, key=lambda x: x[1], reverse=True) #Trie les sommets par degré décroissant.
    for i in range(int(nb_vaccins)): #start le vaccine
        node = degres[i][0]
        states[node] = "immunisé"
    return states


#Guérison après 15 jours
#30% de chance aux voisins sains
def propagate_etape(G, states):
    new_states = states.copy()

    for node in G.nodes:
        if states[node] == "infecté":
            infection_jours[node] = infection_jours.get(node, 0) + 1

            if infection_jours[node] >= 15 and node not in malades_a_vie:
                new_states[node] = "immunisé"
                continue

            for neighbor in G.neighbors(node):
                if states[neighbor] == "sain" and random.random() < 0.3:
                    new_states[neighbor] = "infecté"
                    infection_jours[neighbor] = 0

    return new_states


#Afficher le graphe à l’étape
def afficher_etape(G, states, pos, step):
    ax.clear()
    colors = []

    for node in G.nodes:
        if states[node] == "infecté" and node in malades_a_vie and infection_jours.get(node, 0) >= 15:
            colors.append("white")
        else:
            colors.append(color_map.get(states[node], 'gray'))

    #  Titre avec infos
    titre = f"Propagation – {len(G.nodes)} personnes – Jour {step}"
    ax.set_title(titre, fontsize=15)

    #  Dessin du graphe
    nx.draw(G, pos, node_color=colors, with_labels=True, node_size=200, font_size=10, ax=ax)

    #  Ajouter légende
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', edgecolor='k', label='Sain'),
        Patch(facecolor='red', edgecolor='k', label='Infecté'),
        Patch(facecolor='#0098F7', edgecolor='k', label='Immunisé'),
        Patch(facecolor='white', edgecolor='k', label='Malade à vie')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    #  Dernier jour ?
    if all(
    states[n] != "infecté"
    for n in G.nodes
    if n not in malades_a_vie and G.degree[n] >= 1
):
     ax.text(0.5, -0.1, " Dernier jour de la propagation", transform=ax.transAxes,
            fontsize=12, color='black', ha='center')

    plt.draw()



def afficher_statistiques(states):
    total = len(states)
    sains = sum(1 for s in states.values() if s == "sain")
    infectes = sum(1 for s in states.values() if s == "infecté")
    immunises = sum(1 for s in states.values() if s == "immunisé")
    messagebox.showinfo("Statistiques",
        f"=== STATISTIQUES ===\n"
        f"Total d'individus : {total}\n"
        f"Sains : {sains}\n"
        f"Infectés : {infectes}\n"
        f"Immunisés : {immunises}")



def couper_connexion(G, u, v):
    if G.has_edge(u, v):
        G.remove_edge(u, v)
        messagebox.showinfo("Connexion supprimée", f"Connexion entre {u} et {v} supprimée.")



def detecter_Composantes_Connexes(G): #Utilise NetworkX pour trouver toutes les composantes connexes dans le graphe 
    composantes = list(nx.connected_components(G))
    info = f"Nombre de zones isolées : {len(composantes)}\n"
    for i, comp in enumerate(composantes):
        info += f"Zone {i+1} : {len(comp)} individus\n"
    messagebox.showinfo("Zones isolées", info)



def afficher_graphe(highlight=None):
    colors = []
    for node in G.nodes:
        if highlight and node in highlight:
            colors.append(highlight[node])
        else:
            colors.append(color_map.get(states[node], 'gray'))
    plt.figure(figsize=(8, 6))
    nx.draw(G, node_color=colors, with_labels=False, node_size=80)
    plt.title("Réseau social")
    plt.show()

def coloration_graphe():
    coloring = nx.coloring.greedy_color(G, strategy='largest_first')
    num_colors = len(set(coloring.values()))
    palette = plt.cm.tab20
    highlight = {node: palette(coloring[node] % 20) for node in coloring}

    #  Affichage du graphe
    plt.figure(figsize=(8, 6))
    nx.draw(G, node_color=[highlight[n] for n in G.nodes],
            with_labels=True, node_size=80)

    #  Créer la légende
    from matplotlib.patches import Patch
    used_colors = sorted(set(coloring.values()))
    legend_elements = [
        Patch(facecolor=palette(c % 20), label=f'Couleur {c}')
        for c in used_colors
    ]
    plt.legend(handles=legend_elements, loc='upper right', title="Coloration")

    plt.title(f"Coloration du graphe – {num_colors} couleurs utilisées")
    plt.show()

    messagebox.showinfo("Coloration", f"Coloration effectuée avec {num_colors} couleurs.")



#MST avec NeTworKS(algorithme de Kruskal ou Prim)
#relie tous les nœuds ensemble,
#sans aucun cycle,
#avec le poids total minimal
def arbre_couvrant_maximum():
    for u, v in G.edges:
        G[u][v]['weight'] = random.randint(1, 20) #poids aleatoire entre 1 et 20
    T = nx.maximum_spanning_tree(G, weight='weight')
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, node_color='lightgray', with_labels=True, node_size=200)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    nx.draw_networkx_edges(T, pos, edge_color='red', width=2)
    plt.title("Arbre couvrant minimal (MST)")
    plt.show()



# Algorithme equivalent a Dijkstra
def plus_court_chemin():
    try:
        #demend entrer les sommet
        s = simpledialog.askinteger("Sommet de départ", "Entrez le sommet de départ :")
        t = simpledialog.askinteger("Sommet d’arrivée", "Entrez le sommet d’arrivée :")
        
        #Vérifie que les sommets existent
        if s not in G.nodes or t not in G.nodes:
            messagebox.showerror("Erreur", "Un ou les deux sommets n'existent pas dans le graphe.")
            return

        #Donner un poids aléatoire entre 1 et 20 à chaque arête
        for u, v in G.edges:
            G[u][v]['weight'] = round(random.uniform(1, 20), 2)

        #Plus court chemin basé sur les poids
        path = nx.shortest_path(G, source=s, target=t, weight='weight')
        path_edges = list(zip(path[:-1], path[1:]))

        # Couleurs des nœuds
        colors = []
        for node in G.nodes:
            if node == s:
                colors.append('#0098F7')  # départ
            elif node == t:
                colors.append('white')    # arrivée
            elif node in path:
                colors.append("#77C9FC")  # sur le chemin
            else:
                colors.append('lightgray')

        #  Dessin du graphe avec poids affichés
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, node_color=colors, with_labels=True, node_size=400, font_size=10)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

        #  Étiquettes des poids
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        #  Légende
        legend_elements = [
            Patch(facecolor="#0098F7", edgecolor='k', label='Départ'),
            Patch(facecolor='white', edgecolor='k', label='Arrivée'),
            Patch(facecolor="#77C9FC", edgecolor='k', label='Sur le chemin'),
            Patch(facecolor='lightgray', edgecolor='k', label='Autres')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=8)

        total_length = round(sum(G[u][v]['weight'] for u, v in path_edges), 2)
        plt.title(f"Plus court chemin de {s} à {t} – Longueur totale : {total_length}")
        plt.show()

        messagebox.showinfo("Chemin trouvé", f"Chemin entre {s} et {t} :\n{path}\nLongueur totale : {total_length}")

    except nx.NetworkXNoPath:
        messagebox.showwarning("Pas de chemin", f"Aucun chemin entre {s} et {t}.")
    except TypeError:
        pass  # l’utilisateur a annulé



def flot_maximal():
    try:
        #entre les sommets
        s = simpledialog.askinteger("Source", "Entrez le sommet source :")
        t = simpledialog.askinteger("Puits", "Entrez le sommet puits :")

        #verification lexestance des noeuds
        if s not in G.nodes or t not in G.nodes:
            messagebox.showerror("Erreur", "Un ou les deux sommets n'existent pas dans le graphe.")
            return

        # Donner un poids aléatoire entre 1 et 20 à chaque arête
        for u, v in G.edges:
            poids = round(random.uniform(1, 20), 2)
            G[u][v]['weight'] = poids

        #cree un graphe oriente avec les capacites
        DG = nx.DiGraph()
        for u, v in G.edges:
            DG.add_edge(u, v, capacity=G[u][v]['weight'])
            DG.add_edge(v, u, capacity=G[u][v]['weight'])

        #calcul du flot maximum avec la fonction predefinie de FORD_FULKERSON
        flow_value, flow_dict = nx.maximum_flow(DG, s, t)

        edges_actives = [(u, v) for u in flow_dict for v, f in flow_dict[u].items() if f > 0]

        #  Couleurs
        node_colors = []
        for node in G.nodes:
            if node == s:
                node_colors.append('#FC6A6A')
            elif node == t:
                node_colors.append('red')
            else:
                node_colors.append('lightgray')

        #  Affichage
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=400)
        nx.draw_networkx_edges(G, pos, edgelist=edges_actives, edge_color='red', width=2)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        #  Légende
        legend_elements = [
            Patch(facecolor="#FC6A6A", edgecolor='k', label='Source'),
            Patch(facecolor='red', edgecolor='k', label='Puits'),
            Patch(facecolor='red', edgecolor='k', label='Arêtes utilisées'),
            Patch(facecolor='lightgray', edgecolor='k', label='Autres nœuds')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=8)

        plt.title(f"Flot maximal de {s} vers {t} = {flow_value}")
        plt.show()

        messagebox.showinfo("Flux maximal", f"Flux maximal entre {s} et {t} : {flow_value}")

    except nx.NetworkXError as e:
        messagebox.showwarning("Erreur de flux", str(e))
    except TypeError:
        pass  # utilisateur a annulé


#Remettre à zéro la simulation de propagation :on repart de l’état initial avec un nouveau patient zéro infecté.
def initialiser_simulation():
    global states, step_counter, infection_jours, patient_zero

    # Demander le patient zéro à l'utilisateur
    patient_zero = simpledialog.askinteger("Patient zéro", "Entrez l’ID du patient zéro :")

    if patient_zero not in G.nodes:
        messagebox.showerror("Erreur", "Ce sommet n'existe pas dans le graphe.")
        return

    states = {node: "sain" for node in G.nodes}
    states[patient_zero] = "infecté"
    infection_jours = {patient_zero: 0}
    step_counter[0] = 0

    afficher_etape(G, states, pos, step_counter[0])


def etape_suivante(event=None):
    global states, step_counter
    step_counter[0] += 1
    states = propagate_etape(G, states)
    afficher_etape(G, states, pos, step_counter[0])

# ===================== INTERFACE ======================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulation de propagation")
        self.geometry("600x700")
        self.configure(bg="#CDEDFC")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        bg_main = "#CDEDFC"
        bg_frame = "#E5F6FF"
        fg_text = "#203040"
        button_bg = "#469BD8"
        button_fg = "#FFFFFF"

        label_titre = tk.Label(self, text="Simulation de propagation",
                               font=("Helvetica", 18, "bold"), bg=bg_main, fg=fg_text)
        label_titre.grid(row=0, column=0, pady=20)

        frame = tk.Frame(self, bg=bg_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        for i in range(9):  # +1 ligne pour le nouveau bouton
            frame.grid_rowconfigure(i, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        boutons = [
            ("Lancer la simulation", initialiser_simulation),
            ("Couper une connexion", lambda: couper_connexion(G, *random.choice(list(G.edges)))),
            ("Composantes Connexes", lambda: detecter_Composantes_Connexes(G)),
            ("Coloration (radio)", coloration_graphe),
            ("MST (relais)", arbre_couvrant_maximum),
            ("Plus court chemin", plus_court_chemin),
            ("Flux max", flot_maximal),
            ("دفن المرضى", supprimer_malades_a_vie),  
            ("Réinitialiser avec patient zéro choisi", initialiser_simulation),

        ]

        for i, (texte, action) in enumerate(boutons):
            bouton = tk.Button(frame, text=texte, command=action,
                               font=("Arial", 13), bg=button_bg, fg=button_fg,
                               activebackground=bg_frame, padx=10, pady=8)
            bouton.grid(row=i, column=0, sticky="ew", padx=10, pady=5)

        bouton_quitter = tk.Button(self, text="Quitter", command=self.quit,
                                   font=("Arial", 13), bg="#FF6B6B", fg="white",
                                   activebackground="#C94F4F", padx=10, pady=10)
        bouton_quitter.grid(row=2, column=0, sticky="ew", padx=80, pady=20)

        self.bind('<Return>', etape_suivante)

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.mainloop()