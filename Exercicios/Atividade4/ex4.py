import requests

topico = "data-science"
url = f"https://api.github.com/search/repositories?q={topico}&sort=stars&order=desc"

response = requests.get(url)
dados = response.json()

for repo in dados["items"][:5]:
    print(f"Nome: {repo['name']}")
    print(f"URL: {repo['html_url']}")
    print("---")