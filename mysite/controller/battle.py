from django.http import HttpResponse
from django.shortcuts import render
from mysite.models import Card,Deck,UserCard
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from random import randint

@login_required
def index(request):
    allDecks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'mysite/battle/index.html', {'allDecks': allDecks})

@login_required
def battle(request,deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    cards = deck.cards.all()
    point = 0
    for card in cards:
        point += card.attaque
    combat = point > 10000
    random = randint(0, 1)
    result = combat & random
    print(combat)
    print(random)
    print(result)
    if result :
        request.user.profile.credit += 100
        request.user.save()
    return render(request, 'mysite/battle/result.html', {'result': result})