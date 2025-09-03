import oracledb

# Oracle connection info
ORACLE_CONFIG = {
    "user": "PHARM",
    "password": "xeon",
    "dsn": "192.168.10.6:1521/XE",
}


def fetch_medicaments():
    with oracledb.connect(**ORACLE_CONFIG) as connection:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                M.med_id,
                M.med_commercial_name,
                SUM(NVL(P.prd_qte, 0)) AS total_qte,
                P.prd_date_peremption
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

    result = [
        {
            "med_id": row[0],
            "name": row[1],
            "quantity": row[2],
            "expiration_date": row[3],
        }
        for row in rows
    ]
    
    return result
from datetime import date, timedelta
from django.db.models import Sum
from .models import Medicament, MedicamentSummary

def update_medicaments():
    """Fetch data from Oracle and save into SQLite"""
    print("hiiii")
    data = fetch_medicaments()

    # Clear old raw data
    Medicament.objects.all().delete()

    # Save new raw data
    for row in data:
        print(row)
        Medicament.objects.create(
            med_id=row['med_id'],
            name=row['name'],
            quantity=row['quantity'],
            expiration_date=row['expiration_date']
        )

    # Update summary
    update_med_summary()


def update_med_summary():
    """Compute quantities by expiration ranges and save in summary table"""
    today = date.today()
    three_months = today + timedelta(days=90)
    six_months = today + timedelta(days=180)

    # Clear old summaries
    MedicamentSummary.objects.all().delete()

    meds = Medicament.objects.values('med_id', 'name', 'expiration_date').distinct()
    print("med"+ meds)
    for med in meds:
        med_id = med['med_id']
        med_obj = Medicament.objects.filter(med_id=med_id).first()

        qty_lt_3m = Medicament.objects.filter(
            med_id=med_id,
            expiration_date__lte=three_months
        ).aggregate(total=Sum('quantity'))['total'] or 0

        qty_3_6m = Medicament.objects.filter(
            med_id=med_id,
            expiration_date__gt=three_months,
            expiration_date__lte=six_months
        ).aggregate(total=Sum('quantity'))['total'] or 0

        qty_gt_6m = Medicament.objects.filter(
            med_id=med_id,
            expiration_date__gt=six_months
        ).aggregate(total=Sum('quantity'))['total'] or 0

        MedicamentSummary.objects.create(
            med=med_obj,
            qty_lt_3m=qty_lt_3m,
            qty_3_6m=qty_3_6m,
            qty_gt_6m=qty_gt_6m
        )

"""
from oracledb import connect

ORACLE_CONFIG = {
    "user": "your_username",
    "password": "your_password",
    "dsn": "192.168.10.6:1521/XE",
}

def fetch_medicaments():
    with connect(**ORACLE_CONFIG) as connection:
        with connection.cursor() as cursor:
            query = """
"""

            SELECT med_commercial_name,
                   M.med_id,
                   SUM(NVL(P.prd_qte, 0)),
                   prd_date_peremption
            FROM STP_PRODUITS P
            JOIN stp_medicament M ON P.prd_med_id = M.med_id
            WHERE TO_DATE(prd_date_peremption, 'DD/MM/RRRR') > TRUNC(SYSDATE)
            GROUP BY med_commercial_name, M.med_id, prd_date_peremption
            """
"""

            cursor.execute(query)
            rows = cursor.fetchall()

    result = [
        {
            "name": row[0],
            "med_id": row[1],
            "quantity": row[2],
            "expiration_date": row[3],
        }
        for row in rows
    ]
    return result
"""