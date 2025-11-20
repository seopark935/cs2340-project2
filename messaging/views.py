from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message
from .forms import MessageForm


# Create your views here.

User = get_user_model()

@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    )
    conversations = set()
    for message in messages:
        if message.sender == request.user:
            conversations.add(message.recipient)
        else:
            conversations.add(message.sender)
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient = request.user))
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            return redirect('conversation', username=username)
    else:
        form = MessageForm()

    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form
    })
