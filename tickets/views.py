from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Ticket
from .serializers import TicketSerializer


# ==============================
# USER + ADMIN TICKET API (VIEWSET)
# ==============================
class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    # ✅ ADMIN sees ALL tickets
    # ✅ USER sees only own tickets
    def get_queryset(self):

        if self.request.user.is_staff:
            return Ticket.objects.all().order_by("-created_at")

        return Ticket.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    # ==============================
    # Intelligent ticket creation
    # ==============================
    def perform_create(self, serializer):

        description = serializer.validated_data.get(
            "description", ""
        ).lower()

        high_keywords = [
            "server", "crash", "down",
            "not working", "not starting",
            "system down", "failure"
        ]

        medium_keywords = [
            "login", "error", "slow",
            "issue", "problem"
        ]

        priority = "LOW"

        for word in high_keywords:
            if word in description:
                priority = "HIGH"
                break

        if priority != "HIGH":
            for word in medium_keywords:
                if word in description:
                    priority = "MEDIUM"
                    break

        serializer.save(
            user=self.request.user,
            priority=priority
        )

    def update(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can update tickets."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can update tickets."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().partial_update(request, *args, **kwargs)


# ==============================
# API ROOT
# ==============================
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):

    return Response({
        "admin_portal": request.build_absolute_uri("/admin/"),
        "register": request.build_absolute_uri("/api/register/"),
        "login_token": request.build_absolute_uri("/api/token/"),
        "refresh_token": request.build_absolute_uri("/api/token/refresh/"),
        "current_user": request.build_absolute_uri("/api/me/"),
        "tickets": request.build_absolute_uri("/api/tickets/"),
        "dashboard": request.build_absolute_uri("/api/dashboard/"),
        "admin_tickets_api": request.build_absolute_uri("/api/admin/tickets/"),
    })


# ==============================
# DASHBOARD API
# ==============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    user = request.user
    tickets = Ticket.objects.all() if user.is_staff else Ticket.objects.filter(user=user)

    data = {
        "total_tickets": tickets.count(),
        "open_tickets": tickets.filter(status="OPEN").count(),
        "resolved_tickets": tickets.filter(status="RESOLVED").count(),
        "high_priority_tickets": tickets.filter(priority="HIGH").count(),
    }

    return Response(data)


# ==============================
# ADMIN ALL TICKETS API (OPTIONAL EXTRA)
# ==============================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_all_tickets(request):

    tickets = Ticket.objects.all().order_by("-created_at")
    serializer = TicketSerializer(tickets, many=True)

    return Response(serializer.data)


# ==============================
# USER REGISTER API
# ==============================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({"message": "User created successfully"})


# ==============================
# CURRENT USER API
# ==============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
    })


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    return render(request, "dashboard.html", {"active_nav": "dashboard"})


def create_ticket_page(request):
    return render(request, "create_ticket.html", {"active_nav": "create"})


def tickets_page(request):
    return render(request, "tickets.html", {"active_nav": "tickets"})
