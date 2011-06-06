#coding:utf-8
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from webmoney.models import Invoice
from webmoney.models import Payment as WebmoneyPayment
from webmoney.views import result as webmoney_result
from zpayment.forms import PrerequestForm, PaymentNotificationForm
from zpayment.models import PrePayment, Payment
from webmoney.forms import SettledPaymentForm, UnSettledPaymentForm
from annoying.decorators import render_to


@csrf_exempt
@require_POST
def result(request):
    form = PrerequestForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        pre_payment = PrePayment(
            id_pay=cleaned_data['ID_PAY'],
            desc_pay=cleaned_data['DESC_PAY'],
            zp_type_pay=cleaned_data['ZP_TYPE_PAY']
        )
        payment_no = cleaned_data['LMI_PAYMENT_NO']
        try:
            invoice = Invoice.objects.get(payment_no=payment_no)
        except Invoice.DoesNotExist:
            return HttpResponseBadRequest(
                "Invoice with number %s not found." % payment_no
            )
        else:
            pre_payment.invoice = invoice
            pre_payment.save()
    response = webmoney_result(request)
    form = PaymentNotificationForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        payment_no = cleaned_data['LMI_PAYMENT_NO']
        webmoney_payment = WebmoneyPayment.objects.get(payment_no=payment_no)
        Payment.objects.create(
            webmoney_payment=webmoney_payment,
            zp_type_pay=cleaned_data['ZP_TYPE_PAY']
        )
    return response


@render_to('zpayment/success.html')
def success(request):
    response = {}
    if request.method == 'POST':
        form = SettledPaymentForm(request.POST)
        if form.is_valid():
            response['id'] = form.cleaned_data['LMI_PAYMENT_NO']
            response['sys_invs_no'] = form.cleaned_data['LMI_SYS_INVS_NO']
            response['sys_trans_no'] = form.cleaned_data['LMI_SYS_TRANS_NO']
            response['date'] = form.cleaned_data['LMI_SYS_TRANS_DATE']
    return response


@render_to('zpayment/fail.html')
def fail(request):
    response = {}
    if request.method == 'POST':
        form = UnSettledPaymentForm(request.POST)
        if form.is_valid():
            response['id'] = form.cleaned_data['LMI_PAYMENT_NO']
            response['sys_invs_no'] = form.cleaned_data['LMI_SYS_INVS_NO']
            response['sys_trans_no'] = form.cleaned_data['LMI_SYS_TRANS_NO']
            response['date'] = form.cleaned_data['LMI_SYS_TRANS_DATE']
    return response
