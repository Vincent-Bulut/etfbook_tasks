WITH RECURSIVE CTE_transactions AS (
    -- Sélection des transactions primaires
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

    -- Recherche récursive des transactions secondaires
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
),

-- Agrégation des transactions non primaires
aggregated_non_primaries AS (
    SELECT
        primary_transaction_id,
        COALESCE(SUM(amount), 0) AS total_amount_no_primaries,
        COUNT(*) AS total_transaction_no_primaries
    FROM CTE_transactions
    WHERE transaction_id <> primary_transaction_id
    GROUP BY primary_transaction_id
)

SELECT
    c.primary_transaction_id,
    SUM(c.amount) AS total_amount,
    COUNT(c.transaction_id) AS total_transaction,
    COALESCE(a.total_amount_no_primaries, 0) AS total_amount_no_primaries,
    COALESCE(a.total_transaction_no_primaries, 0) AS total_transaction_no_primaries,
	(SELECT sum(amount) FROM transactions) as total_amount_over_all
FROM CTE_transactions c
INNER JOIN aggregated_non_primaries a
    ON c.primary_transaction_id = a.primary_transaction_id
GROUP BY c.primary_transaction_id, a.total_amount_no_primaries, a.total_transaction_no_primaries
ORDER BY c.primary_transaction_id;



