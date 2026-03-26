from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

from tickets.views import (
    login_page,
    dashboard_page,
    create_ticket_page,
    my_tickets_page,
    register_page
)

urlpatterns = [

    
    path('admin/', admin.site.urls),

    #api ban rahi hai
    path('api/', include('tickets.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('', login_page),                 # Login Page
    path('register/', register_page),     # Register Page
    path('dashboard/', dashboard_page),
    path('create-ticket/', create_ticket_page),
    path('my-tickets/', my_tickets_page),

   
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='forgot_password.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]