import oracledb
from .models import Medicament, Medicament2

ORACLE_CONFIG = {
    "user": "PHARM",
    "password": "xeon",
    "dsn": "192.168.10.6:1521/XE",
}

def fetch_medicaments(start_date, end_date):
    with oracledb.connect(**ORACLE_CONFIG) as connection:
        with connection.cursor() as cursor:
            
            create_function_sql = """
            CREATE OR REPLACE FUNCTION CALC_REMISE_UG (
                XPRIX  IN NUMBER,
                XQTE   IN VARCHAR2,
                XTX_UG IN NUMBER
            ) RETURN NUMBER AS
                VAL        NUMBER;
                XQTE_UG    NUMBER;
                XTX_REMISE NUMBER;
                XMT_REMISE NUMBER;
            BEGIN
                XQTE_UG := FLOOR((NVL(XTX_UG, 0) * NVL(XQTE, 0)) / 100);
                XTX_REMISE := (NVL(XTX_UG, 0) * 100) / (NVL(XTX_UG, 0) + 100);
                XMT_REMISE := (XTX_REMISE * ((NVL(XPRIX, 0) * (NVL(XQTE, 0))))) / 100;
                RETURN NVL(XMT_REMISE, 0);
            END;
            """
            cursor.execute(create_function_sql)
            # 2. Exécuter la requête SELECT
            select_sql = f"""
                SELECT 
                M.med_id,
                M.med_commercial_name,
                SUM(CASE 
                        WHEN TO_DATE(P.prd_date_peremption, 'DD/MM/RRRR') BETWEEN TO_DATE('{start_date}', 'DD/MM/YYYY') 
                                               AND TO_DATE('{end_date}', 'DD/MM/YYYY')
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS QTE,
                SUM(CASE 
                        WHEN TO_DATE(P.prd_date_peremption, 'DD/MM/RRRR') BETWEEN TO_DATE('{start_date}', 'DD/MM/YYYY') 
                                               AND TO_DATE('{end_date}', 'DD/MM/YYYY')
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS VAL_ACHAT
            FROM 
                STP_PRODUITS P
            JOIN 
                (SELECT DISTINCT med_id, med_commercial_name FROM STP_MEDICAMENT) M
                ON P.prd_med_id = M.med_id
            GROUP BY 
                M.med_id,
                M.med_commercial_name
            """
            cursor.execute(select_sql)
            rows = cursor.fetchall()
    return rows




def update_medicaments2(start_date, end_date):
    """Fetch data from Oracle and save into SQLite"""
    data = fetch_medicaments(start_date, end_date)
    # Clear old raw data
    Medicament2.objects.update(qte=0, valeur_achat=0)
    # Save new raw data
    for med_id, name, qte, val_achat in data:
        Medicament2.objects.filter(med_id=med_id).update(
        qte=qte,
        valeur_achat=val_achat
    )