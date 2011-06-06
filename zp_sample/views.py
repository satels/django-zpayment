#coding:utf-8
from annoying.decorators import render_to
from django.template import loader, RequestContext
from webmoney.models import Invoice
from zpayment.forms import PaymentRequestForm, get_zp_sign


@render_to('zp_sample/simple_payment.html')
def simple_payment(request):
    response = {}
    invoice = Invoice.objects.create(user=request.user)
    payment_no = invoice.payment_no
    description = loader.render_to_string('zp_sample/simple_payment_desc.txt',
        context_instance=RequestContext(request)
    )[:255]
    amount = '101.42'
    zp_sign = get_zp_sign(payment_no, amount)
    initial = {
        'LMI_PAYMENT_NO': invoice.payment_no,
        'LMI_PAYMENT_DESC': description,
        'LMI_PAYMENT_AMOUNT': amount,
        'CLIENT_MAIL': 'testmail@example.com',
        'ZP_SIGN': zp_sign
    }
    response['form'] = PaymentRequestForm(initial=initial)

    return response

