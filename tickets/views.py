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
            "server", "production", "prod down",
            "outage", "crash", "down",
            "not working", "not starting",
            "system down", "failure", "data loss",
            "security breach", "database down",
            "deployment failed", "payment failed",
            "website down", "api down"
        ]

        medium_keywords = [
            "login", "vpn", "email", "network",
            "printer", "software", "laptop",
            "access", "permission", "error",
            "slow", "bug", "issue", "problem"
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
        "system": "TechNova Solutions Intelligent Ticket Resolution System",
        "field": "IT service management",
        "region": "Bengaluru, India",
        "admin_portal": request.build_absolute_uri("/admin/"),
        "register": request.build_absolute_uri("/api/register/"),
        "login_token": request.build_absolute_uri("/api/token/"),
        "refresh_token": request.build_absolute_uri("/api/token/refresh/"),
        "current_user": request.build_absolute_uri("/api/me/"),
        "tickets": request.build_absolute_uri("/api/tickets/"),
        "dashboard": request.build_absolute_uri("/api/dashboard/"),
        "admin_tickets_api": request.build_absolute_uri("/api/admin/tickets/"),
        "password_reset": request.build_absolute_uri("/api/password-reset/"),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):

    return Response({"status": "ok", "service": "TechNova Resolve"})


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
# ACCOUNT RECOVERY API
# ==============================
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    email = request.data.get("email", "").strip()
    new_password = request.data.get("new_password", "")

    if not email or not new_password:
        return Response(
            {"error": "Registered Gmail and new password required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters."},
            status=status.HTTP_400_BAD_REQUEST
        )

    users = User.objects.filter(email__iexact=email)

    if users.count() != 1:
        return Response(
            {"error": "No account found with this registered Gmail."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = users.first()
    user.set_password(new_password)
    user.save()

    return Response({
        "message": "Password reset successfully. You may now log in with your new password."
    })


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


def forgot_password_page(request):
    return render(request, "forgot_password.html")


def dashboard_page(request):
    return render(request, "dashboard.html", {"active_nav": "dashboard"})


def create_ticket_page(request):
    return render(request, "create_ticket.html", {"active_nav": "create"})


def tickets_page(request):
    return render(request, "tickets.html", {"active_nav": "tickets"})
