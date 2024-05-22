import os
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
        print(f"Une erreur de parsing est survenue lors de la lecture du fichier {chemin}: {e}")
        df = pd.DataFrame()
    return df

def tronquer_donnees(df, axe_temps):
    df_numeric = df.apply(pd.to_numeric, errors="coerce")
    dernier_index_non_nan = df_numeric.apply(lambda col: col.last_valid_index()).max()
    if pd.isna(dernier_index_non_nan):
        raise ValueError("Dataframe contains only NaN values")
    dernier_index_non_nan = int(dernier_index_non_nan)
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

def ajuster_colonne_9(df):
    # Vérifier que la colonne 9 existe
    if df.shape[1] > 8:
        # Soustraire la première valeur de la colonne 9 pour chaque ligne
        df.iloc[:, 8] = df.iloc[:, 8] - df.iloc[0, 8]
    return df

def tracer_courbes(col_index, df, axe_temps, chemin_figures):
    for i, col in enumerate(df.columns):
        plt.plot(axe_temps[: len(df[col])], df[col], label=col)
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    filename = os.path.join(chemin_figures, f"ESSAI_{col_index:03d}.png")
    plt.savefig(filename)
    plt.close()

def main():
    start_time = time.time()
    chemin_repertoire = "Output"
    chemin_figures = os.path.join(chemin_repertoire, "figures")
    creer_dossier_si_non_existant(chemin_figures)
    FICHIER_AXE_TEMPS = "AXE_DU_TEMPS/ESSAI_1_3_6.csv"
    df_axe_temps = charger_donnees(FICHIER_AXE_TEMPS)
    if df_axe_temps is None:
        return
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
    ]
    fichiers_non_coherents = []
    for plage in plages_essais:
        debut, fin = plage
        for essai in range(debut, fin + 1):
            if essai == 113:
                continue
            nom_fichier = os.path.join("ACQUISITION FORGEAGE", f"ESSAI_{str(essai).zfill(3)}.csv")
            if os.path.exists(nom_fichier):
                df_essai = charger_donnees(nom_fichier)
                if df_essai is not None:
                    df_essai = convertir_colonnes_float(df_essai)
                    df_essai = ajuster_colonne_9(df_essai)
                    df_essai, axe_temps_tronque = tronquer_donnees(df_essai, axe_temps)
                    tracer_courbes(essai, df_essai, axe_temps_tronque, chemin_figures)
            else:
                fichiers_non_coherents.append(nom_fichier)
    print("Les graphiques ont été générés avec succès.")
    if fichiers_non_coherents:
        print("Les fichiers suivants n'ont pas été trouvés :")
        for fichier in fichiers_non_coherents:
            print(fichier)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution pour main.py:", execution_time, "secondes")

if __name__ == "__main__":
    main()

def effortdeplacement():
    chemin_repertoire = "Output"
    chemin_figures = os.path.join(chemin_repertoire, "figuresEFFORT")
    creer_dossier_si_non_existant(chemin_figures)
    plages_essais = [
        (1, 7), (11, 17), (21, 27), (31, 37),
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

    fichiers_non_coherents = []

    for plage in plages_essais:
        debut, fin = plage
        for essai in range(debut, fin + 1):
            if essai == 113:
                continue
            nom_fichier = os.path.join("ACQUISITION FORGEAGE", f"ESSAI_{str(essai).zfill(3)}.csv")
            if os.path.exists(nom_fichier):
                try:
                    df_essai = pd.read_csv(nom_fichier, delimiter=";", skiprows=0)
                    if df_essai.shape[1] > 8:
                        df_essai = convertir_colonnes_float(df_essai)
                        df_essai = ajuster_colonne_9(df_essai)
                        col2 = df_essai.iloc[:, 1]
                        col9 = df_essai.iloc[:, 8]
                        dernier_index_non_nan = min(col2.last_valid_index(), col9.last_valid_index())
                        col2_tronque = col2[:dernier_index_non_nan + 1]
                        col9_tronque = col9[:dernier_index_non_nan + 1]
                        plt.plot(col9_tronque, col2_tronque, label=f'Essai {essai}')
                        plt.title(f"Essai {essai}")
                        plt.xlabel("Colonne 9")
                        plt.ylabel("Colonne 2")
                        plt.legend(loc="upper right")
                        plt.grid(True)
                        nom_figure = os.path.join(chemin_figures, f"ESSAI_{str(essai).zfill(3)}.png")
                        plt.savefig(nom_figure)
                        plt.close()
                    else:
                        print(f"Le fichier {nom_fichier} n'a pas assez de colonnes.")
                except FileNotFoundError:
                    fichiers_non_coherents.append(nom_fichier)
                    continue
            else:
                fichiers_non_coherents.append(nom_fichier)
    print("Les graphiques ont été générés avec succès.")
    if fichiers_non_coherents:
        print("Les fichiers suivants n'ont pas été trouvés :")
        for fichier in fichiers_non_coherents:
            print(fichier)
