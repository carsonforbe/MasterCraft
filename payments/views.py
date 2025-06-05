from django.shortcuts import render
from django.conf import settings
from paystackapi.transaction import Transaction
import random
import string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializer import PaymentSerializer

# Create your views here.
class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):

        #converts the incoming data into a payment object
        serializer = PaymentSerializer(data=request.data)

        #validate the serializer and save
        if serializer.is_valid():
            payment = serializer.save()

            #generate unique reference
            ref = 'PYT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            #paystack API wrapper
            response = Transaction.initialize(
                name = payment.customer_name,
                email = payment.customer_email,
                amount = int(payment.amount * 100),#paystack uses cents
                reference = ref,#unique transaction reference
                callback = "https://yourdomain.com/payment/callback" #where paystack redirects the user after payment
            )

            #check if paystack accepted the request
            if response['status']:
                payment.gateway_reference = ref
                payment.save()
                return Response({
                    'status':'success',
                    'authorization_url':response['data']['authorization_url']
                }, status=status.HTTP_201_CREATED)
            return Response({'error':'payment failed',}, status=400)
        return Response(serializer.errors, status=400)

#verify the payment
"""class VerifyPaymentView(APIView):
    def get(self, request, reference):
        #confirm if the payment was successful
        response = Transaction.verify(reference) #confirm the reference
        if response['data']['status'] == 'success':
            #update th database, using Payment module incase many transactions
            Payment.objects.filter(
                gateway_reference = reference
            ).update(status='complete')
            return Response({'status':'completed'})
        return Response({'status':'fauled'}, status=400)"""""""""""
    
#check payment status
class PaymentStatusView(APIView):
    def get(self, request, payment_id, *args, **kwargs):
        try:
            payment = Payment.objects.get(id=payment_id)
            serializer = PaymentSerializer(payment)
            return Response({
                "status":"success",
                "message":"payment details retrieved successfuly",
                "payment":serializer.data
            }, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({
                "status":"failed",
                "message":"payment with given id not found",
            },status=status.HTTP_404_NOT_FOUND)