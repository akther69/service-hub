from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken

from service import views

urlpatterns = [
    path("token/",ObtainAuthToken.as_view()),
    
    path("customers/",views.CustomerListCreateView.as_view()),
    
    path("customers/<int:pk>/",views.CustomerRetrieveUpdateDestroyView.as_view()),
    
    path('customers/<int:pk>/add-work/',views.WorkCreateView.as_view()),
    
    path("works/<int:pk>/",views.WorkRetrieveUpdateDestroyView.as_view())
]
