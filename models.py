from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):

    # ================= STATUS =================
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    # ================= PRIORITY =================
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    # ================= USER INFO =================
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    # ================= TICKET DATA =================
    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    # ⭐⭐⭐ ADMIN RESPONSE (MOST IMPORTANT PART)
    admin_response = models.TextField(
        blank=True,
        null=True,
        help_text="Admin solution visible to user"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ================= DISPLAY =================
    def __str__(self):
        return f"{self.title} - {self.user.username}"