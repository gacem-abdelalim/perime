from django.db import models

class Medicament(models.Model):
    med_id = models.IntegerField()
    name = models.CharField(max_length=255)

    # Quantités
    qte_total = models.IntegerField(null=True, blank=True)
    qte_avant_3m = models.IntegerField(null=True, blank=True)
    qte_apres_3m_avant_6m = models.IntegerField(null=True, blank=True)
    qte_apres_6m_avant_12m = models.IntegerField(null=True, blank=True)
    qte_apres_12m_avant_18m = models.IntegerField(null=True, blank=True)
    qte_apres_18m_avant_24m = models.IntegerField(null=True, blank=True)
    qte_apres_24m_avant_36m = models.IntegerField(null=True, blank=True)
    qte_apres_36m = models.IntegerField(null=True, blank=True)

    # Valeurs d’achat
    val_total_achat = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_avant_3m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_3m_avant_6m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_6m_avant_12m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_12m_avant_18m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_18m_avant_24m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_24m_avant_36m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    val_achat_apres_36m = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    qte = models.IntegerField(null=True, blank=True)
    valeur_achat = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    class Meta:
        verbose_name = "Répartition automatique des péremptions"
        verbose_name_plural = "Répartition automatique des péremptions"

    def __str__(self):
        return self.name

class Medicament2(Medicament):  # hérite d'un modèle concret
    class Meta:
        proxy = True
        verbose_name = "Analyse personnalisée des péremptions"
        verbose_name_plural = "Analyse personnalisée des péremptions"