
WITH sales_with_lag AS (
    SELECT
        EXTRACT(MONTH FROM sale_date) AS month_number
        region,
        SUM(amount) AS total_sales,
        LAG(SUM(amount), 1, 0) OVER (
            PARTITION BY region
            ORDER BY EXTRACT(MONTH FROM sale_date)
        ) AS prev_month_sales
    FROM sales
    GROUP BY month_number, region
)

SELECT
    month_number,
    region,
    total_sales,
    prev_month_sales,
    COALESCE(ROUND(
    CASE
        WHEN prev_month_sales = 0 THEN NULL  -- Éviter division par zéro
        ELSE ((total_sales - prev_month_sales) / prev_month_sales * 100)::NUMERIC
    END, 2
), 0) AS percentage_change
FROM sales_with_lag
ORDER BY region, month_number;