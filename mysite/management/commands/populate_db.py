"""
Import json data from URL to Datababse
"""
import requests,json,os,base64
from django.core.management.base import BaseCommand
from django.conf import settings
from mysite.models import Card

IMPORT_URL = 'http://www.ygo-api.com/api/Cards/'
YUGI_URL = os.path.join(settings.BASE_DIR, 'mysite/static/json/yugi.json')
JOEY_URL = os.path.join(settings.BASE_DIR, 'mysite/static/json/joey.json')
KAIBA_URL = os.path.join(settings.BASE_DIR, 'mysite/static/json/kaiba.json')
DECKS = [YUGI_URL,JOEY_URL,KAIBA_URL]

class Command(BaseCommand):

    def handle(self, *args, **options):

        for deck in DECKS:
            cards = json.load(open(deck))
            print(cards)
            for card in cards:
                headers = {'Content-Type': 'application/json'}
                response = requests.get(
                    url=IMPORT_URL+card,
                    headers=headers,
                )
                if response.status_code != 404:
                    data = response.json()
                    if data['atk'] != None:
                        card = Card.objects.filter(name = data["name"])
                        if card.count() == 0:
                            Card.objects.create(name = data["name"],
                                                image = (str(data["cardNumber"]) if data["cardNumber"] else str(0)) +".jpg",
                                                description = data["description"],
                                                cardLevel = data["cardLevel"],
                                                attaque = data["atk"],
                                                defense = data["def"],
                                                numero = data["cardNumber"] if data["cardNumber"] else 0)
                        else:
                            print("card already exist")
