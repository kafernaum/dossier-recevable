import importlib.util
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location("budget", Path(__file__).resolve().parents[1] / "scripts/check_budget.py")
budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget)

class BudgetTests(unittest.TestCase):
    def base(self):
        return {"currency": "USD", "lines": [{"label":"Test", "quantity":"3", "unit_price":"0.10"}], "declared_total":"0.30", "payment_percentages":[20,40,40]}
    def test_decimal(self):
        self.assertTrue(budget.check(self.base())["arithmetic_ok"])
    def test_wrong_total(self):
        d=self.base(); d["declared_total"]="1"
        self.assertFalse(budget.check(d)["arithmetic_ok"])
    def test_missing(self):
        d=self.base(); del d["lines"][0]["unit_price"]
        with self.assertRaises(ValueError): budget.check(d)
    def test_mixed(self):
        d=self.base(); d["lines"][0]["currency"]="EUR"
        with self.assertRaises(ValueError): budget.check(d)
    def test_nonfinite(self):
        for v in ["NaN", "Infinity", "-1", True]:
            d=self.base(); d["lines"][0]["quantity"]=v
            with self.assertRaises(ValueError): budget.check(d)
    def test_percentages(self):
        d=self.base(); d["payment_percentages"]=[20,40]
        self.assertFalse(budget.check(d)["arithmetic_ok"])
    def test_rounding(self):
        d=self.base(); d["lines"][0].update(quantity="1",unit_price="0.05"); d["declared_total"]="0.05"; d["payment_percentages"]=[50,50]
        self.assertIn("Somme des paiements différente du total après arrondi",budget.check(d)["issues"])
    def test_zero(self):
        d=self.base(); d["lines"][0]["quantity"]="0"; d["declared_total"]="0"
        self.assertTrue(budget.check(d)["arithmetic_ok"])

if __name__ == "__main__": unittest.main()
