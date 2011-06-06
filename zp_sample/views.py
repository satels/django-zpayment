#coding:utf-8
from annoying.decorators import render_to
from django.template import loader, RequestContext
from webmoney.forms import SettledPaymentForm, UnSettledPaymentForm
from webmoney.models import Invoice, Purse
from zpayment.forms import PaymentRequestForm, get_zp_sign


@render_to('zp_sample/simple_payment.html')
def simple_payment(request):
    response = {}
    invoice = Invoice.objects.create(user=request.user)
    payment_no = invoice.payment_no
    purse = Purse.objects.all()[0]
    description = loader.render_to_string('zp_sample/simple_payment_desc.txt',
        context_instance=RequestContext(request)
    )[:255]
    zp_sign = get_zp_sign(payment_no, '101.42')
    initial = {
        'LMI_PAYEE_PURSE': purse,
        'LMI_PAYMENT_NO': invoice.payment_no,
        'LMI_PAYMENT_DESC': description,
        'CLIENT_MAIL': 'testmail@example.com',
        'ZP_SIGN': zp_sign
    }
    response['form'] = PaymentRequestForm(initial=initial)

    return response

@render_to('zp_sample/success.html')
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

@render_to('zp_sample/fail.html')
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
