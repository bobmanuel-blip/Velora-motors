from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from vehicles.models import Vehicle
from .ai_assistant import answer_faq, generate_quick_replies
from .models import Conversation, Message


@login_required
def inbox(request):
    conversations = (
        Conversation.objects.filter(buyer=request.user) | Conversation.objects.filter(dealer=request.user)
    ).distinct().select_related("buyer", "dealer", "vehicle")
    return render(request, "chatapp/inbox.html", {"conversations": conversations})


@login_required
def start_conversation(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    if request.user == vehicle.dealer:
        return redirect("vehicles:vehicle_detail", pk=vehicle_pk)

    conversation, created = Conversation.objects.get_or_create(
        buyer=request.user, dealer=vehicle.dealer, vehicle=vehicle
    )
    if created:
        Message.objects.create(
            conversation=conversation,
            sender=vehicle.dealer,
            content=(
                f"Hi! Thanks for your interest in the {vehicle.year} {vehicle.make} "
                f"{vehicle.model}. I'm happy to answer any questions — feel free to "
                f"ask about pricing, condition, financing, or shipping."
            ),
            is_ai_suggestion=True,
        )
    return redirect("chatapp:conversation_detail", pk=conversation.pk)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.filter(buyer=request.user) | Conversation.objects.filter(dealer=request.user),
        pk=pk,
    )

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        attachment = request.FILES.get("attachment")
        if content or attachment:
            Message.objects.create(
                conversation=conversation, sender=request.user, content=content, attachment=attachment
            )
            conversation.save()  # bump updated_at

            # If the buyer asks a common question and the dealer hasn't
            # replied yet, the AI assistant can jump in with an instant
            # answer, then the dealer can continue the conversation.
            if request.user == conversation.buyer:
                faq_answer = answer_faq(content)
                if faq_answer:
                    Message.objects.create(
                        conversation=conversation,
                        sender=conversation.dealer,
                        content=faq_answer,
                        is_ai_suggestion=True,
                    )
        return redirect("chatapp:conversation_detail", pk=pk)

    conversation.messages.exclude(sender=request.user).update(is_read=True)
    quick_replies = generate_quick_replies(conversation.vehicle)

    return render(request, "chatapp/conversation.html", {
        "conversation": conversation,
        "other": conversation.other_participant(request.user),
        "quick_replies": quick_replies,
    })


@login_required
def poll_messages(request, pk):
    """Simple AJAX polling endpoint. Swap for a WebSocket consumer
    (Django Channels) later for true real-time push delivery."""
    conversation = get_object_or_404(
        Conversation.objects.filter(buyer=request.user) | Conversation.objects.filter(dealer=request.user),
        pk=pk,
    )
    since_id = int(request.GET.get("since", 0))
    messages = conversation.messages.filter(id__gt=since_id)
    data = [
        {
            "id": m.id,
            "sender": m.sender.username,
            "is_me": m.sender_id == request.user.id,
            "content": m.content,
            "created_at": timezone.localtime(m.created_at).strftime("%I:%M %p"),
            "is_ai": m.is_ai_suggestion,
        }
        for m in messages
    ]
    return JsonResponse({"messages": data})
