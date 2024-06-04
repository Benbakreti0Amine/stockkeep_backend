# your_app_name/management/commands/populate_products.py

from django.core.management.base import BaseCommand
from Service_Achat.models import Article, Produit

class Command(BaseCommand):
    help = 'Populate the database with products for the article "Acqisition du matériels informatiques"'

    def handle(self, *args, **kwargs):
        # Ensure the target article exists
        article_designation = 'Acqisition du matériels informatiques'
        try:
            acquisition_informatique_article = Article.objects.get(designation=article_designation)
        except Article.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Article "{article_designation}" does not exist. Please create it first.'))
            return

        # Products to add
        products = [
            ('Graveur DVD Externe', 0, 0),
            ('Imprimante KYOCERA multifonction A4', 0, 0),
            ('Imprimante laser canon LBP 6030', 0, 0),
            ('Imprimante matricielle epson LQ 2090', 0, 0),
            ('Onduleur 500 va', 0, 0),
            ('Onduleur 700 va', 0, 0),
            ('pc all in one HP I3', 0, 0),
            ('PC de bureau HP i3 ; 4Go ddram disque dur 1To graveur dvd écran 19"', 0, 0),
            ('PC de bureau HP i5 ; 4Go ddram disque dur 1To graveur dvd écran 19"', 0, 0),
            ('PC de bureau HP i7 ; 4Go ddram disque dur 1To graveur dvd écran 19"', 0, 0),
            ('PC de bureau HP;4Go ddram disque dur 1To graveur dvd écran 19"', 0, 0),
            ('pc dell all in one i3', 0, 0),
            ('Pc portable HP I3', 0, 0),
            ('pc portable I7 17" HP', 0, 0),
            ('Vidéo projecteur acer', 0, 0),
            ('Vidéo projecteur Sony', 0, 0),
            ('Disque Dur Externe Portable de marque 2 terra', 0, 0),
            ('Rallonge multiprise 10 M', 0, 0),
            ('Point d’Accès WIFI/Routeur', 0, 0),
            ('Ram 16 G LAPTOP DELL Inspiron 5559-I7, Available OS Memory: 7892MB RAM', 0, 0),
            ('Ram 16 G:  HP 290 G2 MT Business PC', 0, 0),
            ('Cables (usb-micro_usb) pour les raspberry pi3 et les esp8266 (esp12,...)', 0, 0),
            ('Cables usb- usb_type C pour raspberry pi4', 0, 0),
            ('Micro SD cards (16 ou 32 GB) comme HD pour raspberry Pi', 0, 0),
            ('Power banks 5000 ou 10000 mah', 0, 0),
            ('Ventilateur Climatiseur pour PC', 0, 0),
        ]

        for designation, quantite_en_stock, quantite_en_security in products:
            produit_obj, created = Produit.objects.get_or_create(
                designation=designation,
                quantite_en_stock=quantite_en_stock,
                quantite_en_security=quantite_en_security
            )
            produit_obj.articles.add(acquisition_informatique_article)
            self.stdout.write(self.style.SUCCESS(f'Product "{designation}" added with stock {quantite_en_stock} and security {quantite_en_security}.'))

        self.stdout.write(self.style.SUCCESS('Products added successfully.'))
