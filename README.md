Auteur: Régis Bigot , Cyrille Baudouin
Contributeur: Josselin Schumacker (data collector),
Project Member:  Alexandre Fendler 
Data curator: Etudiant Alexis Vauttier ;Etudiante Lina Zelmat 
Description: This data set contains experimental data on compression tests. These tests are realized on screw press and hydraulic press with several parameters: initial diameters, initial length, press energy or maximal load. Data contains loads, displacement and final shapes.
Keywords: forging, forming, upsetting, manufacturing, material behaviour, copper alloys, compression tests

# INFORMATIONS GENERALES
## Titre du jeu de données : Test de refoulement sur des alliages de cuivre
## DOI :
## Adresse de contact : Régis 

# Informations Méthodologiques
### Conditions Environnementales / Expérimentales
Vulcain est une plateforme technologique qui regroupe des équipements à l’échelle industrielle pour la mise en forme des matériaux et l’assemblage. Elle est principalement composée de cinq Îlots : forgeage, robotisation des procédés (FSW, WAAM, SPIF...), ligne d’assemblage DWARF, contrôle sans contact (Scan 3D, laser tracker) et mise en forme des métaux en feuilles.
PlateformeVulcain.png
### Presse Utilisée : Presse à Vis
La presse à vis utilise un moteur pour piloter la vitesse de descente du coulisseau jusqu'au point d'impact en raison de sa liaison directe avec la vis, laquelle entraîne l'écrou solidaire du coulisseau. Lors de l'impact, le moteur débraye, laissant le volant d'inertie délivrer l’énergie suffisante pour déformer la pièce.
Energie de frappe à 30 Kilojoules inscrit sur la fiche notice de cette presse vendu à 31,5 Kilojoules . 
### Paramètre Contrôlé
Le paramètre contrôlé dans ce processus est l'énergie de frappe.
### Description des Sources et Méthodes de Collecte des Données
Les données expérimentales ont été générées et collectées dans l’îlot de forgeage et de contrôle sans contact.
Pour collecter les différentes données, la presse est dotée des capteurs suivants :
- **Capteur Laser**: Utilisé pour mesurer des distances et détecter des variations de forme ou de position.
- **Capteur d’Effort**: Utilisé pour mesurer la force exercée pendant le processus de forgeage.
- **Capteur de Flexion Accéléromètre**: Utilisé pour détecter et mesurer les variations de flexion et d'accélération lors de l'impact.
Ces capteurs sont intégrés à la presse et fournissent des données en temps réel sur les différentes variables du processus de forgeage.
 Et enfin on a mis à disposition un fichier récapitulatif synthèse nommé : Plan_Expérience sous format Excell mettant les essais et les scans ensemble. (Document à exploiter)


## Aperçus des Données et Fichiers :
Un fichier ou la structure des colonnes, 
Coup1 	 lopin 1 ; lopin 2 …
Coup 2 lopin 1 …
### Convention de Nommage des Fichiers :
- Utilisez *UpperCaseCamelCase* pour les noms de classe. Les classes intégrées de Python sont généralement en minuscules. Les classes d'exception doivent se terminer par "Error".
- Utilisez *lowercase_with_underscores* pour les noms de module, les noms de package, les fonctions et les noms de méthode. Préférez les noms en un seul mot lorsque c'est possible.
- Les *variables globales* doivent être toutes en minuscules avec des mots séparés par des underscores.
- *Les variables d'instance* doivent être toutes en minuscules avec des mots séparés par des underscores. 
- Les *constantes* doivent être entièrement en majuscules avec des mots séparés par des underscores.

### Arborescence/Plan de Classement des Fichiers :
## Informations Spécifiques aux Données pour : 
(Pour les données tabulaires, fournir un dictionnaire des données/manuel de codage contenant les informations suivantes :)
### Liste des Variables/Entêtes de Colonne
```
_STAGEOPENDATA-MAIN_
├── ACQUISITION FORGEAGE    
├── AXE_DU_TEMPS 
│   ├── AXE_DU_TEMPS.csv
│   └── ESSAI_1_3_6.csv
├── output               
│   ├── figuresgrap 
│   └── figuresEFFORT
├── effort.ipynb
├── main.ipynb
├── main.py 
├── main2.ipynb   
├── main2.py    
├── main3.py 
├── main4.py                                
├── test_processing_integration.py                       
└──test_processing.py 
```
### Code des Valeurs Manquantes
### Informations Additionnelles 
La plateforme Vulcain a été utilisée pour collecter les données, qui comprend différents équipements industriels pour la mise en forme des matériaux et l’assemblage.

Ces informations fournissent un aperçu général du jeu de données, y compris les variables enregistrées et les méthodes utilisées pour collecter les données.

# Partie openData

## Introduction
Ces codes ont pour objectif de générer des figures au format PNG à partir de données contenues dans des fichiers CSV.

Ces fichiers CSV sont situés dans le répertoire **ACQUISITION FORGEAGE**, tandis que les données de sortie, y compris les figures générées, sont enregistrées dans le répertoire **Output**.
Le fichier principal du projet est main.py, qui contient le code permettant de traiter les données et de générer les figures.

## Structure
- Ces fichiers CSV sont situés dans le répertoire **ACQUISITION FORGEAGE**, tandis que les données de sortie, y compris - les figures générées, sont enregistrées dans le répertoire **Output**.
- Le fichier principal du projet est main.py , qui contient le code clean  permettant de traiter les données et de générer les figures. 
- Le Jupyternotebook **main.ipynb** contenant un code explicative avec une description et des commentaires.

## Décomposition
- *AQUISITION FORGEAGE* :  Les données entrantes, dossier qui contient les fichiers ESSAI_XX.csv.
- *AXE_DU_TEMPS*:  Fichier qui contient l'ESSAI_1_3_6.csv qui a une colonne de plus (axe du temps) et qui est extraite dans un fichier AXE_DU_TEMPS.csv
- *output* : Les données de sortie , figures >>>> Toutes les grandeurs en fonction du temps.
- *figuresEFFORT*: les graphes de l'effort en fonction du déplacement  
- *effort.ipynb*  Code python sur Jupyter qui génère les figuresEFFORT SEULEMENT!
- *main.ipynb* : Code python main qui génère toutes les graphes
-  *main.py* : Code python main qui génère toutes les graphes avec commentaires 
-  *main2.ipynb* :   Code python main qui génère toutes les graphes en utilisant les fonctions
-  *main2.py* :    Code python main qui génère toutes les graphes en utilisant les fonctions avec commentaires
-  *main3.py* :  Code python main qui génère toutes les graphes en utilisant le calcul parallèle avec la bibliothèque Dask
-  *main4.py* :     Code python main qui génère toutes les graphes en utilisant le calcul parallèle avec la bibliothèque Multiprocessing                         
-  *test_processing_integration.py*:   Test d'intégration pour vérifier si l'ensemble du pipeline de traitement des données fonctionne correctemen                   
- *test_processing.py*:  Test d'unité pour vérifier le comportement de chaque fonction

**Test d'unité** :

Le test d'unité est une pratique de test logiciel où des composants individuels ou des unités de code sont testés de manière isolée afin de s'assurer qu'ils fonctionnent comme prévu. *Une unité* peut être une fonction, une méthode, une classe ou même un module, selon le niveau de granularité du test. L'objectif principal des tests d'unité est de *vérifier que chaque unité de code produit les résultats attendus pour différentes entrées*, ainsi que de *détecter et de corriger les erreurs dans les plus petites parties du code*.

**Test d'intégration** :

Le test d'intégration vise à *tester la manière dont les différentes unités ou composants de code s'assemblent et interagissent les uns avec les autres* pour former des fonctionnalités plus larges ou des systèmes complets. Contrairement aux tests d'unité qui se concentrent sur des parties isolées du code, les tests d'intégration examinent les flux de données entre les composants, les interactions entre les modules et la cohérence globale du système.


# Comment run?
- Ouvrir le terminal : Terminal >>> New Terminal
- COPIER= CTRL + C
- COLLER = CTRL + SHIFT + V
1- Pour accéder à l'environnement virtuel pandavenv, dans le terminal, copier & coller chaque commande et appuyez sur ENTRÉE  : 
    - ```cd STAGEOPENDATA-MAIN ```
    - ```cd env```
    - ```cd Scripts```
    - ```.\Activate```
2- ```poetry install```

3- Exécuter le script principal : 
    -  ```python -m main.py```  ou ( python -m main2.py ) ou ( python -m main3.py ) ou ( python -m main4.py )
- **Sinon**, ouvrez  le fichier **main.ipynb** et puis appuyez sur  'Run All' en haut.

-Pour exécuter les tests: 
	
    - python -m unittest test_processing.py
    - python -m unittest test_processing_integration.py


## Assistance
En cas de problème ou de question, veuillez vous diriger vers Régis Bigot 
 < Regis.bigot@ensam.eu >