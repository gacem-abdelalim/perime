# Oracle connection info
ORACLE_CONFIG = {
    "user": "PHARM",
    "password": "xeon",
    "dsn": "192.168.10.6:1521/XE",
}

def fetch_medicaments():
    print("sqdsqdsq")
    # Connect to Oracle
    with oracledb.connect(**ORACLE_CONFIG) as connection:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                M.med_id,
                M.med_commercial_name,
                SUM(NVL(P.prd_qte, 0)),
                prd_date_peremption
            FROM 
                STP_PRODUITS P
            JOIN 
                (SELECT DISTINCT med_id, med_commercial_name FROM stp_medicament) M
                ON P.prd_med_id = M.med_id
            WHERE 
                TO_DATE(P.prd_date_peremption,'DD/MM/RRRR') > TRUNC(SYSDATE)
            GROUP BY 
                M.med_id, M.med_commercial_name, P.prd_date_peremption
            """
            cursor.execute(query)
            rows = cursor.fetchall()

    # Optional: convert to list of dicts for easier use
    result = [
        {
            "name": row[0],
            "med_id": row[1],
            "quantity": row[2],
            "expiration_date": row[3],
        }
        for row in rows
    ]
    print(result)
    return result