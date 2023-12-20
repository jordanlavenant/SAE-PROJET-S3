from fpdf import FPDF #pip install fpdf
import datetime

title = "GestLab"

class PDF_BonCommande:
    class PDF(FPDF):
        def header(self):
            #logo
            try:
                self.image('./GestLab/static/images/logo-GestLab.png', 10, 8, 33)
            except:
                self.image('./static/images/logo-GestLab.png', 10, 8, 33)
            #font
            self.set_font('Arial', 'B', 30)
            #padding
            #line break
            self.ln(10)
            #Title
            self.cell(80)
            title_w = self.get_string_width(title) + 6
            doc_w = self.w
            self.set_x((doc_w-title_w)/2)
            self.set_draw_color(0,80,180)
            self.set_fill_color(230,230,0)
            self.set_text_color(220,50,50)
            self.set_line_width(1)
            self.cell(title_w,10, title, ln=1, align="C")
            #line break
            self.ln(20)

        def footer(self):
            #set position of the footer
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)
            self.cell(0,10, 'Page '+ str(self.page_no()) + '/{nb}', align="C")
        

        def afficher_numero_commande(self, numero_commande, date):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, "Bon de commande n°"+numero_commande + " - " + date, ln=1, align="C")
            self.ln(10)

        def cree_par(self, nom, prenom):
            self.set_font('Arial', 'I', 12)
            self.cell(0, 10, "Crée par le gestionnaire: " + nom + " " + prenom, ln=1, align="C")
            self.ln(10)
            
            
        def affiche_materiel(self, liste_materiel):
            self.set_font('Arial', 'B', 10)
            self.cell(38, 10, "Nom", border=True, align="C")
            self.cell(38, 10, "Quantité", border=True, align="C")
            self.cell(38, 10, "Réference", border=True, align="C")
            self.cell(38, 10, "Categorie", border=True, align="C")
            self.cell(38, 10, "Domaine", border=True, align="C")
            self.ln(10)
            print(liste_materiel)
            for materiel in liste_materiel:
                self.set_font('Arial', '', 8)
                self.cell(38, 10, materiel[0], border=True, align="C")
                self.cell(38, 10, str(materiel[4]), border=True, align="C")
                self.cell(38, 10, materiel[1], border=True, align="C")
                self.cell(38, 10, materiel[3], border=True, align="C")
                self.cell(38, 10, materiel[2], border=True, align="C")
                self.ln(10)
        
        def affiche_FDS(self,referenceMateriel, nomMateriel, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif ):
            #image
            try:
                lien = "./GestLab/static/images/"
                lienImageLogo = "./GestLab/static/images/logo-Gestlab.png"
                lienImageToxique = lien + "Pictogramme-chimique-toxique-removebg-preview.png"
                lienImageInflamable = lien + "Pictogramme-chimique-inflammable-removebg-preview.png"
                lienImageCorrosif = lien + "Pictogramme-chimique-corrosif-removebg-preview.png"
                lienImageExplosif = lien + "Pictogramme-chimique-explosion-removebg-preview.png"
                lienImageGazSousPression = lien + "Pictogramme-chimique-gaz-sous-pression-removebg-preview.png"
                lienImageCMR = lien + "Pictogramme-chimique-CMR-removebg-preview.png"
                lienImageChimiqueEnvironement = lien + "Pictogramme-chimique-environnement-removebg-preview.png"
                lienImageDangereux = lien + "Pictogramme-chimique-point-dexclamation-removebg-preview.png"
                lienImageComburant = lien + "Pictogramme-chimique-comburant-removebg-preview.png"
            except:
                lien = "./static/images/FDS/"
                lienImageLogo = "./static/images/logo-Gestlab.png"
                lienImageToxique = lien + "Pictogramme-chimique-toxique-removebg-preview.png"
                lienImageInflamable = lien + "Pictogramme-chimique-inflammable-removebg-preview.png"
                lienImageCorrosif = lien + "Pictogramme-chimique-corrosif-removebg-preview.png"
                lienImageExplosif = lien + "Pictogramme-chimique-explosion-removebg-preview.png"
                lienImageGazSousPression = lien + "Pictogramme-chimique-gaz-sous-pression-removebg-preview.png"
                lienImageCMR = lien + "Pictogramme-chimique-CMR-removebg-preview.png"
                lienImageChimiqueEnvironement = lien + "Pictogramme-chimique-environnement-removebg-preview.png"
                lienImageDangereux = lien + "Pictogramme-chimique-point-dexclamation-removebg-preview.png"
                lienImageComburant = lien + "Pictogramme-chimique-comburant-removebg-preview.png"


            explication_explosif = "Ce pictogramme chimique identifie des produits explosifs instables et très réactifs. Ces derniers peuvent exploser au contact d'une flamme, d'une étincelle, sous l'effet de la chaleur, en cas de frottement ou en cas de choc."
            explication_danger_incendie = "Le symbole de la flamme identifie des produits qui peuvent s'enflammer :\nau contact d'une flamme, d'une étincelle (ex. : benzène, acétone, éthanol, éther)\nau contact avec l'air\nau contact de l'eau en produisant des gaz inflammables qui s'enflamment spontanément ou en présence d'une source d'énergie\nLes produits identifiés par ce symbole sont variés. Ce sont :\nLes liquides inflammables, les matières solides inflammables, les gaz inflammables, les aérosols inflammables.\nLes liquides et solides pyrophoriques,\nCertains peroxydes organiques\nCertains produits autoréactifs\nLes hydroréactifs\nLes auto-échauffants"
            explication_comburant = "Ce pictogramme chimique identifie les produits comburants. Ces derniers peuvent provoquer ou aggraver un incendie en présence d'un combustible.\nIls peuvent provoquer une explosion s'ils sont en contact avec un inflammable.\nExemples : acide perchlorique, acide nitrique concentré, chlore gazeux."
            explication_gaz_sous_pression = "Ce pictogramme chimique identifie les produits sous pression dans un récipient.  En cas de chaleur, ce dernier peut exploser sous l'effet de la chaleur qui génère une expansion du gaz et une montée en pression.\nLes gaz sous pression sont classés en 4 catégories :\nLes gaz comprimés non liquéfiés\nLes gaz liquéfiés réfrigérés responsables de graves brûlures par le froid. Ce sont les fluides cryogéniques. (ex. : azote liquide)\nLes gaz liquéfiés (ex. : chlore, propane)\nLes gaz dissous (ex. : bouteille d'acétylène)"
            explication_corrosion = "Ce pictogramme de danger signale les produits chimiques pouvant :\nAttaquer ou détruire les métaux\nRonger la peau et/ou les yeux en cas de contact ou projection\nLe symbole de corrosion identifie les produits corrosifs pour les yeux, la peau et/ou les métaux.\n\nExemples : acide chlorhydrique, soude (hydroxyde de sodium), acide sulfurique."
            explication_toxicité_aiguë = "Ce pictogramme de danger identifie les produits chimiques toxiques aigus. Ils empoisonnent rapidement, même à faible dose, par inhalation, ingestion et/ou par contact cutané.\nLe symbole de toxicité aiguë identifie des produits chimiques capables de provoquer la mort quelques minutes, heures ou jours après l'exposition.\n\nExemples : méthanol, sulfure d'hydrogène, acide fluorhydrique."
            explication_altération_santé_humaine = "Ce pictogramme de danger identifie un produit chimique :\nnocif (capable d'empoisonner en cas d'exposition à forte dose)\nirritant pour la peau, les yeux ou les voies respiratoires\nqui provoque somnolence ou vertiges (ex. : acétone)\nqui provoque une irritation des voies respiratoires\ncapable de détruire la couche d'ozone en haute atmosphère (ex. : CFC)\n\nsensibilisant cutané (allergisant cutané) (Ex.: eczéma)"
            explication_effets_graves_sur_la_santé = "Ce pictogramme de danger signale au moins une des propriétés suivantes :\ncancérogène (ex.: formaldéhyde).\nmutagène sur les cellules germinales (susceptibles de provoquer des maladies génétiques héréditaires).\nreprotoxique (atteinte des capacités de reproduction telle que la fertilité, le développement de l'enfant à naître).\ntoxique pour certains organes cibles, à la suite d'une exposition unique ou suite à des expositions répétées.\nsensibilisant respiratoire (allergisant respiratoire).\nMortel par aspiration (ie. : mortel par ingestion puis pénétration dans les voies respiratoires)."
            explication_toxicité_aquatique = "Ce pictogramme de danger identifie les produits néfastes pour les organismes aquatiques (crustacés, algues, poissons).\nCe symbole de danger environnemental signale une toxicité à court terme (toxicité aiguë) ou des effets néfastes à long terme (toxicité chronique) sur les organismes aquatiques.\nExemples : eau de javel, isopentane, sodium azide."

            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, "Fiche de données de sécurité", ln=1, align="C")
            self.ln(10)
            self.set_font('Arial', 'B', 12)

            # Calcul de l'espace horizontal nécessaire pour centrer le tableau
            largeur_totale = 38 * 2  # Largeur totale des deux cellules
            espacement = 10  # Espacement entre les cellules
            espace_restant = self.w - largeur_totale - espacement * 2
            x_centre = espace_restant / 2

            # Première ligne du tableau
            self.cell(x_centre)
            self.cell(38, 10, "Référence", border=True, align="C")
            self.cell(38, 10, "Nom", border=True, align="C")
            self.ln(10)

            # Deuxième ligne du tableau
            self.cell(x_centre)
            self.cell(38, 10, referenceMateriel, border=True, align="C")
            self.cell(38, 10, nomMateriel, border=True, align="C")
            self.ln(10)

            # Ajout des pictogrammes
            self.cell(x_centre)

            list_lien_image = []
            list_explication = []

            if estToxique:
                list_lien_image.append(lienImageToxique)
                list_explication.append(explication_toxicité_aiguë)

            if estInflamable:
                list_lien_image.append(lienImageInflamable)
                list_explication.append(explication_danger_incendie)
            
            if estExplosif:
                list_lien_image.append(lienImageExplosif)
                list_explication.append(explication_explosif)
            
            if est_gaz_sous_pression:
                list_lien_image.append(lienImageGazSousPression)
                list_explication.append(explication_gaz_sous_pression)

            if est_CMR:
                list_lien_image.append(lienImageCMR)
                list_explication.append(explication_effets_graves_sur_la_santé)

            if est_chimique_environement:
                list_lien_image.append(lienImageChimiqueEnvironement)
                list_explication.append(explication_toxicité_aquatique)

            if est_dangereux:
                list_lien_image.append(lienImageDangereux)
                list_explication.append(explication_altération_santé_humaine)

            if est_comburant:
                list_lien_image.append(lienImageComburant)
                list_explication.append(explication_comburant)

            if est_corrosif:
                list_lien_image.append(lienImageCorrosif)
                list_explication.append(explication_corrosion)
                

    
            # if estCorrisif:
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)

            x_position = 10  # Commencer à partir de la gauche
            y_position = 130  # Y initial

            for lien_image in list_lien_image:
                if x_position + 33 > self.w:  # Vérifie si l'image sort du cadre
                    x_position = 10  # Revenir à gauche
                    y_position += 40  # Aller à la ligne suivante
                    self.ln(40)  # Sauter une ligne dans le PDF

                self.image(lien_image, x_position, y_position, 33)
                x_position += 40  # Décaler horizontalement pour la prochaine image
            self.ln(70)  # Sauter une ligne dans le PDF

            # Ajout des explications
            self.set_font('Arial', '', 10)
            for explication in list_explication:
                
                self.multi_cell(0, 5, explication)
                self.ln(6)

        def affiche_FDS_picatogramme(self):
        #image
            lien = "./GestLab/static/images/FDS/"
            lienImageLogo = "./GestLab/static/images/logo-Gestlab.png"
            lienImageToxique = lien + "Pictogramme-chimique-toxique-removebg-preview.png"
            lienImageInflamable = lien + "Pictogramme-chimique-inflammable-removebg-preview.png"
            lienImageCorrosif = lien + "Pictogramme-chimique-corrosif-removebg-preview.png"
            lienImageExplosif = lien + "Pictogramme-chimique-explosion-removebg-preview.png"
            lienImageGazSousPression = lien + "Pictogramme-chimique-gaz-sous-pression-removebg-preview.png"
            lienImageCMR = lien + "Pictogramme-chimique-CMR-removebg-preview.png"
            lienImageChimiqueEnvironement = lien + "Pictogramme-chimique-environnement-removebg-preview.png"
            lienImageDangereux = lien + "Pictogramme-chimique-point-dexclamation-removebg-preview.png"
            lienImageComburant = lien + "Pictogramme-chimique-comburant-removebg-preview.png"


            explication_explosif = "Ce pictogramme chimique identifie des produits explosifs instables et très réactifs. Ces derniers peuvent exploser au contact d'une flamme, d'une étincelle, sous l'effet de la chaleur, en cas de frottement ou en cas de choc."
            explication_danger_incendie = "Le symbole de la flamme identifie des produits qui peuvent s'enflammer :\nau contact d'une flamme, d'une étincelle (ex. : benzène, acétone, éthanol, éther)\nau contact avec l'air\nau contact de l'eau en produisant des gaz inflammables qui s'enflamment spontanément ou en présence d'une source d'énergie\nLes produits identifiés par ce symbole sont variés. Ce sont :\nLes liquides inflammables, les matières solides inflammables, les gaz inflammables, les aérosols inflammables.\nLes liquides et solides pyrophoriques,\nCertains peroxydes organiques\nCertains produits autoréactifs\nLes hydroréactifs\nLes auto-échauffants"
            explication_comburant = "Ce pictogramme chimique identifie les produits comburants. Ces derniers peuvent provoquer ou aggraver un incendie en présence d'un combustible.\nIls peuvent provoquer une explosion s'ils sont en contact avec un inflammable.\nExemples : acide perchlorique, acide nitrique concentré, chlore gazeux."
            explication_gaz_sous_pression = "Ce pictogramme chimique identifie les produits sous pression dans un récipient.  En cas de chaleur, ce dernier peut exploser sous l'effet de la chaleur qui génère une expansion du gaz et une montée en pression.\nLes gaz sous pression sont classés en 4 catégories :\nLes gaz comprimés non liquéfiés\nLes gaz liquéfiés réfrigérés responsables de graves brûlures par le froid. Ce sont les fluides cryogéniques. (ex. : azote liquide)\nLes gaz liquéfiés (ex. : chlore, propane)\nLes gaz dissous (ex. : bouteille d'acétylène)"
            explication_corrosion = "Ce pictogramme de danger signale les produits chimiques pouvant :\nAttaquer ou détruire les métaux\nRonger la peau et/ou les yeux en cas de contact ou projection\nLe symbole de corrosion identifie les produits corrosifs pour les yeux, la peau et/ou les métaux.\n\nExemples : acide chlorhydrique, soude (hydroxyde de sodium), acide sulfurique."
            explication_toxicité_aiguë = "Ce pictogramme de danger identifie les produits chimiques toxiques aigus. Ils empoisonnent rapidement, même à faible dose, par inhalation, ingestion et/ou par contact cutané.\nLe symbole de toxicité aiguë identifie des produits chimiques capables de provoquer la mort quelques minutes, heures ou jours après l'exposition.\n\nExemples : méthanol, sulfure d'hydrogène, acide fluorhydrique."
            explication_altération_santé_humaine = "Ce pictogramme de danger identifie un produit chimique :\nnocif (capable d'empoisonner en cas d'exposition à forte dose)\nirritant pour la peau, les yeux ou les voies respiratoires\nqui provoque somnolence ou vertiges (ex. : acétone)\nqui provoque une irritation des voies respiratoires\ncapable de détruire la couche d'ozone en haute atmosphère (ex. : CFC)\n\nsensibilisant cutané (allergisant cutané) (Ex.: eczéma)"
            explication_effets_graves_sur_la_santé = "Ce pictogramme de danger signale au moins une des propriétés suivantes :\ncancérogène (ex.: formaldéhyde).\nmutagène sur les cellules germinales (susceptibles de provoquer des maladies génétiques héréditaires).\nreprotoxique (atteinte des capacités de reproduction telle que la fertilité, le développement de l'enfant à naître).\ntoxique pour certains organes cibles, à la suite d'une exposition unique ou suite à des expositions répétées.\nsensibilisant respiratoire (allergisant respiratoire).\nMortel par aspiration (ie. : mortel par ingestion puis pénétration dans les voies respiratoires)."
            explication_toxicité_aquatique = "Ce pictogramme de danger identifie les produits néfastes pour les organismes aquatiques (crustacés, algues, poissons).\nCe symbole de danger environnemental signale une toxicité à court terme (toxicité aiguë) ou des effets néfastes à long terme (toxicité chronique) sur les organismes aquatiques.\nExemples : eau de javel, isopentane, sodium azide."

            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, "Fiche de données de sécurité des pictogrammes", ln=1, align="C")
            self.ln(10)
            self.set_font('Arial', 'B', 12)

            list_lien_image = []

            list_explication = []

            list_lien_image.append(lienImageToxique)
            list_explication.append(explication_toxicité_aiguë)

            list_lien_image.append(lienImageInflamable)
            list_explication.append(explication_danger_incendie)

            list_lien_image.append(lienImageExplosif)
            list_explication.append(explication_explosif)

            list_lien_image.append(lienImageGazSousPression)
            list_explication.append(explication_gaz_sous_pression)

            list_lien_image.append(lienImageCMR)
            list_explication.append(explication_effets_graves_sur_la_santé)

            list_lien_image.append(lienImageChimiqueEnvironement)
            list_explication.append(explication_toxicité_aquatique)

            list_lien_image.append(lienImageDangereux)
            list_explication.append(explication_altération_santé_humaine)

            list_lien_image.append(lienImageComburant)
            list_explication.append(explication_comburant)

            list_lien_image.append(lienImageCorrosif)
            list_explication.append(explication_corrosion)
                
            x_position = 10  # Commencer à partir de la gauche
            y_position = 50  # Y initial

            for i in range(len(list_lien_image)):
                self.image(list_lien_image[i], 10, y_position, 33)
                self.ln(30)  # Sauter une ligne avant l'explication
                self.multi_cell(0, 5, list_explication[i])
                y_position += 70  # Aller à l'image suivante
                
                
    def genererpdfBonCommande(nom,prenom,liste_materiel, numero_commande):
        my_pdf = PDF_BonCommande.PDF()
        my_pdf.add_page()
        my_pdf.afficher_numero_commande(numero_commande, datetime.datetime.now().strftime("%d/%m/%Y"))
        my_pdf.cree_par(nom, prenom)
        my_pdf.affiche_materiel(liste_materiel)
        try:
            my_pdf.output("./GestLab/static/data/bonCommande.pdf")
        except:
            my_pdf.output("./static/data/bonCommande.pdf")


    def genererpdfFDS(nom, prenom,referenceMateriel, nomMateriel,estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif):
        my_pdf = PDF_BonCommande.PDF()
        my_pdf.add_page()
        my_pdf.cree_par(nom, prenom)
        my_pdf.affiche_FDS(referenceMateriel, nomMateriel, estToxique, estInflamable, estExplosif,est_gaz_sous_pression, est_CMR, est_chimique_environement, est_dangereux, est_comburant,est_corrosif)
        my_pdf.output("./GestLab/static/data/FDS.pdf")


    def genererpdfFDSPicatogramme():
        my_pdf = PDF_BonCommande.PDF()
        my_pdf.add_page()
        my_pdf.affiche_FDS_picatogramme()
        my_pdf.output("./GestLab/static/data/FDS_pictogramme.pdf")


# PDF_BonCommande.genererpdfFDS("testNom", "testPrenom", "reftest", "testNomMateriel", True, True, False, False, False, False, True, False, False)
# PDF_BonCommande.genererpdfFDSPicatogramme() # PATCH AUJOUDHUI
