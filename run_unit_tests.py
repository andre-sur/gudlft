import unittest
import coverage

def run_unit_tests():
    # Démarrer la couverture
    cov = coverage.Coverage()
    cov.start()

    # Charger les tests unitaires
    loader = unittest.TestLoader()
    suite = loader.discover('tests/unit')

    # Exécuter et enregistrer dans le fichier
    with open('resultats_tests_unitaires.txt', 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

    # Arrêter et sauvegarder la couverture
    cov.stop()
    cov.save()

    # Ajouter le rapport de couverture au même fichier
    with open('resultats_tests_unitaires.txt', 'a', encoding='utf-8') as f:
        f.write("\n\n=== Rapport de couverture ===\n")
        cov.report(file=f, show_missing=True)

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_unit_tests()
    if success:
        print("Tous les tests unitaires ont réussi. Rapport dans 'resultats_tests_unitaires.txt'.")
    else:
        print("Certains tests unitaires ont échoué. Voir 'resultats_tests_unitaires.txt' pour détails.")
