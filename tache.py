import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# Fonction pour ajouter des tâches
def ajouter_tache():
    description = entry_description.get()  # Récupère la description depuis le champ de saisie
    date = entry_date.get()  # Récupère la date depuis le champ de saisie
    notes = entry_notes.get("1.0", "end-1c")  # Récupère les notes depuis le widget Text
    if description and date:  # Vérifie que la description et la date ne sont pas vides
        # Insère une nouvelle ligne dans le Treeview avec description, date, statut et notes
        tree.insert("", "end", values=(description, date, "Non commencé", notes))
        # Efface les champs après l'ajout
        entry_description.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_notes.delete("1.0", tk.END)

# Fonction pour supprimer une tâche
def supprimer_tache():
    selected_item = tree.selection()  # Obtient l'élément sélectionné dans le Treeview
    if selected_item:
        tree.delete(selected_item)  # Supprime l'élément sélectionné
    else:
        messagebox.showinfo("Information", "Veuillez sélectionner une tâche à supprimer.")  # Affiche une boîte de dialogue d'information

# Fonction pour mettre à jour le statut d'une tâche
def update_status(status):
    selected_item = tree.selection()  # Obtient l'élément sélectionné dans le Treeview
    if selected_item:
        values = tree.item(selected_item)["values"]  # Obtient les valeurs de l'élément sélectionné
        tree.item(selected_item, values=(values[0], values[1], status, values[3]))  # Met à jour le statut de la tâche
    else:
        messagebox.showinfo("Information", "Veuillez sélectionner une tâche à mettre à jour.")  # Affiche une boîte de dialogue d'information

# Fonction pour sauvegarder la liste de tâches dans un fichier CSV
def sauvegarder_liste_csv(liste_taches, nom_fichier):
    with open(nom_fichier, 'w', newline='') as csvfile:
        fieldnames = ["Description", "Date d'échéance", "Statut", "Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Écrit la ligne d'en-tête dans le fichier CSV
        for item in tree.get_children():
            values = tree.item(item)["values"]
            tache = {
                "Description": values[0],
                "Date d'échéance": values[1],
                "Statut": values[2],
                "Notes": values[3]
            }
            writer.writerow(tache)  # Écrit chaque tâche dans le fichier CSV

# Fonction pour charger la liste de tâches depuis un fichier CSV
def charger_liste_csv(nom_fichier):
    try:
        with open(nom_fichier, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                notes = row.get("Notes", "")  # Assurez-vous de traiter les notes si elles sont présentes dans le CSV
                tree.insert("", "end", values=(row["Description"], row["Date d'échéance"], row["Statut"], notes))
    except FileNotFoundError:
        pass  # Ignore l'erreur si le fichier n'existe pas

# Fonction pour charger les tâches à partir d'un fichier CSV
def charger_taches():
    fichier_csv = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
    if fichier_csv:
        tree.delete(*tree.get_children())  # Efface toutes les tâches actuellement affichées
        charger_liste_csv(fichier_csv)  # Charge les tâches à partir du fichier CSV sélectionné

# Fonction pour sauvegarder les tâches dans un fichier CSV
def sauvegarder_taches():
    sauvegarder_liste_csv(tree.get_children(), "taches.csv")  # Sauvegarde les tâches actuelles dans un fichier CSV

# Fonction pour trier les tâches par date
def trier_par_date():
    l = [(tree.set(k, "Date d'échéance"), k) for k in tree.get_children('')]  # Trie les tâches par date
    l.sort()
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)  # Déplace les tâches dans l'ordre trié

root = tk.Tk()
root.title("Gestionnaire de Tâches")
root.geometry("700x600")

frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), padx=20, pady=(20, 0))

lbl_description = ttk.Label(frame_input, text="Description:")
lbl_description.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
entry_description = ttk.Entry(frame_input, width=30)
entry_description.grid(row=0, column=1, padx=(0, 20))

lbl_date = ttk.Label(frame_input, text="Date d'échéance:")
lbl_date.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky=tk.W)
entry_date = ttk.Entry(frame_input, width=30)
entry_date.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))

lbl_notes = ttk.Label(frame_input, text="Notes:")
lbl_notes.grid(row=2, column=0, padx=(0, 10), pady=(10, 0), sticky=tk.W)
entry_notes = tk.Text(frame_input, width=30, height=5)
entry_notes.grid(row=2, column=1, padx=(0, 20), pady=(10, 0))

btn_ajouter = ttk.Button(frame_input, text="Ajouter", command=ajouter_tache)
btn_ajouter.grid(row=3, column=0, columnspan=2, pady=20)

tree = ttk.Treeview(root, columns=("Description", "Date d'échéance", "Statut", "Notes"), show="headings")
tree.heading("Description", text="Description")
tree.heading("Date d'échéance", text="Date d'échéance")
tree.heading("Statut", text="Statut")
tree.heading("Notes", text="Notes")
tree.grid(row=1, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), padx=20, pady=20)

scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scroll.grid(row=1, column=1, sticky=(tk.N + tk.S + tk.W))
tree.configure(yscrollcommand=scroll.set)

frame_manage = ttk.Frame(root, padding="10")
frame_manage.grid(row=2, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), padx=20, pady=(0, 20))

btn_supprimer = ttk.Button(frame_manage, text="Supprimer", command=supprimer_tache)
btn_supprimer.pack(side=tk.LEFT, padx=10)

btn_encours = ttk.Button(frame_manage, text="En cours", command=lambda: update_status("En cours"))
btn_encours.pack(side=tk.LEFT, padx=10)

btn_terminé = ttk.Button(frame_manage, text="Terminé", command=lambda: update_status("Terminé"))
btn_terminé.pack(side=tk.LEFT, padx=10)

btn_noncommencé = ttk.Button(frame_manage, text="Non commencé", command=lambda: update_status("Non commencé"))
btn_noncommencé.pack(side=tk.LEFT, padx=10)

btn_trier = ttk.Button(frame_manage, text="Trier par Date", command=trier_par_date)
btn_trier.pack(side=tk.LEFT, padx=10)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

btn_charger = ttk.Button(root, text="Charger", command=charger_taches)
btn_charger.grid(row=3, column=0, pady=10)

btn_sauvegarder = ttk.Button(root, text="Sauvegarder", command=sauvegarder_taches)
btn_sauvegarder.grid(row=4, column=0, pady=10)

root.mainloop()
