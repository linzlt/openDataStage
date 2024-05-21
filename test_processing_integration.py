import unittest
import os
import pandas as pd
import main2
import main3
import main4


class TestCSVProcessingIntegration(unittest.TestCase):

    def setUp(self):
        self.test_csv_file = "test_data_integration.csv"
        self.test_data = pd.DataFrame(
            {
                "tps": [0, 1, 2, 3],
                "col1": ["1,1", "2,2", "3,3", "4,4"],
                "col2": [4.4, 5.5, 6.6, None],
            }
        )
        self.test_data.to_csv(self.test_csv_file, sep=";", index=False)
        self.test_axes = pd.Series([0, 1, 2, 3])

    def tearDown(self):
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_full_pipeline(self):
        for module in [main2, main3, main4]:
            # Charger les données
            df = module.charger_donnees(self.test_csv_file, delimiter=";")
            self.assertEqual(len(df), 4)

            # Convertir les colonnes en float
            df = module.convertir_colonnes_float(df)
            self.assertTrue(df["col1"].dtype == "float64")
            self.assertTrue(df["col2"].dtype == "float64")

            # Tronquer les données
            df_tronque, axe_temps_tronque = module.tronquer_donnees(df, self.test_axes)

            # Trouver le dernier index non-NaN pour chaque colonne, puis prendre le maximum de ces index
            dernier_index_non_nan = df.apply(
                lambda col: pd.to_numeric(col, errors="coerce").last_valid_index()
            ).max()

            # Vérifier la longueur des données tronquées
            self.assertEqual(len(df_tronque), dernier_index_non_nan + 1)
            self.assertEqual(len(axe_temps_tronque), dernier_index_non_nan + 1)

            # Vérifier que les colonnes contenant uniquement des NaN sont supprimées
            self.assertFalse(df_tronque.isnull().all(axis=1).any())
            self.assertTrue(df_tronque.isnull().all(axis=0).sum() == 0)

            # Vérifier si les courbes sont tracées correctement
            chemin_figures = f"test_figures_{module.__name__}"
            module.creer_dossier_si_non_existant(chemin_figures)
            module.tracer_courbes(1, df_tronque, axe_temps_tronque, chemin_figures)
            self.assertTrue(
                os.path.exists(os.path.join(chemin_figures, "ESSAI_001.png"))
            )
            os.remove(os.path.join(chemin_figures, "ESSAI_001.png"))
            os.rmdir(chemin_figures)


if __name__ == "__main__":
    unittest.main()
