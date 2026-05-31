import os
import pandas as pd
import matplotlib.pyplot as plt


CHEMIN_REPERTOIRE = "Output"

chemin_figures = os.path.join(CHEMIN_REPERTOIRE, "figures")

if not os.path.exists(chemin_figures):
    os.makedirs(chemin_figures)


FICHIER_AXE_TEMPS = "Axe_du_temps/ESSAI_1_3_6.csv"
FICHIER_REF_DATA2 = "ACQUISITION FORGEAGE/ESSAI_114.csv"

df_axe_temps = pd.read_csv(FICHIER_AXE_TEMPS, delimiter=";")

axe_temps = df_axe_temps["tps"]
axe_temps.to_csv("Axe_du_temps/AXE_TEMPS.csv", index=False)


colonnes_reference1 = pd.read_csv(
    FICHIER_AXE_TEMPS, delimiter=";", nrows=0
).columns.tolist()
colonnes_reference2 = pd.read_csv(
    FICHIER_REF_DATA2, delimiter=";", nrows=0
).columns.tolist()

plages_essais = [
    (101, 107),
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

    dernier_index_non_nan = df.apply(lambda col: col.last_valid_index()).min()

    axe_temps_tronque = axe_temps[: dernier_index_non_nan + 1]
    df_essai_tronque = df.iloc[: dernier_index_non_nan + 1, :]
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
