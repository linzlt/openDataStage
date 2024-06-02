import os
import pandas as pd
import matplotlib.pyplot as plt

# Définir le chemin du répertoire contenant les fichiers de données
CHEMIN_REPERTOIRE = "Output"

# Définir le chemin du répertoire pour sauvegarder les figures
chemin_figures = os.path.join(CHEMIN_REPERTOIRE, "figures")

# Vérifier si le répertoire "figures" existe, sinon le créer
if not os.path.exists(chemin_figures):
    os.makedirs(chemin_figures)

# Chemin du fichier CSV contenant les données
FICHIER_AXE_TEMPS = "Axe_du_temps/ESSAI_1_3_6.csv"
FICHIER_REF_DATA2 = "ACQUISITION FORGEAGE/ESSAI_114.csv"
# Charger les données du fichier CSV
df_axe_temps = pd.read_csv(FICHIER_AXE_TEMPS, delimiter=";")

# Sélectionner la dernière colonne "tps" comme axe du temps
axe_temps = df_axe_temps["tps"]

# Enregistrer l'axe du temps dans un nouveau fichier CSV
axe_temps.to_csv("Axe_du_temps/AXE_TEMPS.csv", index=False)

fichiers_non_coherents = []

# Récupérer les colonnes de référence pour chaque type de fichier
colonnes_reference1 = pd.read_csv(
    FICHIER_AXE_TEMPS, delimiter=";", nrows=0
).columns.tolist()
colonnes_reference2 = pd.read_csv(
    FICHIER_REF_DATA2, delimiter=";", nrows=0
).columns.tolist()

# Définir les plages d'essais selon la séquence spécifiée
plages_essais = [
    (26, 27),
    (31, 37),
    (41, 47),
    (51, 57),
    (61, 67),
    (71, 77),
    (81, 87),
    (91, 97),
    (101, 107),
    (111, 117),
    (121, 127),
]

for plage in plages_essais:
    debut, fin = plage
    for essai in range(debut, fin + 1):
        if essai == 113:
            continue
        # Construire le chemin complet du fichier CSV de l'essai
        nom_fichier = os.path.join(
            "ACQUISITION FORGEAGE", f"ESSAI_{str(essai).zfill(3)}.csv"
        )
        print(nom_fichier)
        print(os.getcwd())
        if os.path.exists(nom_fichier):
            print("exist")
            try:
                # Charger les données à partir du fichier CSV de l'essai à partir de la deuxième ligne
                df_essai = pd.read_csv(nom_fichier, delimiter=";", skiprows=0)
                print(df_essai)
                # Conversion des données en float
                for col in df_essai.columns:
                    if (
                        df_essai[col].dtype == "object"
                    ):  # Vérifier si le type de données est une chaîne de caractères
                        df_essai[col] = (
                            df_essai[col].str.replace(",", ".").astype(float)
                        )  # Convertir les virgules en points décimaux et les colonnes en float
                    elif (
                        df_essai[col].dtype == "float64"
                        and df_essai[col].isnull().any()
                    ):  # Vérifier si le type de données est float et s'il y a des NaN
                        df_essai[col] = df_essai[col].astype(
                            float
                        )  # Convertir les colonnes en float
                # Soustraire la première valeur de la colonne 9 pour chaque ligne
                if df_essai.shape[1] > 8:
                    df_essai.iloc[:, 8] = df_essai.iloc[:, 8] - df_essai.iloc[0, 8]

                # Trouver l'index de la dernière valeur non NaN dans les données
                dernier_index_non_nan = df_essai.apply(pd.Series.last_valid_index)

                # Trouver l'index le plus petit parmi les colonnes
                dernier_index = min(dernier_index_non_nan)

                # Tronquer l'axe des temps pour correspondre à la longueur de df_essai
                axe_temps_tronque = axe_temps[: dernier_index + 1]

                # Tronquer les données de chaque colonne à l'index de la dernière valeur non NaN
                df_essai_tronque = df_essai.iloc[: dernier_index + 1, :]

                # Extraction des données utiles
                df_essai = df_essai_tronque[: len(axe_temps_tronque)]

                for col in df_essai.columns:
                    # Tracer chaque courbe avec le nom de colonne correspondant
                    plt.plot(axe_temps_tronque, df_essai[col], label=col)

                # Ajouter des titres et des légendes
                plt.title(f"Essai {essai}")
                plt.xlabel("Temps")  # Définir le nom de l'axe x
                plt.ylabel("Valeurs")
                plt.legend(
                    loc="upper right", bbox_to_anchor=(1.3, 1.0)
                )  # Ajouter la légende avec les noms de colonnes

                # Afficher et sauvegarder le graphique dans le dossier "figures"
                plt.grid(True)
                nom_figure = os.path.join(
                    chemin_figures, f"ESSAI_{str(essai).zfill(3)}.png"
                )
                plt.savefig(nom_figure)
                plt.close()
            except FileNotFoundError:
                print("FileNotFoundError")
                continue  # Passer à l'essai suivant s'il n'y a pas de fichier pour cet essai


print("Les graphiques ont été générés avec succès.")
