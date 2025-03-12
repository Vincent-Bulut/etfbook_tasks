WITH RECURSIVE CTE_transactions AS (
    SELECT
        transaction_id,
        etf_symbol,
        amount,
        transaction_date,
        parent_transaction_id,
        transaction_id AS primary_transaction_id
    FROM transactions
    WHERE parent_transaction_id IS NULL

    UNION ALL

    SELECT
        t.transaction_id,
        t.etf_symbol,
        t.amount,
        t.transaction_date,
        t.parent_transaction_id,
        th.primary_transaction_id
    FROM CTE_transactions th
    JOIN transactions t
        ON th.transaction_id = t.parent_transaction_id
)

--select * from CTE_transactions

SELECT
    primary_transaction_id,
    SUM(amount) AS total_amount
FROM CTE_transactions
GROUP BY primary_transaction_id
ORDER BY primary_transaction_id;