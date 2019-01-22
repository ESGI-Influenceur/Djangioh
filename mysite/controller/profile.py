from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from mysite.models import Card,Deck,UserCard
from random import randint
import json
import random

@login_required
def profile(request):
    allCards = UserCard.objects.filter(user_id=request.user.id)
    return render(request, 'mysite/profile/profile.html', {'allCards': allCards})

@login_required
def cards(request):
    allCards = UserCard.objects.filter(user_id=request.user.id)
    return render(request, 'mysite/profile/cards.html', {'allCards': allCards})

@login_required
def decks(request):
    allDecks = Deck.objects.all().filter(user_id=request.user.id)
    return render(request, 'mysite/profile/decks.html', {'allDecks': allDecks})

@login_required
def createDeck(request):
    cardsUser = UserCard.objects.filter(user_id=request.user.id)
    error = ''
    if request.POST:
        title = request.POST.get("title", "")
        cards = request.POST.getlist("cards", "")
        print (cards)
        if len(title) < 1:
            error = 'Ajouter un titre'
            return render(request, 'mysite/profile/add-deck.html', {'cardsUser': cardsUser, 'error': error})
        if len(cards) < 1:
            error = 'Ajouter au moins une carte au deck'
            return render(request, 'mysite/profile/add-deck.html', {'cardsUser': cardsUser, 'error': error})
        newDeck = Deck.objects.create(
            user=request.user,
            title=title
        )
        for card in cards:
            newDeck.cards.add(Card.objects.get(id=card))

        allDecks = Deck.objects.all().filter(user_id=request.user.id)

        return render(request, 'mysite/profile/decks.html', {'allDecks': allDecks})
    else:

        return render(request, 'mysite/profile/add-deck.html', {'cardsUser': cardsUser})


@login_required
def buy(request):
    cardsCounter = Card.objects.all().count()
    cards = []
    if request.user.profile.credit >= 100:
        for i in range(5):
            random_index = randint(0, cardsCounter - 1)
            card = Card.objects.all()[random_index]
            cards.append(card)
            userCard = UserCard(user=request.user, card = card)
            userCard.save()
        request.user.profile.credit -= 100
        request.user.save()
        return render(request, 'mysite/profile/add-card.html', {'cards': cards})
    else:
        return render(request, 'mysite/profile/add-card.html', {'error': "Vous n'avez pas assez de credit"})



@login_required
def deck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    cards = deck.cards.all()

    return render(request, 'mysite/profile/deck.html', {'cards': cards, 'deck': deck})

@login_required
def deleteDeck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)

    deck.delete()

    return redirect('decks')

@login_required
def updateDeck(request, deck_id):
    if request.POST:

        deck = get_object_or_404(Deck, pk=deck_id)
        title = request.POST.get("title", "")
        cards = request.POST.getlist("cards", "")

        obj = Deck.objects.get(pk= deck_id)
        obj.title = title
        obj.cards.set([])
        for card in cards:
            obj.cards.add(Card.objects.get(id=card))
        obj.save()

        allDecks = Deck.objects.all().filter(user_id=request.user.id)

        return redirect('decks')
    else:
        deck = get_object_or_404(Deck, pk=deck_id)

        cards = deck.cards.all()
        allCards = UserCard.objects.filter(user_id=request.user.id)


        return render(request, 'mysite/profile/update-deck.html', {'cards': cards,'deck': deck,'allCards':allCards})