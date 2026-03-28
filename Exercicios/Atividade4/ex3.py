import requests
from bs4 import BeautifulSoup

url = "https://www.flamengo.com.br/"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, "html.parser")

titulos = soup.find_all("h2")

for titulo in titulos:
    print(titulo.get_text())