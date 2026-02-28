import firebirdsql
import pandas as pd
import os

DB_PATH = r"C:\Users\Wellington Luiz\Documents\gas\dados_antigos\DADOS.FDB"
print("Connecting with pure python driver...")
try:
    con = firebirdsql.connect(
        host='localhost', 
        database=DB_PATH, 
        user='SYSDBA', 
        password='masterkey', 
        charset='UTF8'
    )
    print("Connection Successful!")

    query = """
        SELECT RDB$RELATION_NAME
        FROM RDB$RELATIONS
        WHERE RDB$VIEW_BLR IS NULL 
        AND (RDB$SYSTEM_FLAG IS NULL OR RDB$SYSTEM_FLAG = 0);
    """
    cur = con.cursor()
    cur.execute(query)
    tables = [row[0].strip() for row in cur.fetchall()]
    
    print(f"Tables: {tables}")
    for table in tables:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", con)
            out_file = os.path.join(os.path.dirname(DB_PATH), f"{table}.csv")
            df.to_csv(out_file, index=False)
            print(f"Exported {table} to CSV ({len(df)} rows)")
        except Exception as e:
            print(f"Could not export table {table}: {e}")
except Exception as e:
    print(f"Error: {e}")
