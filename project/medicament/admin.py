import datetime
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import Medicament
from datetime import date, timedelta
from django.db.models import Sum
""" 
@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'qte_lt_6_mois', 'qte_6m_1an', 'qte_1_3_ans', 'qte_plus_3_ans')
    actions = ['export_to_excel']

    def qte_lt_6_mois(self, obj):
        today = date.today()
        six_months = today + timedelta(days=6*30)
        return Medicament.objects.filter(
            name=obj.name, expiration_date__lte=six_months
        ).aggregate(total=Sum('quantity'))['total'] or 0
    qte_lt_6_mois.short_description = "Qte < 6 mois"

    def qte_6m_1an(self, obj):
        today = date.today()
        six_months = today + timedelta(days=6*30)
        one_year = today + timedelta(days=365)
        return Medicament.objects.filter(
            name=obj.name,
            expiration_date__gt=six_months,
            expiration_date__lte=one_year
        ).aggregate(total=Sum('quantity'))['total'] or 0
    qte_6m_1an.short_description = "Qte 6 mois - 1 an"

    def qte_1_3_ans(self, obj):
        today = date.today()
        one_year = today + timedelta(days=365)
        three_years = today + timedelta(days=3*365)
        return Medicament.objects.filter(
            name=obj.name,
            expiration_date__gt=one_year,
            expiration_date__lte=three_years
        ).aggregate(total=Sum('quantity'))['total'] or 0
    qte_1_3_ans.short_description = "Qte 1 - 3 ans"

    def qte_plus_3_ans(self, obj):
        today = date.today()
        three_years = today + timedelta(days=3*365)
        return Medicament.objects.filter(
            name=obj.name,
            expiration_date__gt=three_years
        ).aggregate(total=Sum('quantity'))['total'] or 0
    qte_plus_3_ans.short_description = "Qte > 3 ans"

    # -------------------- Export Action --------------------
    def export_to_excel(self, request, queryset):
        # Create workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Medicaments"

        # Header
        headers = ['Name', 'Qte < 6 mois', 'Qte 6 mois - 1 an', 'Qte 1 - 3 ans', 'Qte > 3 ans']
        sheet.append(headers)

        # Data rows
        for obj in queryset:
            row = [
                obj.name,
                self.qte_lt_6_mois(obj),
                self.qte_6m_1an(obj),
                self.qte_1_3_ans(obj),
                self.qte_plus_3_ans(obj),
            ]
            sheet.append(row)

        # Prepare response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename=medicaments_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        workbook.save(response)
        return response

    export_to_excel.short_description = "Exporter la sélection vers Excel"

"""
""" 
import datetime
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Sum
from datetime import date, timedelta

from .models import Medicament
from .oracle_utils import fetch_medicaments   # import your Oracle fetcher

actions = ['export_to_excel']
@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ("name", "qte_lt_3m", "qte_3_6m", "qte_gt_6m")
    actions = ['export_to_excel']

    # -------------------- Sync Oracle before displaying --------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Fetch fresh data from Oracle
        oracle_data = fetch_medicaments()

        for item in oracle_data:
            Medicament.objects.update_or_create(
                med_id=item["med_id"],
                defaults={
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "expiration_date": item["expiration_date"],
                },
            )

        return super().get_queryset(request)

    # -------------------- Quantities --------------------
    def qte_lt_3m(self, obj):
        today = date.today()
        three_months = today + timedelta(days=90)
        return Medicament.objects.filter(
            med_id=obj.med_id,
            expiration_date__lte=three_months
        ).aggregate(total=Sum("quantity"))["total"] or 0
    qte_lt_3m.short_description = "Qty < 3M"

    def qte_3_6m(self, obj):
        today = date.today()
        three_months = today + timedelta(days=90)
        six_months = today + timedelta(days=180)
        return Medicament.objects.filter(
            med_id=obj.med_id,
            expiration_date__gt=three_months,
            expiration_date__lte=six_months
        ).aggregate(total=Sum("quantity"))["total"] or 0
    qte_3_6m.short_description = "Qty 3-6M"

    def qte_gt_6m(self, obj):
        today = date.today()
        six_months = today + timedelta(days=180)
        return Medicament.objects.filter(
            med_id=obj.med_id,
            expiration_date__gt=six_months
        ).aggregate(total=Sum("quantity"))["total"] or 0
    qte_gt_6m.short_description = "Qty > 6M"

    # -------------------- Export Action --------------------
    def export_to_excel(self, request, queryset):
        # Create workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Medicaments"

        # Header
        headers = ['Name', 'Qte < 6 mois', 'Qte 6 mois - 1 an', 'Qte 1 - 3 ans', 'Qte > 3 ans']
        sheet.append(headers)

        # Data rows
        for obj in queryset:
            row = [
                obj.name,
                self.qte_lt_6_mois(obj),
                self.qte_6m_1an(obj),
                self.qte_1_3_ans(obj),
                self.qte_plus_3_ans(obj),
            ]
            sheet.append(row)

        # Prepare response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename=medicaments_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        workbook.save(response)
        return response

    export_to_excel.short_description = "Exporter la sélection vers Excel"
"""
from django.contrib import admin
from .models import Medicament, MedicamentSummary

from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from .models import Medicament, MedicamentSummary
from .oracle_utils import update_medicaments

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('med_id', 'name', 'quantity', 'expiration_date')
    change_list_template = "admin/medicament_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-oracle/', self.admin_site.admin_view(self.sync_oracle), name="sync_oracle"),
        ]
        return custom_urls + urls

    def sync_oracle(self, request):
        try:
            update_medicaments()
            self.message_user(request, "Oracle data synchronized successfully!", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error: {str(e)}", level=messages.ERROR)
        return redirect("../")


@admin.register(MedicamentSummary)
class MedicamentSummaryAdmin(admin.ModelAdmin):
    list_display = ('med', 'qty_lt_3m', 'qty_3_6m', 'qty_gt_6m')