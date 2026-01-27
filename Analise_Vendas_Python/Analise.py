import pandas as pd
import matplotlib.pyplot as plt

arquivo = r"C:\Users\rodri\OneDrive\Ambiente de Trabalho\GitHub\python\Analise_1\Dados_ficticios.xlsx"
dados = pd.read_excel(arquivo)

resumo = dados.groupby("Categoria")["Valor"].sum().sort_values(ascending=False)

plt.style.use("dark_background")
plt.rcParams["font.family"] = "Segoe UI"

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#1E1E2F")
ax.set_facecolor("#1E1E2F")

cores = ["#4E79A7", "#59A14F", "#76B7B2", "#A0CBE8"]
barras = ax.bar(resumo.index, resumo.values, color=cores)

ax.set_title("Valor Total por Categoria", fontsize=18, fontweight="bold")
ax.set_xlabel("Categoria")
ax.set_ylabel("Valor Total (R$)")
ax.tick_params(axis='x', rotation=20)
ax.grid(False)

for barra in barras:
    y = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2, y, f"R$ {y:.0f}",
            ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.show()
