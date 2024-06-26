
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import views, status

from Service_Achat.models import BonDeCommande
from io import BytesIO
from .serializers import BonDeReceptionSerializer
from .models import BonDeReception, BonDeReceptionItem
from rest_framework import generics
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from reportlab.lib import colors 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet


class GenerateReceipt(APIView):
    def post(self, request):
        bon_de_commande_id = request.data.get('bon_de_commande_id', None)
        items_data = request.data.get('items', [])

        if bon_de_commande_id is None:
            return Response({'error': 'Veuillez fournir un identifiant de bon de commande.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bon_de_commande = BonDeCommande.objects.get(id=bon_de_commande_id)
        except BonDeCommande.DoesNotExist:
            return Response({'error': 'Le bon de commande spécifié n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)
        
        bon_de_reception_count = BonDeReception.objects.filter(bon_de_commande=bon_de_commande).count()
        bon_de_reception = BonDeReception.objects.create(bon_de_commande=bon_de_commande)
        
        print(bon_de_reception_count)

        for item_data in items_data:
            nom_produit = item_data.get('nom_produit')
            print(nom_produit)
            quantite_livree = item_data.get('quantite_livree')
            # Trouver l'objet Item correspondant dans le bon de commande
            items = bon_de_commande.items.filter(produit__designation=nom_produit)
            item = items.first()
            print(items)
            if item:
                # Check if it's the first reception for this product
                reception = BonDeReceptionItem.objects.filter(nom_produit=nom_produit)
                print(reception)
                first_reception = bon_de_reception_count == 0

                if first_reception:
                    quantite_commandee = item.quantite # No previous orders
                else:
                    # Retrieve the most recent BonDeReceptionItem and get its reste_a_livrer value
                    last_reception_item = reception.order_by('-id').first()
                    quantite_commandee = last_reception_item.reste_a_livrer

                BonDeReceptionItem.objects.create(bon_de_reception=bon_de_reception, nom_produit=nom_produit, quantite_commandee=quantite_commandee, quantite_livree=quantite_livree)

        serializer = BonDeReceptionSerializer(bon_de_reception)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class BonDeReceptionListView(generics.ListAPIView):
    queryset = BonDeReception.objects.all()
    serializer_class = BonDeReceptionSerializer
    
class BonDeReceptionRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeReception.objects.all()
    serializer_class = BonDeReceptionSerializer

      

class GeneratePDFView(views.APIView):
     def get(self, request, bon_de_reception_id, *args, **kwargs):

        try:
            bon_de_reception = BonDeReception.objects.get(id=bon_de_reception_id)
        except BonDeReception.DoesNotExist:
            return Response({'message': 'Bon de reception not found'}, status=404)



        items = bon_de_reception.items.all()

        # Create a PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        bold_body_text_style = styles['BodyText']
        bold_body_text_style.fontName = 'Helvetica-Bold'
        bold_body_text_style.fontSize = 10  # Increased font size

        title_text = f"<b>Bon de reception N° {bon_de_reception.id} / Date : {bon_de_reception.date}</b>"
        ttite1_text = f"<b>MINISTERE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHERCHE SCIENTIFIQUE</b>"
        title_style = ParagraphStyle(name='Title', fontSize=10, leading=20, alignment=1)  # Define paragraph style
        title = Paragraph(title_text, style=title_style)
        title1 = Paragraph(ttite1_text, style=title_style)
        elements.append(title1)
        elements.append(title)

        elements.append(Paragraph("", bold_body_text_style))

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
        elements.append(Paragraph("Caractéristiques de la commande interne :", bold_body_text_style))
        elements.append(Paragraph("", bold_body_text_style))
        elements.append(Paragraph(f"<b>information sur la commande :</b> {bon_de_reception.bon_de_commande} ", title_style))
        # elements.append(Paragraph(f"<strong>Article :</strong> {bon_de_reception.items.first().article} ", title_style))
        elements.append(Paragraph(" ", bold_body_text_style))
        item_data = [["N°","Designation", "quantite livrée", "reste à livrer", ]]
        for index, item in enumerate(items):
            item_data.append([str(index+1), item.nom_produit, str(item.quantite_livree), str(item.reste_a_livrer)])
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
       
        items_table = Table(data2,colWidths=[30,250,100,100])
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


        # Add total information
        right_aligned_style = ParagraphStyle(
            'LeftAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=2
        )
        
        # Add total information aligned to the right



        elements.append(Paragraph("LE DIRECTEUR", right_aligned_style))

        # Build the PDF document
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'bondereception_{bon_de_reception_id}.pdf')
    
