
from curses import A_LEFT
from rest_framework import generics
from io import BytesIO
from .models import Article, BonDeCommande, Chapitre, Item, Produit
from .serializers import BonDeCommandeSerializer, ChapitreSerializer, ProduitSerializer, articleSerializer,ItemSerializer

from rest_framework.response import Response
from rest_framework import viewsets, status,views
from reportlab.lib.pagesizes import letter,A4
from django.http import FileResponse
from reportlab.lib import colors 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from num2words import num2words

class ListCreateChapitre(generics.ListCreateAPIView):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer
class RetrieveUpdateDeleteChapitre(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer

class ListCreatearticle(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = articleSerializer

class RetrieveUpdateDeletearticle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = articleSerializer

    def perform_destroy(self, instance):
        # Delete associated products if any
        produits = instance.produits.all()
        for produit in produits:
            if not produit.articles.exists():
                produit.delete()
        # Call the superclass' perform_destroy to delete the article
        super().perform_destroy(instance)

class ListCreateProduit(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantite_en_security = serializer.validated_data.get('quantite_en_security')
        quantite_en_stock = serializer.validated_data.get('quantite_en_stock')
        print(quantite_en_security)
        
        if quantite_en_security > quantite_en_stock:       
            return Response({"error": "Quantity in security cannot be greater than quantity in stock."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RetrieveUpdateDeleteProduit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    
class BonDeCommandeCreateView(generics.ListCreateAPIView):
    queryset = BonDeCommande.objects.all()
    serializer_class = BonDeCommandeSerializer
    
class BonDeCommandeRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommande.objects.all()
    serializer_class = BonDeCommandeSerializer


class ArticleProduitsAPIView(generics.ListAPIView):
    serializer_class = ProduitSerializer

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Produit.objects.filter(article_id=article_id)
    

class ChapitreArticlesAPIView(generics.ListAPIView):
    serializer_class = articleSerializer

    def get_queryset(self):
        chapitre_id = self.kwargs['chapitre_id']
        return Article.objects.filter(chapitre_id=chapitre_id)
    

class ChapitreProduitsAPIView(generics.ListAPIView):
    serializer_class = ProduitSerializer

    def get_queryset(self):
        chapitre_id = self.kwargs['chapitre_id']
        return Produit.objects.filter(article__chapitre_id=chapitre_id)

class ItemViewSet(viewsets.ViewSet):
    def create(self, request, bon_de_commande_id):
        bon_de_commande = BonDeCommande.objects.get(pk=bon_de_commande_id)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            bon_de_commande.items.add(item)
            
            # Recalculate montant_global
            bon_de_commande.montant_global = sum(item.montant for item in bon_de_commande.items.all())
            bon_de_commande.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      

class GeneratePDFView(views.APIView):
     def get(self, request, bon_de_commande_id, *args, **kwargs):

        try:
            bon_de_commande = BonDeCommande.objects.get(id=bon_de_commande_id)
        except BonDeCommande.DoesNotExist:
            return Response({'message': 'Bon de commande not found'}, status=404)

        fournisseur = bon_de_commande.fournisseur
        raison_sociale = fournisseur.raison_sociale
        adresse = fournisseur.adresse
        telephone = fournisseur.telephone
        fax = fournisseur.fax
        num_registre_commerce = fournisseur.num_registre_commerce
        rib_ou_rip = fournisseur.rib_ou_rip
        nif = fournisseur.nif
        nis = fournisseur.nis

        items = bon_de_commande.items.all()

        # Create a PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        bold_body_text_style = styles['BodyText']
        bold_body_text_style.fontName = 'Helvetica-Bold'
        bold_body_text_style.fontSize = 10  # Increased font size

        title_text = f"<b>Bon de Commande N° {bon_de_commande.id} / Date : {bon_de_commande.date}</b>"
        ttite1_text = f"<b>MINISTERE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHERCHE SCIENTIFIQUE</b>"
        title_style = ParagraphStyle(name='Title', fontSize=10, leading=20, alignment=1)  # Define paragraph style
        title = Paragraph(title_text, style=title_style)
        title1 = Paragraph(ttite1_text, style=title_style)
        elements.append(title1)
        elements.append(title)


        elements.append(Paragraph("Identification du prestataire : ", bold_body_text_style))
        elements.append(Paragraph("", bold_body_text_style))
        # Add supplier information
        data = [
            ["Raison sociale:", raison_sociale],
            ["Adresse:", adresse],
            ["Téléphone:", telephone],
            ["Fax:", fax],
            ["N° Registre Commerce:", num_registre_commerce],
            ["RIB (ou RIP):", rib_ou_rip],
            ["N° Identification Fiscale (NIF):", nif],
            ["Numéro d'identification statistique (NIS):", nis]
        ]

        # Create the table and add it to elements
        company_table = Table(data , colWidths=[200, 200])

        # Apply style to the table
        company_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1),2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))

        # Add company_table to the document
        elements.append(company_table)

        # Add line break between supplier information and item table
        elements.append(Paragraph("Identification du service contractant : ", bold_body_text_style))
        elements.append(Paragraph(" ", bold_body_text_style))

        client_data = [
            ['',"Dénomination:ECOLE SUPERIEURE EN INFORMATIQUE SBA "],
            ['',"Code Gestionnaire (ordonnateur):268.543"],
            ['',"Adresse:01 Rue guerrouche mohamed sidi bel abbes" ],
            ['',"Téléphone et Fax:(048) 74- 94 -52 "],
        ]
        client_table = Table(client_data, colWidths=[200, 200])
        client_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(client_table)

        # Add item information
        elements.append(Paragraph("Caractéristiques de la commande :", bold_body_text_style))
        elements.append(Paragraph(f"<b>Chapitre :</b> {bon_de_commande.items.first().chapitre} ", title_style))
        elements.append(Paragraph(f"<strong>Article :</strong> {bon_de_commande.items.first().article} ", title_style))
        elements.append(Paragraph(" ", bold_body_text_style))
        item_data = [["id","Designation", "Prix Unitaire", "Quantite", "Montant"]]
        for item in items:
            item_data.append([str(item.produit.id), item.produit.designation, str(item.prix_unitaire), str(item.quantite), str(item.montant)])
        # Define styles
        s = getSampleStyleSheet()["BodyText"]
        s.textColor = 'black'
        s.wordWrap = 'CJK'
        s.fontSize = 9

        s2 = getSampleStyleSheet()["BodyText"]
        s2.fontName = 'Helvetica-Bold'
        s2.wordWrap='CJK'
        s.fontSize = 9

        print(item_data)

        # Create data with styles
        data2 = [
            [Paragraph(cell, s2) if row_index == 0 else Paragraph(cell, s) for cell in row]
            for row_index, row in enumerate(item_data)
        ]
       
        items_table = Table(data2,colWidths=[30,250,80,60,60])
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0DC1DC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), 'WORDWRAP'),  # Adjust right padding
        ]))


        elements.append(items_table)

        # Calculate the TOTAL TTC
        montant_global = bon_de_commande.montant_global
        tva = bon_de_commande.tva
        total_ttc = montant_global + (montant_global * tva / 100)

        # Add total information
        right_aligned_style = ParagraphStyle(
            'LeftAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=2
        )
        
        # Add total information aligned to the right
        elements.append(Paragraph(f"TOTAL HT: {montant_global}", right_aligned_style))
        elements.append(Paragraph(f"TVA: {int(tva)} %", right_aligned_style))
        elements.append(Paragraph(f"TOTAL TTC: {total_ttc}", right_aligned_style))
        elements.append(Paragraph("", bold_body_text_style))

        total_ttc_text = num2words(total_ttc, lang='fr')

        elements.append(Paragraph("Arrêté le présent bon de commande à la somme de (en lettres): ", bold_body_text_style))
        elements.append(Paragraph("", bold_body_text_style))

        custom_style = ParagraphStyle(
        name='CustomStyle',
        fontSize=10
        )
        elements.append(Paragraph( total_ttc_text, custom_style ))

        elements.append(Paragraph("LE DIRECTEUR", right_aligned_style))

        # Build the PDF document
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'bondecommande_{bon_de_commande_id}.pdf')
    
