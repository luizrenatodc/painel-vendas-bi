"""Lê um CSV de vendas, calcula indicadores e gera um painel HTML sem dependências."""
import csv
import html
import sys
from collections import defaultdict
from pathlib import Path


def ler(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        return [{**l, "valor": float(l["valor"])} for l in csv.DictReader(f)]


def indicadores(vendas):
    total = sum(v["valor"] for v in vendas)
    por_mes, por_canal = defaultdict(float), defaultdict(float)
    for v in vendas:
        por_mes[v["data"][:7]] += v["valor"]
        por_canal[v["canal"]] += v["valor"]
    return {
        "faturamento": total,
        "pedidos": len(vendas),
        "ticket_medio": total / len(vendas) if vendas else 0,
        "por_mes": dict(sorted(por_mes.items())),
        "por_canal": dict(sorted(por_canal.items(), key=lambda i: -i[1])),
    }


def moeda(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def barras(dados):
    maior = max(dados.values(), default=1)
    return "".join(
        f'<div class="l"><span>{html.escape(k)}</span><i style="width:{v / maior * 100:.0f}%"></i><b>{moeda(v)}</b></div>'
        for k, v in dados.items()
    )


def painel(k):
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Painel de vendas</title>
<style>body{{font:16px system-ui;background:#0c0f17;color:#eef2fa;max-width:820px;margin:40px auto;padding:0 16px}}
.c{{display:flex;gap:12px;flex-wrap:wrap}}.c div{{flex:1;background:#141926;border-radius:12px;padding:16px}}
.c b{{display:block;font-size:24px;color:#a8d8ff}}.l{{display:grid;grid-template-columns:90px 1fr 130px;gap:10px;align-items:center;margin:8px 0}}
.l i{{height:12px;background:#a8d8ff;border-radius:6px}}.l b{{text-align:right}}</style>
<h1>Painel de vendas</h1><p>Dados fictícios de demonstração.</p>
<div class="c"><div>Faturamento<b>{moeda(k["faturamento"])}</b></div><div>Pedidos<b>{k["pedidos"]}</b></div><div>Ticket médio<b>{moeda(k["ticket_medio"])}</b></div></div>
<h2>Por mês</h2>{barras(k["por_mes"])}<h2>Por canal</h2>{barras(k["por_canal"])}</html>"""


if __name__ == "__main__":
    raiz = Path(__file__).parent
    origem = sys.argv[1] if len(sys.argv) > 1 else raiz / "dados/vendas.csv"
    (raiz / "painel.html").write_text(painel(indicadores(ler(origem))), encoding="utf-8")
    print("painel.html gerado")
