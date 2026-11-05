# Pipeline de dados públicos de saúde

Pipeline acadêmico em Python para coletar um CSV de dados governamentais de saúde, tratar seus indicadores e gerar estatísticas, visualizações e uma base SQLite.

## Fluxo

1. Lê os parâmetros de `config.json`.
2. Baixa o CSV caso ainda não exista no diretório local.
3. Limpa nomes de colunas, extrai o ano de `co_anomes`, converte indicadores para números e remove linhas sem indicador municipal válido.
4. Seleciona os últimos dez anos disponíveis nos dados, conforme a configuração.
5. Calcula estatísticas descritivas gerais e por ano.
6. Gera gráficos por ano, região e unidade federativa.
7. Grava os dados filtrados em SQLite e as estatísticas em JSON.

## Executar

Requisitos: Python 3 e acesso à internet para o primeiro download.

```bash
git clone https://github.com/edularson/CienciaDeDados.git
cd CienciaDeDados/Trabalho2
python -m venv .venv
```

Ative o ambiente com `source .venv/bin/activate` no Linux/macOS ou `.venv\Scripts\activate` no Windows.

```bash
python -m pip install -r requirements.txt
python pipeline.py
```

Execute a partir desta pasta, pois os caminhos são relativos ao diretório atual.

## Configuração e fonte

A URL de origem e os nomes das colunas estão em [`config.json`](config.json). A configuração atual usa um CSV hospedado no endereço `demas-dados-abertos.s3.amazonaws.com`, com o campo temporal `co_anomes` e os indicadores `vl_indicador_calculado_mun`, `vl_indicador_calculado_uf` e `vl_indicador_calculado_br`.

Antes de interpretar os gráficos, consulte a documentação da fonte para identificar a definição, a unidade e a possibilidade de agregar o indicador. A soma de taxas ou percentuais, por exemplo, não equivale necessariamente a um total populacional.

Para usar outro arquivo, ajuste a URL, o separador, a codificação e o mapeamento das colunas. O programa reutiliza um CSV já baixado; para atualizar os dados, renomeie ou remova sua cópia local antes de executar novamente.

## Saídas padrão

| Arquivo | Conteúdo |
| --- | --- |
| `estatisticas.json` | Média, mínimo, máximo, soma, variância, desvio padrão e estatísticas por ano |
| `grafico_indicador_por_ano.png` | Soma do indicador municipal por ano |
| `grafico_indicador_por_regiao.png` | Distribuição da soma por região |
| `grafico_top10_uf.png` | Dez UFs com maior soma do indicador |
| `saude.db` | Tabela `indicador_saude` com os registros filtrados |

As saídas são substituídas em novas execuções; a gravação da tabela usa `if_exists="replace"`.

## Tecnologias

Python, pandas, Matplotlib, SQLite, JSON e `urllib.request`.
