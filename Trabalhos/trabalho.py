import os
import json
import requests
from pathlib import Path


def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def criar_pastas(*pastas):
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)


def limpar_nome_arquivo(nome):
    invalidos = '<>:"/\\|?*'
    for c in invalidos:
        nome = nome.replace(c, "_")
    return nome.strip()


def salvar_texto(caminho_arquivo, dados, fields):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        for field in fields:
            if field == "strThumb":
                continue
            valor = dados.get(field, "N/A")
            arquivo.write(f"{field}: {valor}\n\n")


def salvar_historico(caminho_arquivo, termo, resultado):
    with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Pesquisa: {termo} | Resultado: {resultado}\n")


def baixar_imagem(url, caminho_arquivo):
    if not url or url == "N/A":
        return False
    try:
        resposta = requests.get(url, timeout=20)
        resposta.raise_for_status()
        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(resposta.content)
        return True
    except requests.RequestException:
        return False


def buscar_jogador(base_url, api_key, termo):
    url = f"{base_url}/{api_key}/searchplayers.php"
    resposta = requests.get(url, params={"p": termo}, timeout=20)
    resposta.raise_for_status()
    dados = resposta.json()
    jogadores = dados.get("player")
    if not jogadores:
        return None
    return jogadores[0]


def main():
    credenciais = carregar_json("credentials.json")
    config = carregar_json("config.json")

    api_key      = credenciais["API_KEY"]
    base_url     = config["api"]["base_url"]
    fields       = config["data_config"]["fields_to_extract"]
    text_dir     = config["output_config"]["text_dir"]
    image_dir    = config["output_config"]["image_dir"]
    history_file = config["output_config"]["history_file"]

    criar_pastas(text_dir, image_dir, "resultados")

    termo_pesquisa = input("Digite o nome do jogador: ").strip()
    if not termo_pesquisa:
        print("Nenhum jogador foi informado.")
        return

    try:
        jogador = buscar_jogador(base_url, api_key, termo_pesquisa)
        if not jogador:
            print("Jogador não encontrado.")
            return

        nome_jogador = jogador.get("strPlayer", "Sem nome")
        url_imagem   = jogador.get("strThumb") or jogador.get("strCutout")
        nome_base    = limpar_nome_arquivo(nome_jogador)

        caminho_texto  = os.path.join(text_dir, f"{nome_base}.txt")
        caminho_imagem = os.path.join(image_dir, f"{nome_base}.jpg")

        salvar_texto(caminho_texto, jogador, fields)
        salvar_historico(history_file, termo_pesquisa, nome_jogador)

        imagem_salva = baixar_imagem(url_imagem, caminho_imagem)

        print("\nResultado da pesquisa:")
        print(f"Jogador    : {nome_jogador}")
        print(f"Time       : {jogador.get('strTeam', 'N/A')}")
        print(f"Posição    : {jogador.get('strPosition', 'N/A')}")
        print(f"Nascimento : {jogador.get('dateBorn', 'N/A')}")
        print(f"Nac.       : {jogador.get('strNationality', 'N/A')}")
        print(f"\nTexto salvo em: {caminho_texto}")
        if imagem_salva:
            print(f"Imagem salva em: {caminho_imagem}")
        else:
            print("Imagem não disponível.")

    except requests.RequestException as erro:
        print(f"Erro na requisição: {erro}")
    except FileNotFoundError as erro:
        print(f"Arquivo não encontrado: {erro}")
    except json.JSONDecodeError:
        print("Erro ao ler os arquivos JSON.")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")


if __name__ == "__main__":
    main()