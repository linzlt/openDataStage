import unittest
import os
import pandas as pd
import matplotlib.pyplot as plt
import main2
import main3
import main4


class TestCSVProcessing(unittest.TestCase):

    def setUp(self):
        self.test_csv_file = "test_data.csv"
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

    def test_creer_dossier_si_non_existant(self):
        for module in [main2, main3, main4]:
            chemin = f"test_dossier_{module.__name__}"
            if os.path.exists(chemin):
                os.rmdir(chemin)
            if hasattr(module, 'creer_dossier_si_non_existant'):
                module.creer_dossier_si_non_existant(chemin)
            elif hasattr(module, 'creer_repertoire'):
                module.creer_repertoire(chemin)
            self.assertTrue(os.path.exists(chemin))
            os.rmdir(chemin)

    def test_charger_donnees(self):
        for module in [main2, main3, main4]:
            if hasattr(module, 'charger_donnees'):
                df = module.charger_donnees(self.test_csv_file)
            elif hasattr(module, 'charger_donnees'):
                df = module.charger_donnees(self.test_csv_file, delimiter=";")
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 4)

    def test_tronquer_donnees(self):
        for module in [main2, main3, main4]:
            if hasattr(module, 'tronquer_donnees'):
                df = pd.DataFrame({"a": [1, 2, 3, None], "b": [4, 5, None, None]})
                df_tronque, axe_temps_tronque = module.tronquer_donnees(df, self.test_axes)
                self.assertEqual(len(df_tronque), 3)
                self.assertEqual(len(axe_temps_tronque), 3)

    def test_convertir_colonnes_float(self):
        for module in [main2, main3, main4]:
            if hasattr(module, 'convertir_colonnes_en_float'):
                df = pd.DataFrame({"a": ["1,1", "2,2", "3,3"], "b": [4.4, 5.5, None]})
                df = module.convertir_colonnes_en_float(df)
                self.assertTrue(df["a"].dtype == "float64")
                self.assertTrue(df["b"].dtype == "float64")

    def test_tracer_courbes(self):
        for module in [main2, main3, main4]:
            if hasattr(module, 'tracer_courbes'):
                df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
                chemin_figures = f"test_figures_{module.__name__}"
                module.creer_dossier_si_non_existant(chemin_figures)
                module.tracer_courbes(1, df, self.test_axes, chemin_figures)
                self.assertTrue(os.path.exists(os.path.join(chemin_figures, "ESSAI_001.png")))
                plt.close()
                os.remove(os.path.join(chemin_figures, "ESSAI_001.png"))
                os.rmdir(chemin_figures)


if __name__ == "__main__":
    unittest.main()
