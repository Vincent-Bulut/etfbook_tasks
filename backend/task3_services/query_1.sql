

WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(t.amount) AS total_spent
    FROM customers c
    JOIN customer_transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT
    customer_id,
    name,
    total_spent,
    CASE
        WHEN total_spent < 500 THEN 'Segment 1'
        WHEN total_spent BETWEEN 500 AND 1500 THEN 'Segment 2'
        ELSE 'Segment 3'
    END AS customer_segment
FROM customer_spending
ORDER BY total_spent DESC;