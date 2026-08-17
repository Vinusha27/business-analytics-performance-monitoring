from __future__ import annotations
import pandas as pd

def validate(tables: dict[str,pd.DataFrame]) -> tuple[dict[str,pd.DataFrame],dict[str,int]]:
    """Apply transparent repair rules and return a quality summary."""
    summary={"records_processed":sum(map(len,tables.values())),"duplicates_removed":0,"records_rejected":0,"values_corrected":0,"missing_values":0}
    for name,df in tables.items():
        summary["missing_values"]+=int(df.isna().sum().sum()); before=len(df); tables[name]=df.drop_duplicates(); summary["duplicates_removed"]+=before-len(tables[name])
    c=tables["customers"]; missing=c.region.isna(); c.loc[missing,"region"]="Unknown"; summary["values_corrected"]+=int(missing.sum())
    i=tables["order_items"]; invalid=(i.quantity<=0)|(i.unit_price<0)|(i.discount<0)|(i.discount>1); summary["records_rejected"]+=int(invalid.sum()); tables["order_items"]=i.loc[~invalid].copy()
    valid_orders=set(tables["orders"].order_id); valid_products=set(tables["products"].product_id); i=tables["order_items"]; fk=~i.order_id.isin(valid_orders)|~i.product_id.isin(valid_products); summary["records_rejected"]+=int(fk.sum()); tables["order_items"]=i.loc[~fk].copy()
    return tables,summary
