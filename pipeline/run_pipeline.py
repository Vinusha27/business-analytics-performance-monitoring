from __future__ import annotations
import json, sqlite3
import pandas as pd
from config import RAW, DATA, DB_PATH
from database.init_db import initialize_database
from pipeline.validate import validate

TABLES=("customers","products","sales_reps","orders","order_items")
def run_pipeline() -> dict[str,int]:
    tables={n:pd.read_csv(RAW/f"{n}.csv") for n in TABLES}; tables,summary=validate(tables); initialize_database()
    with sqlite3.connect(DB_PATH) as conn:
        for name in reversed(TABLES): conn.execute(f"DELETE FROM {name}")
        for name in TABLES: tables[name].to_sql(name,conn,if_exists="append",index=False)
    (DATA/"quality_summary.json").write_text(json.dumps(summary,indent=2)); return summary
if __name__ == '__main__': print(json.dumps(run_pipeline(),indent=2))
