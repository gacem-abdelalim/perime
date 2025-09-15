import oracledb
from .models import Medicament
ORACLE_CONFIG = {
    "user": "PHARM",
    "password": "xeon",
    "dsn": "192.168.10.6:1521/XE",
}

def fetch_medicaments():
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
            select_sql = """
                SELECT 
                M.med_id,
                M.med_commercial_name,
                SUM(NVL(P.prd_qte, 0)) AS total_quantity,
                SUM((PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG)) AS total_val_achat,
                SUM(CASE 
                        WHEN P.prd_date_peremption < ADD_MONTHS(SYSDATE, 3) 
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_less_than_3_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 3)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 6)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_between_3_and_6_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 6)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 12)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_between_6_and_12_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 12)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 18)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_between_12_and_18_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 18)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 24)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_between_18_and_24_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 24)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 36)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_between_24_and_36_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 36)
                        THEN NVL(P.prd_qte, 0) ELSE 0 
                    END) AS qte_more_than_36_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption < ADD_MONTHS(SYSDATE, 3) 
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS qte_less_than_3_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 3)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 6)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS val_achat_3_and_6_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 6)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 12)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS val_achat_6_and_12_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 12)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 18)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS qte_between_12_and_18_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 18)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 24)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS val_achat_between_18_and_24_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 24)
                        AND P.prd_date_peremption < ADD_MONTHS(SYSDATE, 36)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS val_achat_between_24_and_36_months,
                SUM(CASE 
                        WHEN P.prd_date_peremption >= ADD_MONTHS(SYSDATE, 36)
                        THEN (PRD_QTE * PRD_PRIX_RV)
                        - ACHATS_NEW.CALC_REMISE_UG (PRD_PRIX_RV, PRD_QTE, PRD_TX_UG) ELSE 0 
                    END) AS val_achat_more_than_36_months
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
            """ 
            result = [
                {
                    "med_id": row[0],
                    "name": row[1],
                    "quantity": row[2],
                    "total_val_achat": row[3],
                    "qte_less_than_3_months": row[4],
                    "qte_between_3_and_6_months": row[5],
                    "qte_between_6_and_12_months": row[6],
                    "qte_between_12_and_18_months": row[7],
                    "qte_between_18_and_24_months": row[8],
                    "qte_between_24_and_36_months": row[9],
                    "qte_more_than_36_months": row[10],
                    "val_achat_less_than_3_months": row[11],
                    "val_achat_3_and_6_months": row[12],
                    "val_achat_6_and_12_months": row[13],
                    "val_achat_12_and_18_months": row[14],
                    "val_achat_between_18_and_24_months": row[15],
                    "val_achat_between_24_and_36_months": row[16],
                    "val_achat_more_than_36_months": row[17],
                }
                for row in rows
            ]
            """

    return rows




def update_medicaments():
    """Fetch data from Oracle and save into SQLite"""
    data = fetch_medicaments()
    
    # Clear old raw data
    Medicament.objects.all().delete()

    


    # Save new raw data
    for row in data:
        Medicament.objects.create(
            med_id=row[0],
            name=row[1],
            
            qte_total=row[2],
            val_total_achat=row[3],

            # Quantités par tranche
            qte_avant_3m=row[4],
            qte_apres_3m_avant_6m=row[5],
            qte_apres_6m_avant_12m=row[6],
            qte_apres_12m_avant_18m=row[7],
            qte_apres_18m_avant_24m=row[8],
            qte_apres_24m_avant_36m=row[9],
            qte_apres_36m=row[10],

            # Valeurs d’achat par tranche
            val_achat_avant_3m=row[11],
            val_achat_apres_3m_avant_6m=row[12],
            val_achat_apres_6m_avant_12m=row[13],
            val_achat_apres_12m_avant_18m=row[14],
            val_achat_apres_18m_avant_24m=row[15],
            val_achat_apres_24m_avant_36m=row[16],
            val_achat_apres_36m=row[17]
        )

