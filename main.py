import os
from pathlib import Path
from dataclasses import dataclass

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# Configuration
# ============================================================

@dataclass
class AppConfig:
    dossier_sortie: str = "Output"
    dossier_figures: str = "figures"
    separateur_csv: str = ";"
    colonne_temps: str = "tps"

    @property
    def chemin_figures(self) -> Path:
        return Path(self.dossier_sortie) / self.dossier_figures


# ============================================================
# Gestion des fichiers
# ============================================================

class GestionnaireFichiers:
    def __init__(self, config: AppConfig):
        self.config = config
        self.config.chemin_figures.mkdir(parents=True, exist_ok=True)

    def charger_csv(self, fichier) -> pd.DataFrame:
        try:
            return pd.read_csv(fichier, sep=self.config.separateur_csv)
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du fichier : {e}")

    def sauvegarder_figure(self, fig, nom_fichier: str) -> Path:
        chemin = self.config.chemin_figures / nom_fichier
        fig.savefig(chemin, bbox_inches="tight", dpi=150)
        return chemin


# ============================================================
# Traitement des données
# ============================================================

class TraitementDonnees:
    @staticmethod
    def convertir_colonnes_en_float(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", ".", regex=False)
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    @staticmethod
    def corriger_colonne_reference(df: pd.DataFrame, index_colonne: int = 8) -> pd.DataFrame:
        df = df.copy()

        if df.shape[1] > index_colonne:
            df.iloc[:, index_colonne] = df.iloc[:, index_colonne] - df.iloc[0, index_colonne]

        return df

    @staticmethod
    def tronquer_donnees(df: pd.DataFrame, axe_temps: pd.Series):
        dernier_index_non_nan = df.apply(lambda col: col.last_valid_index()).min()

        if pd.isna(dernier_index_non_nan):
            raise ValueError("Le fichier ne contient pas de données exploitables.")

        dernier_index_non_nan = int(dernier_index_non_nan)

        axe_temps_tronque = axe_temps.iloc[: dernier_index_non_nan + 1]
        df_tronque = df.iloc[: dernier_index_non_nan + 1, :]

        longueur = min(len(axe_temps_tronque), len(df_tronque))

        return axe_temps_tronque.iloc[:longueur], df_tronque.iloc[:longueur, :]

    def traiter(self, df: pd.DataFrame, axe_temps: pd.Series, corriger_reference: bool = True):
        df = self.convertir_colonnes_en_float(df)

        if corriger_reference:
            df = self.corriger_colonne_reference(df)

        return self.tronquer_donnees(df, axe_temps)


# ============================================================
# Tracé des graphes
# ============================================================

class TraceurGraphiques:
    def __init__(self, gestionnaire_fichiers: GestionnaireFichiers):
        self.gestionnaire_fichiers = gestionnaire_fichiers

    def tracer_essai(self, axe_temps: pd.Series, df_essai: pd.DataFrame, titre: str, colonnes=None):
        if colonnes is None:
            colonnes = df_essai.columns.tolist()

        fig, ax = plt.subplots(figsize=(12, 6))

        for col in colonnes:
            ax.plot(axe_temps, df_essai[col], label=col)

        ax.set_title(titre)
        ax.set_xlabel("Temps")
        ax.set_ylabel("Valeurs")
        ax.grid(True)
        ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.0))

        fig.tight_layout()
        return fig

    def tracer_et_sauvegarder(self, axe_temps, df_essai, nom_essai: str, colonnes=None):
        fig = self.tracer_essai(
            axe_temps=axe_temps,
            df_essai=df_essai,
            titre=f"Essai {nom_essai}",
            colonnes=colonnes,
        )

        nom_fichier = f"{nom_essai}.png"
        chemin = self.gestionnaire_fichiers.sauvegarder_figure(fig, nom_fichier)

        return fig, chemin


# ============================================================
# Interface Streamlit
# ============================================================

class InterfaceApplication:
    def __init__(self):
        self.config = AppConfig()
        self.gestionnaire_fichiers = GestionnaireFichiers(self.config)
        self.traitement = TraitementDonnees()
        self.traceur = TraceurGraphiques(self.gestionnaire_fichiers)

    def lancer(self):
        st.set_page_config(
            page_title="Analyse des essais",
            layout="wide",
        )

        st.title("Interface interactive d'analyse des essais")
        st.write("Importez l'axe du temps et les fichiers d'essais, puis générez les graphes.")

        with st.sidebar:
            st.header("Paramètres")

            separateur = st.text_input("Séparateur CSV", value=self.config.separateur_csv)
            colonne_temps = st.text_input("Nom de la colonne temps", value=self.config.colonne_temps)
            corriger_reference = st.checkbox("Corriger la colonne 9 par rapport à sa première valeur", value=True)

            self.config.separateur_csv = separateur
            self.config.colonne_temps = colonne_temps

        st.subheader("1. Importer l'axe du temps")
        fichier_axe_temps = st.file_uploader(
            "Importer le fichier CSV de l'axe du temps",
            type=["csv"],
            key="axe_temps",
        )

        if fichier_axe_temps is None:
            st.info("Veuillez importer le fichier contenant l'axe du temps.")
            return

        try:
            df_axe_temps = self.gestionnaire_fichiers.charger_csv(fichier_axe_temps)
        except ValueError as e:
            st.error(str(e))
            return

        if colonne_temps not in df_axe_temps.columns:
            st.error(f"La colonne '{colonne_temps}' est introuvable dans le fichier d'axe du temps.")
            st.write("Colonnes disponibles :", df_axe_temps.columns.tolist())
            return

        axe_temps = pd.to_numeric(
            df_axe_temps[colonne_temps].astype(str).str.replace(",", ".", regex=False),
            errors="coerce",
        )

        st.success("Axe du temps chargé avec succès.")
        st.dataframe(df_axe_temps.head())

        st.subheader("2. Importer les fichiers d'essais")
        fichiers_essais = st.file_uploader(
            "Importer un ou plusieurs fichiers CSV d'essais",
            type=["csv"],
            accept_multiple_files=True,
            key="essais",
        )

        if not fichiers_essais:
            st.info("Veuillez importer au moins un fichier d'essai.")
            return

        st.success(f"{len(fichiers_essais)} fichier(s) importé(s).")

        for fichier in fichiers_essais:
            st.divider()
            nom_essai = Path(fichier.name).stem
            st.subheader(f"Essai : {nom_essai}")

            try:
                df_essai = self.gestionnaire_fichiers.charger_csv(fichier)
                axe_temps_tronque, df_essai_traite = self.traitement.traiter(
                    df=df_essai,
                    axe_temps=axe_temps,
                    corriger_reference=corriger_reference,
                )
            except Exception as e:
                st.error(f"Erreur avec {fichier.name} : {e}")
                continue

            colonnes_disponibles = df_essai_traite.columns.tolist()
            colonnes_selectionnees = st.multiselect(
                f"Colonnes à tracer pour {nom_essai}",
                options=colonnes_disponibles,
                default=colonnes_disponibles,
                key=f"colonnes_{nom_essai}",
            )

            if not colonnes_selectionnees:
                st.warning("Sélectionnez au moins une colonne à tracer.")
                continue

            col1, col2 = st.columns([1, 3])

            with col1:
                st.write("Aperçu des données traitées")
                st.dataframe(df_essai_traite[colonnes_selectionnees].head())

            with col2:
                fig, chemin = self.traceur.tracer_et_sauvegarder(
                    axe_temps=axe_temps_tronque,
                    df_essai=df_essai_traite,
                    nom_essai=nom_essai,
                    colonnes=colonnes_selectionnees,
                )

                st.pyplot(fig)
                st.success(f"Figure sauvegardée : {chemin}")

                with open(chemin, "rb") as image_file:
                    st.download_button(
                        label="Télécharger la figure PNG",
                        data=image_file,
                        file_name=f"{nom_essai}.png",
                        mime="image/png",
                    )


# ============================================================
# Point d'entrée
# ============================================================

if __name__ == "__main__":
    app = InterfaceApplication()
    app.lancer()
