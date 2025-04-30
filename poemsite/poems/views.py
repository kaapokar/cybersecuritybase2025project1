from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Poem
from .forms import PoemForm
from django.db import connection
import logging
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

# FLAW 4 A09:2021 – Security Logging and Monitoring Failures: 
#logger = logging.getLogger('django.security')  

#@receiver(user_login_failed)
#def log_login_failed(sender, credentials, request, **kwargs):
#    username = credentials.get('username', 'UNKNOWN')
#    ip = request.META.get('REMOTE_ADDR', 'unknown')
#    logger.warning(f"FAILED login for '{username}' from IP {ip}")

@login_required
def home(request):
    poems = Poem.objects.all().order_by('-created_at')
    return render(request, 'poems/home.html', {'poems': poems})

@login_required
def add_poem(request):
    if request.method == 'POST':
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save(commit=False)
            poem.author = request.user
            poem.save()
            return redirect('/')
    else:
        form = PoemForm()
    return render(request, 'poems/add_poem.html', {'form': form})

# FLAW 1: A01:2021 – Broken Access Control
@login_required
def delete_poem(request, poem_id):
    poem = get_object_or_404(Poem, id=poem_id)

# These line of code should be added so only the poem author can delete the poem
   # if poem.author != request.user:
    #    return HttpResponseForbidden("You are not allowed to delete this poem.")

    if request.method == 'POST':
        poem.delete()
        return redirect('/')
    return render(request, 'poems/confirm_delete.html', {'poem': poem})

@login_required
def poem_detail(request, poem_id):
    poem = get_object_or_404(Poem, id=poem_id)
    return render(request, 'poems/poem_detail.html', {'poem': poem})

@login_required
def unsafe_search(request):
    title = request.GET.get('q', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM poems_poem WHERE title = '{title}'")
        results = cursor.fetchall()
    return HttpResponse(str(results))
