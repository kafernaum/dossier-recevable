"""Contrôles arithmétiques locaux ; aucune validation contractuelle."""
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")

def number(value):
    if value is None or isinstance(value, bool):
        raise ValueError("Valeur numérique absente ou booléenne")
    try:
        n = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Valeur numérique invalide")
    if not n.is_finite() or n < 0:
        raise ValueError("Valeur non finie ou négative")
    return n

def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)

def check(data):
    currency = data.get("currency")
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError("Devise obligatoire")
    lines = data.get("lines")
    if not isinstance(lines, list) or not lines:
        raise ValueError("Lignes obligatoires")
    amounts = []
    for line in lines:
        if not isinstance(line, dict) or not line.get("label"):
            raise ValueError("Libellé de ligne obligatoire")
        if line.get("currency", currency) != currency:
            raise ValueError("Devises mixtes interdites")
        amounts.append(money(number(line.get("quantity")) * number(line.get("unit_price"))))
    total = sum(amounts, Decimal(0))
    declared = number(data.get("declared_total"))
    issues = []
    if declared != total:
        issues.append("Total déclaré différent du total calculé")
    payments = None
    if "payment_percentages" in data:
        raw = data["payment_percentages"]
        if not isinstance(raw, list) or not raw:
            raise ValueError("Pourcentages invalides")
        percents = [number(p) for p in raw]
        if any(p > 100 for p in percents):
            raise ValueError("Pourcentage supérieur à 100")
        if sum(percents, Decimal(0)) != 100:
            issues.append("Somme des pourcentages différente de 100")
        payments = [money(total * p / 100) for p in percents]
        if sum(payments, Decimal(0)) != total:
            issues.append("Somme des paiements différente du total après arrondi")
    return {"currency": currency, "line_totals": [str(x) for x in amounts],
            "calculated_total": str(total), "declared_total": str(declared),
            "payment_amounts": None if payments is None else [str(x) for x in payments],
            "issues": issues, "arithmetic_ok": not issues}

def main():
    try:
        with open(sys.argv[1], encoding="utf-8") as stream:
            result = check(json.load(stream, parse_float=Decimal))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["arithmetic_ok"] else 1
    except (OSError, ValueError, KeyError, TypeError, IndexError, InvalidOperation) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    sys.exit(main())
