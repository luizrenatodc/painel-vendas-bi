import unittest

from painel import indicadores, moeda, painel

VENDAS = [
    {"data": "2030-01-01", "canal": "Site", "valor": 100.0},
    {"data": "2030-01-09", "canal": "Loja", "valor": 300.0},
    {"data": "2030-02-01", "canal": "Site", "valor": 200.0},
]


class TestPainel(unittest.TestCase):
    def test_indicadores(self):
        k = indicadores(VENDAS)
        self.assertEqual(k["faturamento"], 600)
        self.assertEqual(k["ticket_medio"], 200)
        self.assertEqual(k["por_mes"], {"2030-01": 400, "2030-02": 200})

    def test_lista_vazia_nao_quebra(self):
        self.assertEqual(indicadores([])["ticket_medio"], 0)
        self.assertIn("Painel", painel(indicadores([])))

    def test_moeda(self):
        self.assertEqual(moeda(1234.5), "R$ 1.234,50")


if __name__ == "__main__":
    unittest.main()
