from django.shortcuts import get_object_or_404
from io import BytesIO
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import views, status,generics

from Service_Achat.models import BonDeCommande,Produit
from .serializers import BonDeReceptionSerializer
from .models import BonDeReception, BonDeReceptionItem
from consommateur.models import BonDeCommandeInterne, BonDeCommandeInterneItem
from .serializers import BonDeReceptionSerializer, BonDeSortieItemSerializer, BonDeSortieSerializer
from .serializers import BonDeCommandeInterneMagaSerializer, EtatInventaireSerializer,FicheMovementSerializer,AdditionalInfoSerializer
from .models import BonDeReception, BonDeReceptionItem,BonDeSortie,EtatInventaire, BonDeSortieItem,FicheMovement
from reportlab.lib.pagesizes import A4
from django.http import FileResponse

from reportlab.lib import colors 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import inch


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
            # print(nom_produit)
            quantite_livree = item_data.get('quantite_livree')
            # Trouver l'objet Item correspondant dans le bon de commande
            items = bon_de_commande.items.filter(produit__designation=nom_produit)
            item = items.first()
            # print(items)
            if item:
                # Check if it's the first reception for this product
                reception = BonDeReceptionItem.objects.filter(nom_produit=nom_produit)
                # print(reception)
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
    
    ############################################
    ############################################



class BonDeSortieCreateView(APIView):
    def post(self, request, *args, **kwargs):
        bon_de_commande_interne_id = request.data.get('bon_de_commande_interne')
        items_data = request.data.get('items', [])

        bon_de_commande_interne = get_object_or_404(BonDeCommandeInterne, pk=bon_de_commande_interne_id)


        bon_de_sortie_data = {
            'bon_de_commande_interne': bon_de_commande_interne_id,
            'items': []
        }

        for item_data in items_data:
            bon_de_commande_interne_item_id = item_data.get('bon_de_commande_interne_item')
            quantite_accorde = item_data.get('quantite_accorde')
            observation_item = item_data.get('observation')

            # Retrieve the BonDeCommandeInterneItem instance
            print(f" id bon de com inter",bon_de_commande_interne_item_id)
            bon_de_commande_interne_item = get_object_or_404(BonDeCommandeInterneItem, pk=bon_de_commande_interne_item_id)
            print('etape1')
 
            # Create the item data for BonDeSortie
            item_serializer = BonDeSortieItemSerializer(data={
                'bon_de_commande_interne_item': bon_de_commande_interne_item_id,
                'quantite_accorde': quantite_accorde,
                'observation': observation_item
            })
            print(item_serializer.is_valid())
            print('etape2')
            print(f" id bon de com inter item",bon_de_commande_interne_item_id)
            print(quantite_accorde)
            print(item_serializer.validated_data)


            if item_serializer.is_valid():
                bon_de_sortie_data['items'].append({
                        'bon_de_commande_interne_item': bon_de_commande_interne_item_id,
                        'quantite_accorde': quantite_accorde,
                        'observation': observation_item})
                print('etape3')
                print(item_serializer.validated_data)
            else:
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print('etape4')
        serializer = BonDeSortieSerializer(data=bon_de_sortie_data)

        print(bon_de_sortie_data)
        print('etape5')

        print(serializer.is_valid())
        print('etape6')
        print(serializer.validated_data)


        if serializer.is_valid():      
            bon_de_sortie = serializer.save()  # Save here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BonDeSortieListView(generics.ListAPIView):
    queryset = BonDeSortie.objects.all()
    serializer_class = BonDeSortieSerializer

class BonDeCommandeInterneListCreateView(generics.ListCreateAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneMagaSerializer

class GenerateBonDeSortiePDFView(views.APIView):
     def get(self, request, bon_de_sortie_id, *args, **kwargs):

        try:
            bon_de_sortie = BonDeSortie.objects.get(id=bon_de_sortie_id)
        except BonDeSortie.DoesNotExist:
            return Response({'message': 'Bon de reception not found'}, status=404)

        Consommateur_id = bon_de_sortie.bon_de_commande_interne.Consommateur_id
        username = Consommateur_id.username
        email = Consommateur_id.email

        items = bon_de_sortie.items.all()

        # Create a PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        bold_body_text_style = styles['BodyText']
        bold_body_text_style.fontName = 'Helvetica-Bold'
        bold_body_text_style.fontSize = 10  # Increased font size

        title_text = f"<b>Bon de sortie N° {bon_de_sortie.id} / Date : {bon_de_sortie.date}</b>"
        title2_text = f"<b>Type : {bon_de_sortie.type}</b>"
        ttite1_text = f"<b>MINISTERE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHERCHE SCIENTIFIQUE</b>"
        title_style = ParagraphStyle(name='Title', fontSize=10, leading=20, alignment=1)  # Define paragraph style
        title = Paragraph(title_text, style=title_style)
        title1 = Paragraph(ttite1_text, style=title_style)
        title2 = Paragraph(title2_text, style=title_style)
        elements.append(title1)
        elements.append(title)
        elements.append(title2)

        elements.append(Paragraph("", bold_body_text_style))

        # Add line break between supplier information and item table
        elements.append(Paragraph("Identification du cosommateur : ", bold_body_text_style))
        elements.append(Paragraph(" ", bold_body_text_style))

        client_data = [
            ["Nom De Demandeur : ", username],
            ["Email : ", email],
        ]
        client_table = Table(client_data, colWidths=[200, 200])
        client_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(client_table)

        # Add item information
        elements.append(Paragraph("Caractéristiques de la bon de sortie :", bold_body_text_style))
        elements.append(Paragraph("", bold_body_text_style))
        elements.append(Paragraph(f"<b>information sur la commande interne : N° </b> {bon_de_sortie.bon_de_commande_interne.id} ", title_style))
        elements.append(Paragraph(" ", bold_body_text_style))
        item_data = [["N°","Designation", "Quantite Accordé", "Observation", ]]
        for index, item in enumerate(items):
            item_produit = item.bon_de_commande_interne_item.produit.designation
            item_data.append([str(index+1), item_produit, str(item.quantite_accorde), item.observation])
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
       
        items_table = Table(data2,colWidths=[30,250,70,150])
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
            'RightAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=2
        )
        Middle_aligned_style = ParagraphStyle(
            'MiddleAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=1
        )
        LEFT_aligned_style = ParagraphStyle(
            'LeftAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=0
        )

        # Create paragraphs
        paragraphs = [
            Paragraph("LE MAGASINIER", right_aligned_style),
            Paragraph("LE DIRECTEUR", Middle_aligned_style),
            Paragraph("LE DEMANDEUR", LEFT_aligned_style)
        ]

        # Create a table with a single row and three columns
        data = [paragraphs]
        table = Table(data, colWidths=[4*inch, 4*inch, 4*inch])

        # Add the table to elements
        elements.append(table)


        # Build the PDF document
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'bondereception_{bon_de_sortie_id}.pdf')


class EtatInventaireListCreateAPIView(generics.ListCreateAPIView):
    queryset = EtatInventaire.objects.all()
    serializer_class = EtatInventaireSerializer

class EtatInventaireRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EtatInventaire.objects.all()
    serializer_class = EtatInventaireSerializer
        
class GenerateFichMouv(APIView):
    def get(self, request):
        fiches = FicheMovement.objects.all()
        serializer = FicheMovementSerializer(fiches, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'produit_id' not in request.data:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        produit_id = request.data['produit_id']

        try:
            product = Produit.objects.get(id=produit_id)

            receptions = BonDeReception.objects.filter(items__nom_produit=product.designation)
            suppliers_dates = [{'fournisseur': reception.bon_de_commande.fournisseur, 'date_entree': reception.date} for reception in receptions]

            total_quantity_received = receptions.aggregate(total=Sum('items__quantite_livree'))['total'] or 0

            sorties = BonDeSortieItem.objects.filter(bon_de_commande_interne_item__produit=product)

            remaining_quantity = total_quantity_received - sum(sortie.quantite_accorde for sortie in sorties)

            additional_info_data = []
            for sortie in sorties:
                bon_de_sortie = sortie.bon_de_sortie
                additional_info_data.append({
                    'numero_bon': str(sortie.bon_de_sortie.id),
                    'quantite_sortie': sortie.quantite_accorde,
                    'observations': sortie.observation,
                    'consommateur':str(bon_de_sortie.bon_de_commande_interne.Consommateur_id),
                    'date_sortie':bon_de_sortie.date
                })

            additional_info_serializer = AdditionalInfoSerializer(data=additional_info_data, many=True)
            additional_info_serializer.is_valid(raise_exception=True)
            additional_info_serializer.save()
            fiche_de_mouvement_data = {
                'produit_id': produit_id,
                'date_entree': suppliers_dates[0]['date_entree'] if suppliers_dates else None,
                'fournisseur': str(suppliers_dates[0]['fournisseur']),
                'quantite_entree': total_quantity_received,
                'sum_quantite_sortie': sum(sortie.quantite_accorde for sortie in sorties),
                'reste': remaining_quantity,
                'additional_info':additional_info_serializer.data
            }

            fiche_de_mouvement_serializer = FicheMovementSerializer(data=fiche_de_mouvement_data)
            fiche_de_mouvement_serializer.is_valid(raise_exception=True)
            fiche_de_mouvement_instance = fiche_de_mouvement_serializer.save()


            response_data = {
                'id': fiche_de_mouvement_instance.id,
                **fiche_de_mouvement_data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Produit.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
class GenerateFicheDeMouvementPDFView(views.APIView):
     def get(self, request, fiche_de_mouvement_id, *args, **kwargs):

        try:
            fiche_de_mouvement = FicheMovement.objects.get(id=fiche_de_mouvement_id)
        except BonDeSortie.DoesNotExist:
            return Response({'message': 'Bon de reception not found'}, status=404)
        
        produit = Produit.objects.get(id=fiche_de_mouvement.produit_id)

        date_entree = fiche_de_mouvement.date_entree
        fournisseur = fiche_de_mouvement.fournisseur
        quantite_entree = fiche_de_mouvement.quantite_entree

        items = fiche_de_mouvement.additional_info.all()
        print(items)

        # Create a PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        bold_body_text_style = styles['BodyText']
        bold_body_text_style.fontName = 'Helvetica-Bold'
        bold_body_text_style.fontSize = 10  # Increased font size

        title_text = f"<b>Fiche de mouvement N° {fiche_de_mouvement.id}</b>"
        title2_text = f"<b>Produit : {produit.designation}</b>"
        ttite1_text = f"<b>MINISTERE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHERCHE SCIENTIFIQUE</b>"
        title_style = ParagraphStyle(name='Title', fontSize=10, leading=20, alignment=1)  # Define paragraph style
        title = Paragraph(title_text, style=title_style)
        title1 = Paragraph(ttite1_text, style=title_style)
        title2 = Paragraph(title2_text, style=title_style)
        elements.append(title1)
        elements.append(title)
        elements.append(title2)

        elements.append(Paragraph("", bold_body_text_style))

        # Add line break between supplier information and item table
        elements.append(Paragraph("Identification du Fiche : ", bold_body_text_style))
        elements.append(Paragraph(" ", bold_body_text_style))

        client_data = [
            ["Date d'éntree : ", date_entree],
            ["Fournissuer : ", fournisseur],
            ["Quantity Entree : ", quantite_entree],
        ]
        client_table = Table(client_data, colWidths=[200, 200])
        client_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(client_table)

        # Add item information
        elements.append(Paragraph("Caractéristiques de la fiche de mouvement :", bold_body_text_style))
        elements.append(Paragraph("", bold_body_text_style))
        #elements.append(Paragraph(f"<b>information sur la bon de sortie : N° </b> {bon_de_sortie.bon_de_commande_interne.id} ", title_style))
        elements.append(Paragraph(" ", bold_body_text_style))
        item_data = [["N° de bon ","Benefit", "Date de Sortie","Qauntity Sortie", "Observation" ]]
        for item in (items):
            item_data.append([item.numero_bon, item.consommateur, str(item.date_sortie), str(item.quantite_sortie), item.observations])
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
       
        items_table = Table(data2,colWidths=[70,100,70,70,200])
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
            'RightAligned',
            fontSize=10,
            parent=bold_body_text_style,
            alignment=2
        )
        elements.append(Paragraph(f"Quantite de sortie globale : {fiche_de_mouvement.sum_quantite_sortie}", right_aligned_style))
        elements.append(Paragraph("", bold_body_text_style))
        elements.append(Paragraph(f"Quantite rest: {fiche_de_mouvement.reste}", right_aligned_style))
        elements.append(Paragraph("", bold_body_text_style))
        # Create paragraphs
        paragraphs = [
            Paragraph("LE MAGASINIE", right_aligned_style),
        ]

        # Create a table with a single row and three columns
        data = [paragraphs]
        table = Table(data, colWidths=[4*inch, 4*inch, 4*inch])

        # Add the table to elements
        elements.append(table)


        # Build the PDF document
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'fiche_de_mouvement{fiche_de_mouvement_id}.pdf')