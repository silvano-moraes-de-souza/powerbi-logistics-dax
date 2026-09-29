"""Fill the HTML prototype (DASH LOGISTICA.html) with numbers computed from the CSV.

    python scripts/build_prototype.py

The prototype was drawn with placeholder numbers. This script replaces every
value on it (KPI cards, top 10 customers, carrier table, state tooltips) with
aggregates of BASE LOGISTICA.csv, so the page and the Power BI report agree.
It can be rerun whenever the CSV changes. The state shapes on the map are
still schematic, not real borders.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "DASH LOGISTICA.html"
df = pd.read_csv(ROOT / "BASE LOGISTICA.csv", sep=";", encoding="utf-8")

UF = {"São Paulo": "SP", "Minas Gerais": "MG", "Rio de Janeiro": "RJ", "Bahia": "BA",
      "Paraná": "PR", "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Pernambuco": "PE",
      "Ceará": "CE", "Distrito Federal": "DF"}  # fmt: skip


def brl(v: float) -> str:
    return f"R$ {v:,.0f}"


def k(v: float) -> str:
    return f"R$ {v / 1e3:,.0f}k"


def sub_seq(pattern: str, values: list, text: str, flags: int = re.S) -> str:
    """Replace the n-th match of ``pattern`` with the n-th value (a callable on the match)."""
    it = iter(values)
    return re.sub(pattern, lambda m: next(it)(m), text, count=len(values), flags=flags)


html = HTML.read_text(encoding="utf-8")
revenue, cost = df["Valor Faturamento"].sum(), df["Custo de Frete"].sum()

# KPI cards and the lines under them (the placeholders claimed growth that does not exist)
kpis = {
    "Total de Volumes": f"{df['Volume'].sum():,}",
    "Total Faturado": brl(revenue),
    "Total Transportado": f"{len(df):,}",
}
for label, value in kpis.items():
    html = re.sub(rf"({label}.*?<h2[^>]*>\s*)[^<]+?(\s*</h2>)", rf"\g<1>{value}\2",
                  html, count=1, flags=re.S)  # fmt: skip
# The KPI footers are plain facts now, so the "trending up" arrows go.
kpi_end = html.index("Total Transportado") + 2000
html = html[:kpi_end].replace(">trending_up<", ">info<") + html[kpi_end:]
html = re.sub(r">\+?[\d.]+% vs mês anterior<", f">{len(df)} embarques em 2025<", html)
html = re.sub(r">Novo recorde diário<", f">Frete = {cost / revenue:.0%} da receita<", html)
html = re.sub(r">\+?[\d.]+% em eficiência<", f">{df['Transportadora'].nunique()} transportadoras<",
              html)  # fmt: skip

# Top 10 customers by revenue
top_start = html.index("Top 10 Faturado")
top_end = html.index("Transportadora</th>")
block = html[top_start:top_end]
clients = df.groupby("Cliente")["Valor Faturamento"].sum().nlargest(10)
names = [lambda m, n=n: f"{m.group(1)}{n}{m.group(3)}" for n in clients.index]
block = sub_seq(r'(<span class="text-xs font-bold text-on-surface"\s*>)\s*([^<]+?)\s*(</span)',
                names, block)  # fmt: skip
block = sub_seq(r"R\$ [\d,.]+k", [lambda m, v=v: k(v) for v in clients.values], block)
widths = [round(100 * v / clients.max()) for v in clients.values]
block = sub_seq(r"(bg-gradient-to-r from-\w+ to-\w+/60 )(w-full|w-\[\d+%\])",
                [lambda m, w=w: f"{m.group(1)}w-[{w}%]" for w in widths], block)  # fmt: skip
html = html[:top_start] + block + html[top_end:]

# Carrier table
t_start = html.index("<tbody", html.index("Transportadora</th>"))
t_end = html.index("</tbody>", t_start)
table = html[t_start:t_end]
car = (df.groupby("Transportadora")
         .agg(cost=("Custo de Frete", "sum"), vol=("Volume", "sum"), rev=("Valor Faturamento", "sum"))
         .sort_values("rev", ascending=False).head(10))  # fmt: skip
rows = table.split("<tr")
for i, (name, r) in enumerate(car.iterrows(), start=1):
    row = rows[i]
    row = re.sub(r'(<td class="py-5 px-4 font-bold text-on-surface">)\s*[^<]+?\s*(</td>)',
                 rf"\g<1>{name}\2", row, count=1)  # fmt: skip
    row = sub_seq(r"R\$ [\d,.]+k", [lambda m, v=r.cost: k(v), lambda m, v=r.rev: k(v)], row)
    row = re.sub(r'(<td class="py-5 px-5 text-right text-on-surface">)[^<]+(</td>)',
                 rf"\g<1>{r.vol:,}\2", row, count=1)  # fmt: skip
    share = r.rev / revenue * 100
    row = re.sub(r">\s*[\d.]+%</span", f">{share:.1f}%</span", row, count=1)
    row = re.sub(r"(bg-gradient-to-r from-\w+ to-\w+/60 )(w-full|w-\[\d+%\])",
                 rf"\g<1>w-[{round(100 * r.rev / car.rev.max())}%]", row, count=1)  # fmt: skip
    rows[i] = row
# Rows beyond the real carriers (the placeholder "Outras Transportadoras") are dropped.
rows = rows[: len(car) + 1]
html = html[:t_start] + "<tr".join(rows) + html[t_end:]

# State tooltips on the (schematic) map: revenue, volume and shipments by destination
by_state = df.groupby("Estado_Destino").agg(rev=("Valor Faturamento", "sum"),
                                            vol=("Volume", "sum"), trips=("ID", "count"))  # fmt: skip


def state_attrs(m: re.Match) -> str:
    uf = UF.get(m.group(1))
    rev, vol, trips = (by_state.loc[uf] if uf in by_state.index else (0, 0, 0))
    return (f'data-state="{m.group(1)}"\n                      data-value="{brl(rev)}"\n'
            f'                      data-volume="{int(vol)}"\n                      '
            f'data-trips="{int(trips)}"')  # fmt: skip


html = re.sub(r'data-state="([^"]+)"\s*data-value="[^"]*"\s*data-volume="[^"]*"\s*'
              r'data-trips="[^"]*"', state_attrs, html)  # fmt: skip
sp = by_state.loc["SP"]
html = re.sub(r'(id="stateValue"[^>]*>\s*)[^<]+', rf"\g<1>{brl(sp.rev)}", html, count=1)
html = re.sub(r'(id="stateVolume"[^>]*>\s*)[^<]+', rf"\g<1>{int(sp.vol):,}", html, count=1)
html = re.sub(r'(id="stateTrips"[^>]*>\s*)[^<]+', rf"\g<1>{int(sp.trips)}", html, count=1)

HTML.write_text(html, encoding="utf-8", newline="\n")
print(f"{HTML.name}: revenue {brl(revenue)}, {len(df)} shipments, top customer {clients.index[0]}")
