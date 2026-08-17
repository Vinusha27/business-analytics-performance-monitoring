# Architecture

The generator produces controlled, reproducible raw CSVs. The pipeline reads every source, removes exact duplicates, repairs missing customer regions, rejects invalid order items, records the quality outcome, and reloads all tables in a transactionally consistent order. The analytics layer joins normalized tables at query time; it is consumed directly by the Streamlit UI, FastAPI service, and report generator. SQLite provides zero-setup local operation; the schema uses portable relational SQL and a database URL setting supports a future PostgreSQL deployment.
