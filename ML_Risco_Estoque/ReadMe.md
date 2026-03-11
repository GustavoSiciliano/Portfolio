# ML - Risco de Produtos Parados no Estoque

Este projeto usa Machine Learning para identificar quais produtos têm alta probabilidade de parar de vender, ou seja, ficarem parados no estoque sem gerar receita. Os dados vêm diretamente do banco **Contoso** no SQL Server e o modelo classifica cada produto como **Normal** ou **Em Risco**.

---

## O que o projeto faz

O algoritmo analisa o histórico de vendas de cada produto e aprende quais padrões indicam que um produto está deixando de vender. Com isso, em vez de um analista revisar produto por produto, o modelo faz isso automaticamente e aponta os casos mais críticos.

O critério principal é: **produto que ficou mais de 120 dias sem vender é classificado como Em Risco**. A partir daí, o modelo aprende outros padrões como queda de frequência, tendência de volume e comparação entre períodos.

---

## Estrutura do projeto

```
├── Previsao.py      script principal com todo o pipeline de ML
├── DataBase.sql     query SQL que busca os dados do banco
└── README.md        este arquivo
```

---

## Pré-requisitos

Antes de rodar o projeto você precisa ter instalado:

- Python 3.8 ou superior
- SQL Server com o banco Contoso disponível
- As bibliotecas Python listadas abaixo

---

## Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/GustavoSiciliano/Portfolio.git
cd Portfolio
```

**2. Instale as dependências**

```bash
pip install pandas numpy sqlalchemy pyodbc matplotlib seaborn scikit-learn
```

**3. Configure a conexão**

Abra o arquivo `Previsao.py` e atualize essas duas linhas no topo com o nome do seu servidor e banco:

```python
SERVIDOR = "SEU_SERVIDOR\\SQLEXPRESS"
BANCO    = "ContosoRetailDW"
```

Para saber o nome do seu servidor, abra o SQL Server Management Studio. O nome aparece na tela de login. Você também pode rodar essa query para confirmar:

```sql
SELECT @@SERVERNAME
```

**4. Execute o projeto**

```bash
python Previsao.py
```

---

## Como o pipeline funciona

O projeto segue um fluxo linear de etapas, cada uma representada por uma função no código.

**conectar_banco** — cria a conexão com o SQL Server usando SQLAlchemy, o que evita o warning de compatibilidade que ocorre ao usar pyodbc diretamente com o pandas.

**carregar_query** — abre o arquivo `DataBase.sql` e lê o conteúdo como texto. O SQL fica separado do Python para manter o código mais organizado e fácil de manter.

**carregar_dados** — executa a query no banco e retorna um DataFrame do pandas com todos os produtos e seus indicadores de venda.

**tratar_dados** — preenche valores nulos com zero e garante que os tipos das colunas estão corretos antes de passar para o modelo.

**criar_features** — cria duas novas colunas que ajudam o modelo a entender melhor o comportamento de cada produto:
- `IndiceQueda`: proporção das vendas dos últimos 30 dias em relação aos últimos 90. Quanto mais próximo de zero, mais o produto está caindo.
- `ScoreVenda`: aplica logaritmo na soma das vendas recentes para suavizar valores muito altos e não deixar produtos com volume grande dominarem o modelo.

**criar_target** — define o que o modelo vai prever. Produtos com mais de 120 dias sem vender recebem o valor 1 (Em Risco), os demais recebem 0 (Normal).

**modelo_ml** — treina um RandomForest com os dados, avalia a acurácia, roda cross-validation para confirmar que o resultado é consistente e exibe o relatório completo.

**graficos** — gera três visualizações para interpretar os resultados de forma visual.

---

## Entendendo os resultados

**Acurácia** indica a porcentagem geral de acertos do modelo. Um valor acima de 85% já é considerado bom para esse tipo de problema.

**Precision** diz: dos produtos que o modelo classificou como Em Risco, quantos realmente eram? Um valor baixo significa muitos alarmes falsos.

**Recall** diz: dos produtos que realmente eram Em Risco, quantos o modelo conseguiu encontrar? Este é o número mais importante — um recall alto significa que o modelo raramente deixa um produto em risco escapar.

**Cross-Validation** testa o modelo 5 vezes em partes diferentes dos dados para confirmar que o resultado não foi sorte. Se a variação entre os testes for pequena, o modelo é confiável.

**Matriz de Confusão** mostra os acertos e erros separados por categoria:
- Linha 1: produtos que eram Normais — quantos o modelo acertou e quantos classificou errado como Em Risco
- Linha 2: produtos que eram Em Risco — quantos o modelo acertou e quantos deixou escapar como Normal

---

## Entendendo os gráficos

**Distribuição de Dias Sem Venda** mostra quantos produtos ficaram X dias sem vender. A maioria tende a estar perto de zero, e os produtos no lado direito do gráfico são os que estão parados há mais tempo.

**Classificação de Produtos** é uma contagem simples mostrando a proporção entre produtos Normais e Em Risco no catálogo inteiro.

**Tendência de Vendas** é o gráfico mais informativo. Cada ponto representa um produto. O eixo horizontal mostra as vendas dos últimos 90 dias e o vertical mostra as vendas dos últimos 30 dias. Pontos laranjas (Em Risco) concentrados no canto inferior esquerdo indicam produtos que praticamente pararam de vender nos dois períodos.

---

## Observações importantes

As configurações de conexão ficam diretamente no `Previsao.py` no topo do arquivo. Quem clonar o repositório só precisa atualizar essas duas variáveis com os dados do próprio ambiente.

O critério de 120 dias para classificar um produto como Em Risco pode ser ajustado diretamente na função `criar_target` no arquivo `Previsao.py`, dependendo da realidade do negócio.

---

## Tecnologias utilizadas

- Python
- pandas
- numpy
- scikit-learn
- SQLAlchemy
- pyodbc
- matplotlib
- seaborn

---

## Versão em Inglês // English Version

# ML - Stock Risk: Identifying Products at Risk of Stopping Sales

This project uses Machine Learning to identify which products have a high probability of stopping sales, meaning they could sit idle in stock without generating revenue. Data comes directly from the **Contoso** database on SQL Server, and the model classifies each product as **Normal** or **At Risk**.

---

## What the project does

The algorithm analyzes the sales history of each product and learns which patterns indicate that a product is stopping selling. Instead of an analyst reviewing product by product, the model does this automatically and highlights the most critical cases.

The main criterion is: **any product that went more than 120 days without a sale is classified as At Risk**. From there, the model learns additional patterns such as frequency drop, volume trends, and period comparisons.

---

## Project structure

```
├── Previsao.py      main script with the full ML pipeline
├── DataBase.sql     SQL query that fetches data from the database
└── README.md        this file
```

---

## Requirements

Before running the project you need:

- Python 3.8 or higher
- SQL Server with the Contoso database available
- The Python libraries listed below

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/GustavoSiciliano/Portfolio.git
cd Portfolio
```

**2. Install dependencies**

```bash
pip install pandas numpy sqlalchemy pyodbc matplotlib seaborn scikit-learn
```

**3. Set up your connection**

Open `Previsao.py` and update these two lines at the top of the file with your own server and database names:

```python
SERVIDOR = "YOUR_SERVER\\SQLEXPRESS"
BANCO    = "ContosoRetailDW"
```

To find your server name, open SQL Server Management Studio — it appears on the login screen. You can also run this query to confirm:

```sql
SELECT @@SERVERNAME
```

**4. Run the project**

```bash
python Previsao.py
```

---

## How the pipeline works

**conectar_banco** — creates the connection to SQL Server using SQLAlchemy, which avoids the pandas compatibility warning that occurs with pyodbc directly.

**carregar_query** — opens the `DataBase.sql` file and reads its content as text. Keeping SQL separate from Python makes the code cleaner and easier to maintain.

**carregar_dados** — executes the query and returns a pandas DataFrame with all products and their sales indicators.

**tratar_dados** — fills null values with zero and ensures column types are correct before passing data to the model.

**criar_features** — creates two new columns that help the model better understand each product's behavior:
- `IndiceQueda`: proportion of the last 30 days sales relative to the last 90. The closer to zero, the more the product is declining.
- `ScoreVenda`: applies a logarithm to recent sales totals to smooth out very high values and prevent high-volume products from dominating the model.

**criar_target** — defines what the model will predict. Products with more than 120 days without a sale receive the value 1 (At Risk), others receive 0 (Normal).

**modelo_ml** — trains a RandomForest, evaluates accuracy, runs cross-validation to confirm consistency, and displays the full report.

**graficos** — generates three visualizations to interpret the results visually.

---

## Understanding the results

**Accuracy** shows the overall percentage of correct predictions. A value above 85% is considered good for this type of problem.

**Precision** answers: of the products the model classified as At Risk, how many actually were? A low value means many false alarms.

**Recall** answers: of the products that were truly At Risk, how many did the model find? This is the most important number — a high recall means the model rarely lets an at-risk product go undetected.

**Cross-Validation** tests the model 5 times on different parts of the data to confirm the result is consistent and not just luck. A small variation between tests means the model is reliable.

**Confusion Matrix** shows correct predictions and errors by category:
- Row 1: products that were Normal — how many the model got right and how many it wrongly flagged as At Risk
- Row 2: products that were At Risk — how many the model identified correctly and how many it missed

---

## Understanding the charts

**Days Without Sales Distribution** shows how many products went X days without selling. Most tend to cluster near zero, and products on the right side of the chart are the ones that have been idle the longest.

**Product Classification** is a simple count showing the proportion of Normal vs At Risk products across the entire catalog.

**Sales Trend** is the most informative chart. Each dot represents a product. The horizontal axis shows sales in the last 90 days and the vertical axis shows sales in the last 30 days. Orange dots (At Risk) concentrated in the bottom-left corner indicate products that have nearly stopped selling in both periods.

---

## Important notes

The connection details are set directly in `Previsao.py` at the top of the file. Anyone who clones this repository only needs to update those two variables to match their own environment.

The 120-day threshold for classifying a product as At Risk can be adjusted directly in the `criar_target` function inside `Previsao.py`, depending on the business context.

---

## Technologies used

- Python
- pandas
- numpy
- scikit-learn
- SQLAlchemy
- pyodbc
- matplotlib
- seaborn
