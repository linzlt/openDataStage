import os
from multiprocessing import Pool
import time
import pandas as pd
import matplotlib.pyplot as plt


def creer_dossier_si_non_existant(chemin):
    if not os.path.exists(chemin):
        os.makedirs(chemin)


def charger_donnees(chemin, delimiter=","):
    try:
        df = pd.read_csv(chemin, delimiter=delimiter)
    except pd.errors.ParserError as e:
        print(
            f"Une erreur de parsing est survenue lors de la lecture du fichier {chemin}: {e}"
        )
        df = pd.DataFrame()
    return df


chemins_fichiers = [
    "AXE_DU_TEMPS/ESSAI_1_3_6.csv",
    "ACQUISITION FORGEAGE/ESSAI_033.csv",
    "ACQUISITION FORGEAGE/ESSAI_026.csv",
    "ACQUISITION FORGEAGE/ESSAI_037.csv",
]

# Lecture de chaque fichier
for chemin_fichier in chemins_fichiers:
    print(f"Lecture du fichier : {chemin_fichier}")
    df = charger_donnees(chemin_fichier)
    print("Intermediate df_numeric:\n", df)


def tronquer_donnees(df, axe_temps):
    # Convertir toutes les valeurs en numérique, les erreurs sont forcées en NaN
    df_numeric = df.apply(pd.to_numeric, errors="coerce")
    print("Intermediate df_numeric:\n", df_numeric)

    # Trouver le dernier index non-NaN pour chaque colonne, puis prendre le maximum de ces index
    dernier_index_non_nan = df_numeric.apply(lambda col: col.last_valid_index()).max()
    if pd.isna(dernier_index_non_nan):
        raise ValueError("Dataframe contains only NaN values")
    dernier_index_non_nan = int(dernier_index_non_nan)

    # Tronquer les données
    df_tronque = df_numeric.iloc[: dernier_index_non_nan + 1].dropna(axis=1, how="all")
    axe_temps_tronque = axe_temps.iloc[: dernier_index_non_nan + 1].astype(float)

    return df_tronque, axe_temps_tronque


def convertir_colonnes_float(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace(",", ".").astype(float)
        elif df[col].dtype == "float64" and df[col].isnull().any():
            df[col] = df[col].astype(float)
    return df


def tracer_courbes(col_index, df, axe_temps, chemin_figures):
    for col in enumerate(df.columns):
        if col != enumerate(df.columns[4]):
            plt.plot(axe_temps[: len(df[col])], df[col], label=col)
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    filename = os.path.join(chemin_figures, f"ESSAI_{col_index:03d}.png")
    plt.savefig(filename)
    plt.close()


def ajuster_colonne_9(df):
    # Vérifier que la colonne 9 existe
    if df.shape[1] > 8:
        # Soustraire la première valeur de la colonne 9 pour chaque ligne
        df.iloc[:, 8] = df.iloc[:, 8] - df.iloc[0, 8]
    return df


def traiter_fichier(essai):
    nom_fichier = os.path.join(
        "ACQUISITION FORGEAGE", f"ESSAI_{str(essai).zfill(3)}.csv"
    )
    if os.path.exists(nom_fichier):
        df_essai = charger_donnees(nom_fichier)
        if df_essai is not None:
            df_essai, axe_temps_tronque = tronquer_donnees(df_essai, axe_temps)
            df_essai = convertir_colonnes_float(df_essai)
            df_essai = ajuster_colonne_9(df_essai)
            tracer_courbes(essai, df_essai, axe_temps_tronque, chemin_figures)


def main():
    start_time = time.time()  # Capture du temps de début
    chemin_repertoire = "Output"
    chemin_figures = os.path.join(chemin_repertoire, "figures")
    creer_dossier_si_non_existant(chemin_figures)

    FICHIER_AXE_TEMPS = "AXE_DU_TEMPS/ESSAI_1_3_6.csv"
    df_axe_temps = charger_donnees(FICHIER_AXE_TEMPS)
    if df_axe_temps is None:
        return
    global axe_temps
    axe_temps = df_axe_temps["tps"]
    axe_temps.to_csv("AXE_DU_TEMPS/AXE_TEMPS.csv", index=False)

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
        (151, 157),
        (161, 167),
        (171, 177),
        (181, 184),
    ]
    essais = [
        essai
        for plage in plages_essais
        for essai in range(plage[0], plage[1] + 1)
        if essai != 113
    ]

    with Pool() as pool:
        pool.map(traiter_fichier, essais)

    print("Les graphiques ont été générés avec succès.")
    end_time = time.time()  # Capture du temps de fin
    execution_time = end_time - start_time
    print("Temps d'exécution pour main2.py:", execution_time, "secondes")


if __name__ == "__main__":
    main()
