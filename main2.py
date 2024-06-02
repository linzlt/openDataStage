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

# Récupérer les colonnes de référence pour chaque type de fichier
colonnes_reference1 = pd.read_csv(
    FICHIER_AXE_TEMPS, delimiter=";", nrows=0
).columns.tolist()
colonnes_reference2 = pd.read_csv(
    FICHIER_REF_DATA2, delimiter=";", nrows=0
).columns.tolist()

# Définir les plages d'essais selon la séquence spécifiée
plages_essais = [
    (1,7),
    (11,17),
    (21,27),
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


def creer_repertoire(chemin):
    if not os.path.exists(chemin):
        os.makedirs(chemin)


def charger_donnees(nom_fichier):
    try:
        return pd.read_csv(nom_fichier, delimiter=";")
    except FileNotFoundError:
        print(f"FileNotFoundError: {nom_fichier} n'a pas été trouvé.")
        return None


def convertir_colonnes_en_float(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace(",", ".").astype(float)
        elif df[col].dtype == "float64" and df[col].isnull().any():
            df[col] = df[col].astype(float)
    return df


def tracer_et_sauvegarder_graphique(axe_temps_tronque, df_essai, essai, chemin_figures):
    for col in df_essai.columns:
        if col != df_essai.columns[4]:  # Exclure la 5ème colonne
            plt.plot(axe_temps_tronque, df_essai[col], label=col)
    plt.title(f"Essai {essai}")
    plt.xlabel("Temps")
    plt.ylabel("Valeurs")
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
    plt.grid(True)
    nom_figure = os.path.join(chemin_figures, f"ESSAI_{str(essai).zfill(3)}.png")
    plt.savefig(nom_figure)
    plt.close()


def traiter_fichier(df, axe_temps, essai, chemin_figures):
    df = convertir_colonnes_en_float(df)
    if df.shape[1] > 8:
        df.iloc[:, 8] -= df.iloc[0, 8]

    dernier_index_non_nan = df.apply(pd.Series.last_valid_index)
    dernier_index = min(dernier_index_non_nan)

    axe_temps_tronque = axe_temps[: dernier_index + 1]
    df_essai_tronque = df.iloc[: dernier_index + 1, :]
    df_essai = df_essai_tronque[: len(axe_temps_tronque)]

    tracer_et_sauvegarder_graphique(axe_temps_tronque, df_essai, essai, chemin_figures)


def main():
    creer_repertoire(chemin_figures)
    axe_temps = pd.read_csv(FICHIER_AXE_TEMPS, delimiter=";")["tps"]

    for debut, fin in plages_essais:
        for essai in range(debut, fin + 1):
            if essai == 113:
                continue
            nom_fichier = os.path.join(
                "ACQUISITION FORGEAGE", f"ESSAI_{str(essai).zfill(3)}.csv"
            )
            print(f"Traitement de {nom_fichier}")
            df_essai = charger_donnees(nom_fichier)
            if df_essai is not None:
                traiter_fichier(df_essai, axe_temps, essai, chemin_figures)

    print("Les graphiques ont été générés avec succès.")


if __name__ == "__main__":
    main()
