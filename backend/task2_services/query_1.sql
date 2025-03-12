
WITH monthly_sales AS (
    SELECT
        EXTRACT(MONTH FROM sale_date) AS month_number,
        region,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY month_number, region
),
sales_with_lag AS (
    SELECT
        month_number,
        region,
        total_sales,
        LAG(total_sales, 1, 0) OVER (
            PARTITION BY region
            ORDER BY month_number
        ) AS prev_month_sales
    FROM monthly_sales
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