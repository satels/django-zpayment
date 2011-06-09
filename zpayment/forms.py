#coding:utf-8
from annoying.decorators import autostrip
from django import forms
from django.utils.translation import ugettext_lazy as _
from webmoney.forms import PaymentRequestForm as WebmoneyPaymentRequestForm, \
    PrerequestForm as WebmoneyPrerequestForm, \
    PaymentNotificationForm as WebmoneyPaymentNotificationForm
from zpayment import WMID_RE
from zpayment.conf import ZPAYMENT_SHOP_ID, ZPAYMENT_PASSWORD_INITIALIZATION
try:
    from hashlib import md5
except ImportError:
    from md5 import md5


def get_zp_sign(LMI_PAYMENT_NO, LMI_PAYMENT_AMOUNT):
    key = "%s%s%0.2f%s" % (
        ZPAYMENT_SHOP_ID, LMI_PAYMENT_NO, LMI_PAYMENT_AMOUNT,
        ZPAYMENT_PASSWORD_INITIALIZATION
    )
    return md5(key).hexdigest()


@autostrip
class PaymentRequestForm(WebmoneyPaymentRequestForm):

    CLIENT_MAIL = forms.EmailField(required=False, label=_('Client Email'))
    ZP_SIGN = forms.CharField(
        max_length=32, min_length=32,
        required=ZPAYMENT_PASSWORD_INITIALIZATION and True or False
    )

    def __init__(self, *args, **kwargs):
        super(PaymentRequestForm, self).__init__(*args, **kwargs)
        self.fields['LMI_PAYEE_PURSE'].initial = ZPAYMENT_SHOP_ID


@autostrip
class PrerequestForm(WebmoneyPrerequestForm):

    LMI_PAYEE_PURSE = forms.RegexField(regex=WMID_RE)

    LMI_PAYER_WM = forms.CharField()
    LMI_PAYER_PURSE = forms.CharField(required=False)

    LMI_MODE = forms.IntegerField(
        label=_('Test mode'), min_value=0, max_value=0, initial=0
    )
    DESC_PAY = forms.CharField(max_length=255, label=_('Pay Description'))
    ID_PAY = forms.CharField(label=_('Invoice Number in Z-Payment'))
    ZP_TYPE_PAY = forms.CharField(label=_('Z-Payment Pay Type'))

    def __init__(self, *args, **kwargs):
        super(PrerequestForm, self).__init__(*args, **kwargs)
        self.fields['LMI_PAYEE_PURSE'].regex = WMID_RE
        self.fields['LMI_PAYEE_PURSE'].initial = ZPAYMENT_SHOP_ID


@autostrip
class PaymentNotificationForm(WebmoneyPaymentNotificationForm):

    LMI_PAYEE_PURSE = forms.RegexField(regex=WMID_RE)

    LMI_PAYER_WM = forms.CharField()
    LMI_PAYER_PURSE = forms.CharField(required=False)

    LMI_MODE = forms.IntegerField(
        label=_('Test mode'), min_value=0, max_value=0, initial=0
    )
    ZP_TYPE_PAY = forms.CharField(label=_('Z-Payment Pay Type'))

    def __init__(self, *args, **kwargs):
        super(PaymentNotificationForm, self).__init__(*args, **kwargs)
        self.fields['LMI_PAYEE_PURSE'].regex = WMID_RE
        self.fields['LMI_PAYEE_PURSE'].initial = ZPAYMENT_SHOP_ID
