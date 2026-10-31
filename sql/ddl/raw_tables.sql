CREATE TABLE raw.orders
(
    order_id                      TEXT PRIMARY KEY,
    customer_id                   TEXT        NOT NULL,
    order_status                  VARCHAR(32) NOT NULL,
    order_purchase_timestamp      TIMESTAMP   NOT NULL,
    order_approved_at             TIMESTAMP,
    order_delivered_carrier_date  TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE raw.products
(
    product_id                 TEXT PRIMARY KEY,
    product_category_name      TEXT,
    product_name_lenght        INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty         INTEGER,
    product_weight_g           INTEGER,
    product_length_cm          INTEGER,
    product_height_cm          INTEGER,
    product_width_cm           INTEGER
);

CREATE TABLE raw.order_items
(
    order_id            TEXT,
    order_item_id       INTEGER,
    product_id          TEXT      NOT NULL,
    seller_id           TEXT      NOT NULL,
    shipping_limit_date TIMESTAMP NOT NULL,
    price               NUMERIC   NOT NULL CHECK ( price >= 0 ),
    freight_value       NUMERIC   NOT NULL CHECK (freight_value >= 0 ),

    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_order
        FOREIGN KEY (order_id)
            REFERENCES raw.orders (order_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
            REFERENCES raw.products (product_id)
);