# Contrôles financiers
Appliquer le modèle imposé sauf conflit non résolu. Séparer jours rémunérés, terrain, voyage et nuits. Ne jamais présumer qu’un consultant bénéficie du DSA des fonctionnaires internationaux. Un taux exige source, date, localité et applicabilité contractuelle vérifiées ; sinon demander un paramètre validé.

Honoraires = quantité × prix unitaire. Total = somme de lignes compatibles. Paiement = total × pourcentage / 100 sauf formule imposée différente. Vérifier séparément somme des pourcentages, paiements et arrondis. Distinguer taxes incluses, exclues, exonération documentée et traitement inconnu. Aucune conclusion fiscale sans cadre vérifié.

Documenter taux de change, sens, source et date ; ne pas additionner plusieurs devises sans conversion autorisée. Une cellule vide est inconnue, pas zéro.

## Script
JSON : currency non vide ; lines avec label, quantity, unit_price et currency facultative identique ; declared_total obligatoire ; payment_percentages facultatif. Valeurs décimales finies non négatives ; chaînes admises, sans séparateur de milliers.
Decimal ; arrondi de chaque ligne à 0,01 HALF_UP avant addition. Les paiements sont arrondis à 0,01 et leur écart éventuel signalé sans correction silencieuse. Cette convention doit être adaptée si la devise ou le formulaire en impose une autre.
Le script ne contrôle ni éligibilité des dépenses, fiscalité, authenticité des pièces, sources des taux ou conformité contractuelle.
