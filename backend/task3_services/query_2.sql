
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(t.amount) AS total_spent
    FROM customers c
    JOIN customer_transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.name
),
customer_segments AS (
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
),
segment_transactions AS (
    SELECT
        cs.customer_segment,
        t.etf_symbol,
        COUNT(t.transaction_id) AS transaction_count,
        SUM(t.amount) AS total_segment_spent,
        ROUND(AVG(t.amount)::numeric, 2) AS avg_transaction_value
    FROM customer_segments cs
    JOIN customer_transactions t ON cs.customer_id = t.customer_id
    GROUP BY cs.customer_segment, t.etf_symbol
),
segment_totals AS (
    SELECT
        customer_segment,
        SUM(total_segment_spent) AS segment_total
    FROM segment_transactions
    GROUP BY customer_segment
)
SELECT
    st.customer_segment,
    st.etf_symbol,
    st.avg_transaction_value,
    ROUND((st.total_segment_spent / stt.segment_total * 100)::numeric, 2) AS etf_percentage_share
FROM segment_transactions st
JOIN segment_totals stt ON st.customer_segment = stt.customer_segment
ORDER BY st.customer_segment, etf_percentage_share DESC;
