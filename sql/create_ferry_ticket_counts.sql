CREATE TABLE IF NOT EXISTS ferry_ticket_counts (
    id               INTEGER     PRIMARY KEY,
    ticket_timestamp TIMESTAMP   NOT NULL,
    redemption_count INTEGER     NOT NULL,
    sales_count      INTEGER     NOT NULL
);
