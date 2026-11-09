# Démarrage rapide
1. Installer et activer la skill dans un environnement compatible.
2. Préparer des copies autorisées des TDR, addenda, CV, formulaires, offres et chronogramme. Minimiser les données sensibles.
3. Remplir assets/intake.md.
4. Demander un diagnostic sans réécriture, puis valider les corrections.
5. Relire toutes les versions finales après modification.
6. Valider humainement déclarations, signatures et soumission.

## Commandes
- Extrais les exigences avec leur source.
- Compare mes expériences aux critères sans modifier mon CV.
- Contrôle les durées et montants avec tes hypothèses.
- Prépare une revue finale indiquant les zones non vérifiées.

## Tests locaux
python scripts/check_budget.py tests/budget_example.json
python -m unittest discover -s tests -p 'test_*.py'
