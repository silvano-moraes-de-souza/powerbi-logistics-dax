"""Revenue and freight cost by carrier, computed from BASE LOGISTICA.csv.

    python scripts/chart_revenue_by_carrier.py   ->  docs/revenue_by_carrier.png

Same aggregation as the carrier visual in the report: SUM of Valor Faturamento
and Custo de Frete per Transportadora.
"""

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "BASE LOGISTICA.csv", sep=";", encoding="utf-8")
g = (df.groupby("Transportadora")[["Valor Faturamento", "Custo de Frete"]].sum()
       .sort_values("Valor Faturamento"))  # fmt: skip

fig, ax = plt.subplots(figsize=(9, 4.6), dpi=150)
for f in (fig, ax):
    f.set_facecolor("#fcfcfb")
y = range(len(g))
ax.barh(y, g["Valor Faturamento"] / 1e3, height=0.6, color="#2a78d6", label="Revenue", zorder=2)
ax.barh(y, g["Custo de Frete"] / 1e3, height=0.6, color="#eb6834", label="Freight cost", zorder=3)
for yi, rev in zip(y, g["Valor Faturamento"], strict=True):
    ax.text(rev / 1e3 + 15, yi, f"R$ {rev / 1e3:,.0f}k", va="center", fontsize=8, color="#0b0b0b")
ax.set_yticks(list(y), g.index, fontsize=8.5, color="#0b0b0b")
ax.set_xlabel("R$ thousands", color="#52514e", fontsize=9)
ax.tick_params(axis="x", colors="#52514e", labelsize=8)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#e4e3df", linewidth=0.8, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#e4e3df")
ax.set_xlim(0, g["Valor Faturamento"].max() / 1e3 * 1.18)
ax.legend(frameon=False, fontsize=8.5, loc="lower right")
total, cost = df["Valor Faturamento"].sum(), df["Custo de Frete"].sum()
ax.set_title(f"Revenue by carrier, 2025 (synthetic, {len(df)} shipments): "
             f"R$ {total / 1e6:.2f}M revenue, {cost / total:.0%} freight cost",
             loc="left", fontsize=10, color="#0b0b0b", pad=10)  # fmt: skip
fig.tight_layout()
out = ROOT / "docs" / "revenue_by_carrier.png"
fig.savefig(out, facecolor="#fcfcfb")
print(out)
