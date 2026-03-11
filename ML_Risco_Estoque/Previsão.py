import os
import warnings
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

warnings.filterwarnings("ignore")


# se voce clonou esse projeto, altere apenas essas duas linhas abaixo
SERVIDOR = "OK_Computer\\SQLEXPRESS"
BANCO    = "ContosoRetailDW"


def conectar_banco():
    # usamos SQLAlchemy no lugar do pyodbc direto para evitar warning do pandas
    try:

        conn_str = (
            f"mssql+pyodbc://{SERVIDOR}/{BANCO}"
            "?driver=SQL+Server&trusted_connection=yes"
        )

        # fast_executemany acelera a leitura quando o volume de dados e grande
        engine = create_engine(conn_str, fast_executemany=True)

        print("Conexao realizada com sucesso")
        return engine

    except Exception as e:

        print("Erro na conexao:", e)
        return None


def carregar_query():
    # o SQL fica num arquivo separado para deixar o Python mais organizado
    try:

        # __file__ pega o caminho do proprio script, ai juntamos com o nome do SQL
        caminho = os.path.join(os.path.dirname(__file__), "DataBase.sql")

        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:

        print("Erro ao carregar arquivo SQL:", e)
        return None


def carregar_dados():

    print("Carregando dados do banco...")

    engine = conectar_banco()

    if engine is None:
        return None

    query = carregar_query()

    if query is None:
        return None

    try:

        # informar os tipos antes de carregar e mais rapido
        # o pandas nao precisa adivinhar o tipo de cada coluna
        dtype_map = {
            "IdProduto":           "int32",
            "TotalVendido":        "int32",
            "MediaVenda":          "float32",
            "DiasSemVenda":        "int32",
            "VendasUltimos30Dias": "int32",
            "VendasUltimos90Dias": "int32",
        }

        df = pd.read_sql_query(query, engine, dtype=dtype_map)

        print("Dados carregados -", len(df), "produtos encontrados")
        return df

    except Exception as e:

        print("Erro ao executar query:", e)
        return None


def tratar_dados(df):

    print("Tratando dados...")

    # substitui celulas vazias por zero para o modelo nao quebrar
    df = df.fillna(0)
    df["MediaVenda"] = df["MediaVenda"].astype(float)

    print("Tratamento concluido")
    return df


def criar_features(df):

    print("Criando features...")

    # IndiceQueda mostra quanto das vendas dos ultimos 90 dias
    # aconteceram nos ultimos 30 — quanto menor, mais o produto esta caindo
    df["IndiceQueda"] = np.where(
        df["VendasUltimos90Dias"] == 0,
        0,
        df["VendasUltimos30Dias"] / df["VendasUltimos90Dias"]
    )

    # log1p suaviza valores muito altos para o modelo nao dar peso excessivo
    # a produtos que vendem muito — log(x+1) evita erro quando x e zero
    df["ScoreVenda"] = np.log1p(
        df["VendasUltimos30Dias"] + df["VendasUltimos90Dias"]
    )

    print("Features criadas - IndiceQueda, ScoreVenda")
    return df


def criar_target(df):

    print("Criando target...")

    # o target e o que o modelo vai prever
    # definimos como em risco todo produto que passou 120 dias sem vender
    df["ProdutoRisco"] = np.where(df["DiasSemVenda"] > 120, 1, 0)

    total    = len(df)
    em_risco = df["ProdutoRisco"].sum()
    normais  = total - em_risco

    print("Target criado")
    print("  Normal:   ", normais, "produtos")
    print("  Em Risco: ", em_risco, "produtos")

    return df


def modelo_ml(df):

    print("\nIniciando treinamento do modelo...")

    features = [
        "VendasUltimos30Dias",
        "VendasUltimos90Dias",
        "MediaVenda",
        "IndiceQueda",
        "ScoreVenda"
    ]

    # X e o que o modelo aprende, y e o que ele tenta prever
    X = df[features]
    y = df["ProdutoRisco"]

    # 70% dos dados para treino e 30% para testar o modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42
    )

    print("Treinando RandomForest...")

    # n_jobs=-1 usa todos os nucleos do processador, deixa bem mais rapido
    modelo = RandomForestClassifier(
        n_estimators=100,
        n_jobs=-1,
        random_state=42
    )

    modelo.fit(X_train, y_train)

    previsoes = modelo.predict(X_test)

    print("\nResultados:")
    print("  Acuracia:", round(accuracy_score(y_test, previsoes), 3))

    # cross-validation testa o modelo 5 vezes em partes diferentes dos dados
    # serve para confirmar que o resultado nao foi sorte
    cv = cross_val_score(modelo, X, y, cv=5, n_jobs=-1)
    print("  Cross-Validation:", round(cv.mean(), 3), "(+-", round(cv.std(), 3), ")")

    print("\nRelatorio completo:")
    print(classification_report(y_test, previsoes, target_names=["Normal", "Em Risco"]))

    print("Matriz de Confusao:")
    print(confusion_matrix(y_test, previsoes))

    return modelo


def graficos(df):

    print("\nGerando graficos...")

    df["StatusProduto"] = df["ProdutoRisco"].map({
        0: "Normal",
        1: "Em Risco"
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("ML - Risco de Produtos Parados", fontsize=14, fontweight="bold")

    # grafico 1: mostra quantos produtos ficaram X dias sem vender
    sns.histplot(
        df["DiasSemVenda"],
        bins=30,
        color="#3498db",
        ax=axes[0]
    )
    axes[0].set_title("Distribuicao Dias Sem Venda")
    axes[0].set_xlabel("Dias")
    axes[0].set_ylabel("Produtos")

    # grafico 2: contagem simples de normais vs em risco
    sns.countplot(
        x="StatusProduto",
        hue="StatusProduto",
        data=df,
        palette={"Normal": "#2ecc71", "Em Risco": "#e74c3c"},
        legend=False,
        ax=axes[1]
    )
    axes[1].set_title("Classificacao de Produtos")

    # grafico 3: separamos os grupos e plotamos em camadas
    # assim os pontos laranjas ficam sempre visiveis em cima dos azuis
    normais  = df[df["StatusProduto"] == "Normal"]
    em_risco = df[df["StatusProduto"] == "Em Risco"]

    axes[2].scatter(
        normais["VendasUltimos90Dias"],
        normais["VendasUltimos30Dias"],
        color="#3498db",
        label="Normal",
        s=60,
        alpha=0.5
    )

    # zorder=5 garante que os pontos laranjas ficam na frente dos azuis
    axes[2].scatter(
        em_risco["VendasUltimos90Dias"],
        em_risco["VendasUltimos30Dias"],
        color="#e67e22",
        label="Em Risco",
        s=80,
        alpha=0.9,
        zorder=5
    )

    axes[2].set_title("Tendencia de Vendas")
    axes[2].set_xlabel("Vendas Ultimos 90 Dias")
    axes[2].set_ylabel("Vendas Ultimos 30 Dias")
    axes[2].legend()

    plt.tight_layout()
    print("Graficos prontos")
    plt.show()


def main():

    print("=" * 50)
    print("  ML - RISCO DE PRODUTOS NO ESTOQUE")
    print("=" * 50)

    df = carregar_dados()

    if df is None:
        print("Processo encerrado - falha ao carregar dados")
        return

    df = tratar_dados(df)
    df = criar_features(df)
    df = criar_target(df)
    modelo_ml(df)
    graficos(df)

    print("\nProcesso finalizado com sucesso")


# garante que o main() so roda quando o arquivo e executado diretamente
# se outro script importar esse arquivo, o main nao e chamado automaticamente
if __name__ == "__main__":
    main()