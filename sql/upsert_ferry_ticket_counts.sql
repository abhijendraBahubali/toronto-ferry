-- Upsert so re-running the pipeline updates existing rows instead of failing
-- on the primary key or inserting duplicates.
INSERT INTO ferry_ticket_counts (id, ticket_timestamp, redemption_count, sales_count)
VALUES (%s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE SET
    ticket_timestamp = EXCLUDED.ticket_timestamp,
    redemption_count = EXCLUDED.redemption_count,
    sales_count      = EXCLUDED.sales_count;
