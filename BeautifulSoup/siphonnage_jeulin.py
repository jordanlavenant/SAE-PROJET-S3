from bs4 import BeautifulSoup
soup = BeautifulSoup(open("./BeautifulSoup/Physique-Chimie - Matériel pour TP Jeulin.html"), "html.parser")

#print(soup.prettify())
print(soup.title)
print(soup.get_text())