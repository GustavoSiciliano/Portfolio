WITH Base AS (
    SELECT TOP (40000)
        fs.ProductKey,
        CAST(fs.DateKey AS date) AS DataVenda,
        fs.SalesQuantity
    FROM FactSales fs
),

Periodo AS (
    SELECT
        MIN(DataVenda) AS DataMinima,
        MAX(DataVenda) AS DataMaxima
    FROM Base
),

Resumo AS (
    SELECT
        ProductKey,
        MIN(DataVenda) AS PrimeiraVenda,
        MAX(DataVenda) AS UltimaVenda,
        SUM(SalesQuantity) AS TotalVendido,
        AVG(SalesQuantity) AS MediaVenda
    FROM Base
    GROUP BY ProductKey
),

Vendas30 AS (
    SELECT
        b.ProductKey,
        SUM(b.SalesQuantity) AS Vendas30Dias
    FROM Base b
    CROSS JOIN Periodo p
    WHERE b.DataVenda >= DATEADD(DAY,-30,p.DataMaxima)
    GROUP BY b.ProductKey
),

Vendas90 AS (
    SELECT
        b.ProductKey,
        SUM(b.SalesQuantity) AS Vendas90Dias
    FROM Base b
    CROSS JOIN Periodo p
    WHERE b.DataVenda >= DATEADD(DAY,-90,p.DataMaxima)
    GROUP BY b.ProductKey
)

SELECT
    r.ProductKey        AS IdProduto,
    p.ProductName       AS NomeProduto,
    p.BrandName         AS Marca,
    r.PrimeiraVenda     AS DataPrimeiraVenda,
    r.UltimaVenda       AS DataUltimaVenda,
    r.TotalVendido      AS TotalVendido,
    r.MediaVenda        AS MediaVenda,
    DATEDIFF(DAY,r.UltimaVenda,per.DataMaxima) AS DiasSemVenda,
    ISNULL(v30.Vendas30Dias,0) AS VendasUltimos30Dias,
    ISNULL(v90.Vendas90Dias,0) AS VendasUltimos90Dias,

    CASE
        WHEN DATEDIFF(DAY,r.UltimaVenda,per.DataMaxima) > 120 AND ISNULL(v30.Vendas30Dias,0)=0 THEN 'Alto Risco'
        WHEN DATEDIFF(DAY,r.UltimaVenda,per.DataMaxima) BETWEEN 30 AND 120 THEN 'Risco Medio'
        ELSE 'Normal'
    END AS ClassificacaoRisco

FROM Resumo r
JOIN DimProduct p ON r.ProductKey = p.ProductKey
CROSS JOIN Periodo per
LEFT JOIN Vendas30 v30 ON r.ProductKey = v30.ProductKey
LEFT JOIN Vendas90 v90 ON r.ProductKey = v90.ProductKey

ORDER BY DiasSemVenda DESC