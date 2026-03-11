# ML - Risco de Produtos Parados no Estoque

Este projeto usa Machine Learning para identificar quais produtos têm alta probabilidade de parar de vender, ou seja, ficarem parados no estoque sem gerar receita. Os dados vêm diretamente do banco **Contoso** no SQL Server e o modelo classifica cada produto como **Normal** ou **Em Risco**.

---

## O que o projeto faz

O algoritmo analisa o histórico de vendas de cada produto e aprende quais padrões indicam que um produto está deixando de vender. Com isso, em vez de um analista revisar produto por produto, o modelo faz isso automaticamente e aponta os casos mais críticos.

O critério principal é: **produto que ficou mais de 120 dias sem vender é classificado como Em Risco**. A partir daí, o modelo aprende outros padrões como queda de frequência, tendência de volume e comparação entre períodos.

---

## Estrutura do projeto

```
├── Previsao.py          script principal com todo o pipeline de ML
├── DataBase.sql         query SQL que busca os dados do banco
├── .env                 suas configuracoes de conexao (nao sobe pro GitHub)
├── .env.example         modelo do arquivo .env para referencia
├── .gitignore           arquivos que o Git deve ignorar
└── README.md            este arquivo
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
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Instale as dependências**

```bash
pip install pandas numpy sqlalchemy pyodbc python-dotenv matplotlib seaborn scikit-learn
```

**3. Configure o arquivo .env**

Copie o arquivo de exemplo e renomeie:

```bash
copy .env.example .env
```

Abra o arquivo `.env` e preencha com os seus dados:

```
DB_SERVIDOR=SEU_SERVIDOR\SQLEXPRESS
DB_BANCO=ContosoRetailDW
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

**conectar_banco** — lê as configurações do `.env` e cria a conexão com o SQL Server usando SQLAlchemy.

**carregar_query** — abre o arquivo `DataBase.sql` e lê o conteúdo como texto. O SQL fica separado do Python para manter o código organizado.

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

O arquivo `.env` nunca deve ser enviado para o GitHub pois contém informações do seu servidor. O `.gitignore` já está configurado para ignorá-lo automaticamente.

Caso outra pessoa clone este repositório, ela precisará criar o próprio `.env` com as configurações do ambiente dela. O arquivo `.env.example` serve como guia para isso.

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
- python-dotenv
