# Data dictionary

| Table | Key fields | Purpose |
|---|---|---|
| customers | customer_id, signup_date, region, customer_segment | Customer identity and segmentation |
| products | product_id, category, unit_price, cost | Product catalog and unit economics |
| sales_reps | sales_rep_id, region, team | Sales ownership |
| orders | order_id, customer_id, order_date, channel, status | Order-level business event |
| order_items | order_item_id, order_id, product_id, quantity, discount | Product-level transaction detail |

Net revenue is calculated only for completed orders as `quantity × unit_price × (1 − discount)`.
