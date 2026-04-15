import bs4
import requests

resultado = requests.get('https://www.escueladirecta.com/l/products?sortKey=name&sortDirection=asc&page=1')

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
"""

# print(len(sopa.select('h1')))
# print(sopa.select('title')[0].getText())

parrafo_especial = sopa.select('h1')[0].getText()

print(parrafo_especial)

columna_lateral = sopa.select('.post-title')

for p in columna_lateral:
    print(p.getText())

imagenes = sopa.select('.ProductImage')[0]['src']
print(imagenes)

imagen_curso = requests.get(imagenes)

f = open('mi_imagen.jpg', 'wb')
f.write(imagen_curso.content)
f.close()"""

