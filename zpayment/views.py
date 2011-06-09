#coding:utf-8
from annoying.decorators import render_to
from django.core.mail import mail_admins
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from webmoney.forms import SettledPaymentForm, UnSettledPaymentForm
from webmoney.models import Invoice, Purse
from webmoney.models import Payment as WebmoneyPayment
from webmoney.signals import webmoney_payment_accepted
from zpayment.forms import PrerequestForm, PaymentNotificationForm
from zpayment.models import PrePayment, Payment
try:
    from hashlib import md5
except ImportError:
    from md5 import md5


@csrf_exempt
@require_POST
def result(request):
    form = PrerequestForm(request.POST)
    if form.is_valid() and form.cleaned_data['LMI_PREREQUEST']:
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
            pre_payment.webmoney_invoice = invoice
            pre_payment.save()
        return HttpResponse("YES")
    form = PaymentNotificationForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        purse = Purse.objects.get(purse=cleaned_data['LMI_PAYEE_PURSE'])
        key = "%s%s%s%s%s%s%s%s%s%s" % (
            purse.purse,
            cleaned_data['LMI_PAYMENT_AMOUNT'],
            cleaned_data['LMI_PAYMENT_NO'],
            cleaned_data['LMI_MODE'],
            cleaned_data['LMI_SYS_INVS_NO'],
            cleaned_data['LMI_SYS_TRANS_NO'],
            cleaned_data['LMI_SYS_TRANS_DATE'].strftime('%Y%m%d %H:%M:%S'),
            purse.secret_key,
            cleaned_data['LMI_PAYER_PURSE'],
            cleaned_data['LMI_PAYER_WM']
        )
        generated_hash = md5(key).hexdigest().upper()
        payment_no = cleaned_data['LMI_PAYMENT_NO']
        if Payment.objects.filter(webmoney_payment__payment_no=payment_no):
            mail_admins('Dublicate payment', 'Payment NO is %s.' % payment_no, fail_silently=True)
            return HttpResponse("OK")
        if generated_hash == form.cleaned_data['LMI_HASH']:
            payment = WebmoneyPayment(
                payee_purse=purse,
                amount=cleaned_data['LMI_PAYMENT_AMOUNT'],
                payment_no=payment_no,
                mode=cleaned_data['LMI_MODE'],
                sys_invs_no=cleaned_data['LMI_SYS_INVS_NO'],
                sys_trans_no=cleaned_data['LMI_SYS_TRANS_NO'],
                sys_trans_date=cleaned_data['LMI_SYS_TRANS_DATE'],
                payer_purse=cleaned_data['LMI_PAYER_PURSE'],
                payer_wm=cleaned_data['LMI_PAYER_WM'],
                paymer_number=cleaned_data['LMI_PAYMER_NUMBER'],
                paymer_email=cleaned_data['LMI_PAYMER_EMAIL'],
                telepat_phonenumber=cleaned_data['LMI_TELEPAT_PHONENUMBER'],
                telepat_orderid=cleaned_data['LMI_TELEPAT_ORDERID'],
                payment_creditdays=cleaned_data['LMI_PAYMENT_CREDITDAYS']
            )
            try:
                invoice = Invoice.objects.get(payment_no=payment_no)
                payment.invoice = invoice
            except Invoice.DoesNotExist:
                subject = 'Unprocessed payment without invoice!',
                message = 'Payment NO is %s.' % payment_no
                mail_admins(subject, message, fail_silently=True)
            payment.save()
            Payment.objects.create(
                webmoney_payment=payment,
                zp_type_pay=cleaned_data['ZP_TYPE_PAY']
            )
            webmoney_payment_accepted.send(
                sender=payment.__class__, payment=payment
            )
            return HttpResponse("OK")
        else:
            subject = 'Unprocessed payment with incorrect hash!'
            message = 'Payment NO is %s.' % payment_no
            mail_admins(subject, message, fail_silently=True)
            return HttpResponseBadRequest("Incorrect hash")
    return HttpResponseBadRequest("Unknown error!")


@csrf_exempt
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


@csrf_exempt
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
