#coding:utf-8
from django.db import models
from django.db.utils import DatabaseError
from webmoney.models import Purse
from zpayment.conf import ZPAYMENT_SHOP_ID, ZPAYMENT_SECRET_KEY

try:
    Purse.objects.get_or_create(
        purse=ZPAYMENT_SHOP_ID, secret_key=ZPAYMENT_SECRET_KEY
    )
except DatabaseError:
    pass


class Invoice(models.Model):

    webmoney_invoice = models.ForeignKey('webmoney.Invoice')
    client_mail = models.EmailField(null=True, blank=True)
    zp_sign = models.CharField(max_length=255)


class PrePayment(models.Model):

    webmoney_invoice = models.ForeignKey('webmoney.Invoice')
    id_pay = models.CharField(max_length=255)
    desc_pay = models.TextField()
    zp_type_pay = models.CharField(max_length=255)


class Payment(models.Model):

    webmoney_payment = models.ForeignKey('webmoney.Payment')
    zp_type_pay = models.CharField(max_length=255)
