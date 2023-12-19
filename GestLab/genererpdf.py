from fpdf import FPDF #pip install fpdf
import datetime

title = "GestLab"

class PDF_BonCommande:
    class PDF(FPDF):
        def header(self):
            #logo
            self.image('./GestLab/static/images/logo-GestLab.png', 10, 8, 33)
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
        
        def affiche_FDS(self,referenceMateriel, nomMateriel, estToxique, estInflamable):
            #image
            lienImageLogo = "./GestLab/static/images/logo-Gestlab.png"
            lienImageToxique = "./GestLab/static/images/pictogramme-chimique-toxique.png"
            lienImageInflamable = "./GestLab/static/images/pictogramme-chimique-inflammable.png"
            lienImageCorrosif = "./GestLab/static/images/corrosif.png"

            explication_toxique = "Ce pictogramme de danger identifie les produits chimiques toxiques aigus. Ils peuvent empoisonner rapidement, même à de faibles doses, par inhalation, ingestion ou contact cutané. Ces substances peuvent entraîner la mort quelques minutes, heures ou jours après l'exposition. Exemples : méthanol, sulfure d'hydrogène, acide fluorhydrique."
            explication_inflamable = "Ce symbole signale des produits inflammables pouvant s'enflammer au contact d'une flamme, d'une étincelle, de l'air, de l'eau, ou en présence d'une source d'énergie. Il inclut liquides, solides inflammables, gaz, aérosols inflammables, liquides et solides pyrophoriques, certains peroxydes, produits autoréactifs, hydroréactifs et auto-échauffants."


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
                list_explication.append(explication_toxique)

            if estInflamable:
                list_lien_image.append(lienImageInflamable)
                list_explication.append(explication_inflamable)
    
            # if estCorrisif:
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)
            #     list_lien_image.append(lienImageCorrosif)

            x_position = 10  # Commencer à partir de la gauche
            y_position = 100  # Y initial

            for lien_image in list_lien_image:
                if x_position + 33 > self.w:  # Vérifie si l'image sort du cadre
                    x_position = 10  # Revenir à gauche
                    y_position += 40  # Aller à la ligne suivante
                    self.ln(40)  # Sauter une ligne dans le PDF

                self.image(lien_image, x_position, y_position, 33)
                x_position += 40  # Décaler horizontalement pour la prochaine image

            self.ln(50)  # Sauter une ligne dans le PDF

            # Ajout des explications
            self.set_font('Arial', '', 10)
            for explication in list_explication:
                
                self.multi_cell(0, 5, explication)
                self.ln(6)
                
            
                        

    def genererpdfBonCommande(nom,prenom,liste_materiel, numero_commande):
        my_pdf = PDF_BonCommande.PDF()
        my_pdf.add_page()
        my_pdf.afficher_numero_commande(numero_commande, datetime.datetime.now().strftime("%d/%m/%Y"))
        my_pdf.cree_par(nom, prenom)
        my_pdf.affiche_materiel(liste_materiel)
        my_pdf.output("./GestLab/static/data/bonCommande.pdf")


    def genererpdfFDS(nom, prenom,referenceMateriel, nomMateriel,estToxique, estInflamable):
        my_pdf = PDF_BonCommande.PDF()
        my_pdf.add_page()
        my_pdf.affiche_FDS(referenceMateriel, nomMateriel, estToxique, estInflamable)
        my_pdf.output("./GestLab/static/data/FDS.pdf")


PDF_BonCommande.genererpdfFDS("testNom", "testPrenom", "reftest", "testNomMateriel", True, True)



