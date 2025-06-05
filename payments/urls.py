from django.urls import path
from .views import InitiatePaymentView, PaymentStatusView

urlpatterns = [
    path('payments', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/<int:payment_id>', PaymentStatusView.as_view(), name='payment-status'),
    #path('payments/verify/<int:payment_id>', VerifyPaymentView.as_view(), name='verify-payment')
]