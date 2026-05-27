from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    TicketViewSet,
    api_root,
    current_user,
    dashboard_stats,
    register_user,
    admin_all_tickets
)

# ================= ROUTER =================
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='tickets')

# ================= URL PATTERNS =================
urlpatterns = [

    # Custom APIs
    path('', api_root),
    path('dashboard/', dashboard_stats),
    path('me/', current_user),
    path('register/', register_user),

    # ⭐ ADMIN API (ALL REQUESTS)
    path('admin/tickets/', admin_all_tickets),
]

# include router urls LAST
urlpatterns += router.urls
