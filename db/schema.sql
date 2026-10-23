CREATE TABLE dim_member (
    id              SERIAL PRIMARY KEY,
    member_id       INTEGER NOT NULL UNIQUE,
    year_joined     INTEGER NOT NULL,   -- -1 = unknown
    gender          VARCHAR(16) NOT NULL
        CHECK (gender IN ('Male', 'Female', 'Unknown'))
);

CREATE TABLE dim_datetime (
    id              SERIAL PRIMARY KEY,
    timestamp_utc   TIMESTAMPTZ NOT NULL UNIQUE,   -- canonical instant
    year            INTEGER,                       -- Danish local time, below
    month           INTEGER NOT NULL,
    month_name      VARCHAR(16) NOT NULL,
    week            INTEGER NOT NULL,
    weekday         VARCHAR(16) NOT NULL,
    day             INTEGER NOT NULL,
    timeslot_type   VARCHAR(32) NOT NULL
        CHECK (timeslot_type IN ('outside_schedule', 'lecture', 'break')),
    timeslot        VARCHAR(16) NOT NULL
        CHECK (timeslot IN (
            '0000_0815', '0815_1000', '1000_1015', '1015_1200', '1200_1230',
            '1230_1415', '1415_1430', '1430_1615', '1615_2400'
        )),
    hour            INTEGER NOT NULL,
    minute          INTEGER NOT NULL
);

CREATE TABLE dim_product (
    id                  SERIAL PRIMARY KEY,
    product_id          INTEGER NOT NULL,
    name                VARCHAR(255) NOT NULL,
    price               NUMERIC(10, 2) NOT NULL,
    active_state        VARCHAR(16) NOT NULL
        CHECK (active_state IN ('inactive', 'active')),
    category_major      VARCHAR(255) NOT NULL DEFAULT 'Uncategorised',
    category_minor      VARCHAR(255) NOT NULL DEFAULT 'Uncategorised',
    category_sub        VARCHAR(255) NOT NULL DEFAULT 'Uncategorised',
    category_subsub     VARCHAR(255) NOT NULL DEFAULT 'Uncategorised',
    valid_from          timestamptz NOT NULL,
    valid_to            timestamptz,  -- NULL = still current
    version             INTEGER NOT NULL DEFAULT 1,
    UNIQUE (product_id, version)
);

CREATE TABLE fact_sale (
    dim_member      INTEGER NOT NULL REFERENCES dim_member (id),
    dim_product     INTEGER NOT NULL REFERENCES dim_product (id),
    dim_datetime    INTEGER NOT NULL REFERENCES dim_datetime (id),
    quantity        INTEGER NOT NULL,
    price           NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (dim_member, dim_product, dim_datetime)
);
