#coding:utf-8
from django.conf import settings


ZPAYMENT_SHOP_ID = getattr(settings, 'ZPAYMENT_SHOP_ID')
ZPAYMENT_PASSWORD_INITIALIZATION = getattr(settings, 'ZPAYMENT_PASSWORD_INITIALIZATION', None)