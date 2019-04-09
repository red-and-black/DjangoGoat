from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import (
    WriteNoteForm,
    ReplyForm
)
from .models import Note


@login_required
def dash(request):
    all_notes = Note.objects.\
        filter(Q(sender=request.user) | Q(receiver=request.user))

    friends_pks = set()
    for sender, receiver in all_notes.values_list('sender', 'receiver'):
        friends_pks.add(sender)
        friends_pks.add(receiver)

    latest_notes = []
    for friend_pk in friends_pks:
        if friend_pk == request.user.pk:
            conversation = all_notes.\
                filter(sender=request.user).\
                filter(receiver=request.user)
        else:
            conversation = all_notes.\
                filter(Q(receiver__pk=friend_pk) | Q(sender__pk=friend_pk))
        if conversation:
            latest_note = conversation.last()
            latest_notes.append(latest_note)

    return render(request, 'dash.html', {'latest_notes': latest_notes})


@login_required
def write_note(request):
    user = request.user
    if request.method == 'POST':
        form = WriteNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.sender = user
            note.save()
            return redirect('dash')
    else:
        form = WriteNoteForm()
    return render(request, 'write_note.html', {'form': form})


@login_required
def note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'note.html', {'note': note})


@login_required
def conversation(request, friend_pk):
    friend = get_object_or_404(User, pk=friend_pk)
    friend_name = friend.username
    all_notes = Note.objects.\
        filter(Q(sender=request.user) | Q(receiver=request.user))
    if friend == request.user:
        conversation = all_notes.\
            filter(sender=request.user).\
            filter(receiver=request.user)
    else:
        conversation = all_notes.\
            filter(Q(receiver__pk=friend_pk) | Q(sender__pk=friend_pk))

    user = request.user
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.sender = user
            note.receiver = friend
            note.save()
            return redirect('conversation', friend_pk=friend_pk)
    else:
        form = WriteNoteForm()

    return render(request, 'conversation.html', {
        'conversation': conversation,
        'form': form,
        'friend_name': friend_name,
    })
