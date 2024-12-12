from django.urls import path, include
from . import views

app_name = "accounts"



urlpatterns = [
    # path("api/v1/", include("accounts.api.v1.urls")),    
    # path('owner-authentication/', views.OwnerRegisterLoginView.as_view(), name='owner-authentication'),
    # path('owner-authentication/login/<str:phone_number>', views.OwnerloginView.as_view(), name='owner-login'),
]