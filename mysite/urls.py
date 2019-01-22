"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .controller import landing,registration,profile,forum,battle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', registration.signup, name='signup'),
    path('accounts', profile.profile, name='profile'),
    path('accounts/cards', profile.cards, name='cards'),
    path('accounts/decks', profile.decks, name='decks'),
    path('accounts/decks/add', profile.createDeck, name='addDecks'),
    path('accounts/decks/<int:deck_id>', profile.deck, name='deck'),
    path('accounts/decks/<int:deck_id>/delete', profile.deleteDeck, name='deleteDeck'),
    path('accounts/decks/<int:deck_id>/update', profile.updateDeck, name='updateDeck'),
    path('accounts/buy', profile.buy, name='buy'),

    path('battle/', battle.index, name='battle'),
    path('battle/<int:deck_id>', battle.battle, name='start'),

    path('forum/', forum.forum, name='forum-detail'),
    url(r'^topic/(\d+)/$', forum.topic, name='topic-detail'),
    url(r'^reply/(\d+)/$', forum.post_reply, name='reply'),
    url(r'newtopic/(\d+)/$', forum.new_topic, name='new-topic'),
    path('', landing.index, name='home'),
]
