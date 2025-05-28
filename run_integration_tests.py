import unittest
import coverage

# Démarrer la couverture
cov = coverage.Coverage()
cov.start()

# Charger et exécuter les tests d'intégration
loader = unittest.TestLoader()
suite = loader.discover('tests/integration')  # ou adapte le chemin si besoin

with open("resultats_integration_tests.txt", "w", encoding="utf-8") as f:
    runner = unittest.TextTestRunner(stream=f, verbosity=2)
    result = runner.run(suite)

# Arrêter la couverture
cov.stop()
cov.save()

# Générer un rapport de couverture dans le fichier texte
with open("resultats_integration_tests.txt", "a", encoding="utf-8") as f:
    f.write("\n\n=== Rapport de couverture ===\n")
    cov.report(file=f, show_missing=True)
