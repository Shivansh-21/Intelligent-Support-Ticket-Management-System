from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tickets.views import (
    create_ticket_page,
    dashboard_page,
    forgot_password_page,
    login_page,
    register_page,
    tickets_page,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('tickets.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('forgot-password/', forgot_password_page, name='forgot_password'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('create-ticket/', create_ticket_page, name='create_ticket'),
    path('tickets/', tickets_page, name='tickets'),
]
