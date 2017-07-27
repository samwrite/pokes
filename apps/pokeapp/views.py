# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Poke

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    others = User.objects.exclude(id = request.session['id'])
    context= {
        "user": user,
        "others": others,
        "pokers": Poke.objects.filter(poked = user).order_by('-counter'),
        "count": Poke.objects.filter(poked = user).count()
    }
    return render(request, 'pokeapp/index.html', context)

def logout(request):
    request.session.pop('id')
    return redirect(reverse("loginapp:index"))

def poke(request, user_id):
    poker = User.objects.get(id=request.session['id'])
    poked = User.objects.get(id=user_id)
    Poke.objects.createPoke(poker, poked) 
    poked.pokes = poked.pokes + 1
    poked.save()
    return redirect('/main')