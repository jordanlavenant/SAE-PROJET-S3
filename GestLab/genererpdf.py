from fpdf import FPDF
import datetime

title = "GestLab"

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


    def affiche_materiel(self, liste_materiel):
        self.set_font('Arial', 'B', 10)
        self.cell(38, 10, "Nom", border=True, align="C")
        self.cell(38, 10, "Quantité", border=True, align="C")
        self.cell(38, 10, "Réference", border=True, align="C")
        self.cell(38, 10, "Domaine", border=True, align="C")
        self.cell(38, 10, "Categorie", border=True, align="C")
        self.ln(10)
        for materiel in liste_materiel:
            self.set_font('Arial', '', 8)
            self.cell(38, 10, materiel[0], border=True, align="C")
            self.cell(38, 10, materiel[1], border=True, align="C")
            self.cell(38, 10, materiel[2], border=True, align="C")
            self.cell(38, 10, materiel[3], border=True, align="C")
            self.cell(38, 10, materiel[4], border=True, align="C")
            self.ln(10)



def genererpdf(nom,prenom,liste_materiel, numero_commande):
    my_pdf = PDF()
    my_pdf.add_page()
    my_pdf.afficher_numero_commande(numero_commande, datetime.datetime.now().strftime("%d/%m/%Y"))
    my_pdf.affiche_materiel(liste_materiel)
    my_pdf.output("./GestLab/static/data/bonCommande.pdf")


# liste_materiel = [["bouteillebouteillebouteilleeeeeeeeeef", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "4", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"], ["bouteille", "2", "ref1", "domaine1", "categorie1"]]
# genererpdf("blandeau","erwan",liste_materiel, "1")