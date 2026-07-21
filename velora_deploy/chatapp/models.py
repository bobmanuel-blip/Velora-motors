from django.conf import settings
from django.db import models

from vehicles.models import Vehicle


class Conversation(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_buyer"
    )
    dealer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_dealer"
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("buyer", "dealer", "vehicle")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.buyer} <-> {self.dealer} ({self.vehicle or 'general'})"

    def other_participant(self, user):
        return self.dealer if user == self.buyer else self.buyer

    def unread_count_for(self, user):
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="chat_attachments/", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_ai_suggestion = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.content[:40]}"
