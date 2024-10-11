from django.shortcuts import render

# Create your views here.

from rest_framework import authentication,permissions

from service.serializers import CustomerSerializer,WorkSerializer

from rest_framework import generics

from service.models import Customer,Work

from django.core.mail import send_mail

from service.permissions import OwnerOnly

from django.db.models import Sum

from twilio.rest import Client

import threading

from decouple import config

account_sid = config("account_sid")

auth_token = config("auth_token")

def sent_text_message(vehicle_no,customer_name,total):
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_="+18644775634",
    body=f"hi {customer_name} your vehicle {vehicle_no} service has been completed amount {total}",
    to='+917598488180'
    )
    print(message.sid)  
    
def sent_email_message(vehicle_number,customer_name,total):
    
    message=f"your vehicle {vehicle_number} is ready to deliver service amount {total}"
    
    subject="vechile service completion"
    
    send_mail(
                subject,message,"ssuhaibakther12@gmail.com",["suhaibakthers69@gmail.com",],fail_silently=False
            )


class CustomerListCreateView(generics.ListCreateAPIView):
    
    serializer_class=CustomerSerializer
    
    queryset=Customer.objects.all()
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAdminUser]
    
    def perform_create(self, serializer):

        return serializer.save(service_advisor=self.request.user)
    
class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=CustomerSerializer
    
    queryset=Customer.objects.all()
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAdminUser]
    
    def perform_update(self, serializer):
        
        work_status=serializer.validated_data.get("work_status")
        
        if work_status=="completed":
            
            print("sending mail")
            
            
            
            vehicle_number=serializer.validated_data.get("vehicle_number")
            
            customer_name=serializer.validated_data.get("name")
            
            total=Work.objects.filter(customer_object__name=customer_name).values("amount").aggregate(total=Sum("amount")).get("total",0)
            
            # sent_text_message(vehicle_number,customer_name,total)
            
            # sent_email_message(vehicle_number,customer_name,total)
            
            message_thread=threading.Thread(target=sent_text_message,args=(vehicle_number,customer_name,total))
            
            email_thread=threading.Thread(target=sent_email_message,args=(vehicle_number,customer_name,total))
            
            message_thread.start()
            
            email_thread.start()
            
        serializer.save()


class WorkCreateView(generics.CreateAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAdminUser]
    
    serializer_class=WorkSerializer
    
    def perform_create(self, serializer):
        
        id=self.kwargs.get("pk")
        
        cust_obj=Customer.objects.get(id=id)
        
        return serializer.save(customer_object=cust_obj)
    
    
class WorkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=WorkSerializer
    
    queryset=Work.objects.all()
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[OwnerOnly]