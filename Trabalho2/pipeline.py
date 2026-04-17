import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sqlite3
import json
import urllib.request
import os
import sys


# ─────────────────────────────────────────
# 1. CONFIGURAÇÃO
# ─────────────────────────────────────────

def carregar_config(caminho_json: str) -> dict:
    """Lê o arquivo JSON de configuração e retorna um dicionário."""
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)


# ─────────────────────────────────────────
# 2. COLETA DE DADOS
# ─────────────────────────────────────────

def baixar_csv(config: dict) -> None:
    """
    Tenta baixar o CSV da URL definida no config.
    Se o arquivo local já existir, pula o download.
    """
    url = config["input_config"]["csv_url"]
    destino = config["input_config"]["csv_local"]

    if os.path.exists(destino):
        print(f"[INFO] CSV já encontrado localmente: '{destino}'. Pulando download.")
        return

    print(f"[INFO] Baixando CSV de:\n       {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(destino, 'wb') as f:
                f.write(response.read())
        print(f"[OK]   CSV salvo em '{destino}'.")
    except Exception as e:
        print(f"[ERRO] Não foi possível baixar o CSV: {e}")
        sys.exit(1)


# ─────────────────────────────────────────
# 3. CARREGAMENTO E TRATAMENTO
# ─────────────────────────────────────────

def carregar_dados(config: dict) -> pd.DataFrame:
    """
    Lê o CSV, limpa e converte os tipos necessários.
    Extrai o ano a partir da coluna co_anomes (formato AAAAMM).
    """
    caminho = config["input_config"]["csv_local"]
    sep = config["input_config"]["separator"]
    enc = config["input_config"]["encoding"]

    df = pd.read_csv(caminho, sep=sep, encoding=enc)
    df.columns = df.columns.str.strip()

    col_anomes = config["columns_config"]["anomes_column"]
    col_ano = config["columns_config"]["year_column"]
    col_ind_mun = config["columns_config"]["indicador_mun_column"]
    col_ind_uf = config["columns_config"]["indicador_uf_column"]
    col_ind_br = config["columns_config"]["indicador_br_column"]

    # Extrai o ano (primeiros 4 dígitos de co_anomes: ex. 202512 → 2016)
    df[col_ano] = df[col_anomes].astype(str).str[:4].astype(int)

    # Converte colunas de indicador para numérico
    for col in [col_ind_mun, col_ind_uf, col_ind_br]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=[col_ind_mun])

    print(f"[OK]   Dados carregados: {len(df):,} registros | {df[col_ano].nunique()} anos | {df['sg_uf'].nunique()} UFs")
    return df


# ─────────────────────────────────────────
# 4. FILTRO POR PERÍODO
# ─────────────────────────────────────────

def filtrar_ultimos_anos(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Filtra os N últimos anos presentes nos dados."""
    col_ano = config["columns_config"]["year_column"]
    n = config["filter_config"]["last_n_years"]

    anos_ordenados = sorted(df[col_ano].unique())
    ultimos_anos = anos_ordenados[-n:]
    df_filtrado = df[df[col_ano].isin(ultimos_anos)].copy()

    print(f"[OK]   Filtro aplicado: últimos {n} anos → {ultimos_anos[0]} a {ultimos_anos[-1]} ({len(df_filtrado):,} registros)")
    return df_filtrado


# ─────────────────────────────────────────
# 5. ESTATÍSTICAS
# ─────────────────────────────────────────

def calcular_estatisticas(df: pd.DataFrame, config: dict) -> dict:
    """Calcula estatísticas descritivas do indicador municipal."""
    col_ind = config["columns_config"]["indicador_mun_column"]
    col_ano = config["columns_config"]["year_column"]

    stats_gerais = df[col_ind].describe().to_dict()
    stats_gerais["sum"] = df[col_ind].sum()
    stats_gerais["variance"] = df[col_ind].var()

    # Estatísticas por ano
    stats_por_ano = (
        df.groupby(col_ano)[col_ind]
        .agg(["mean", "max", "min", "sum"])
        .rename(columns={"mean": "media", "max": "maximo", "min": "minimo", "sum": "total"})
        .to_dict(orient="index")
    )

    resultado = {"geral": stats_gerais, "por_ano": stats_por_ano}

    # Salva em JSON
    caminho_stats = config["output_config"]["stats_path"]
    with open(caminho_stats, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2, default=str)

    return resultado


# ─────────────────────────────────────────
# 6. GRÁFICOS
# ─────────────────────────────────────────

def gerar_grafico_por_ano(df: pd.DataFrame, config: dict) -> None:
    """Gráfico de linha: evolução do indicador total por ano."""
    col_ano = config["columns_config"]["year_column"]
    col_ind = config["columns_config"]["indicador_mun_column"]
    caminho = config["output_config"]["graph_path"]

    serie = df.groupby(col_ano)[col_ind].sum()

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(serie.index, serie.values, marker='o', linewidth=2.5, color='steelblue', markersize=7)
    ax.fill_between(serie.index, serie.values, alpha=0.12, color='steelblue')

    ax.set_title("Evolução do Indicador de Saúde por Ano", fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Total do Indicador (municípios)", fontsize=11)
    ax.set_xticks(serie.index)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close()
    print(f"[OK]   Gráfico salvo: {caminho}")


def gerar_grafico_por_regiao(df: pd.DataFrame, config: dict) -> None:
    """Gráfico de pizza: distribuição do indicador por região do Brasil."""
    col_regiao = config["columns_config"]["regiao_column"]
    col_ind = config["columns_config"]["indicador_mun_column"]
    caminho = config["output_config"]["region_graph_path"]

    serie = df.groupby(col_regiao)[col_ind].sum().sort_values(ascending=False)

    cores = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        serie.values,
        labels=serie.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=cores,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    ax.set_title("Distribuição do Indicador de Saúde por Região", fontsize=13, fontweight='bold', pad=15)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close()
    print(f"[OK]   Gráfico salvo: {caminho}")


def gerar_grafico_top10_uf(df: pd.DataFrame, config: dict) -> None:
    """Gráfico adicional: top 10 UFs com maior indicador acumulado."""
    col_uf = config["columns_config"]["uf_column"]
    col_ind = config["columns_config"]["indicador_mun_column"]
    caminho = config["output_config"]["uf_graph_path"]

    serie = df.groupby(col_uf)[col_ind].sum().sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(serie.index, serie.values, color='steelblue', edgecolor='white')

    # Rótulos nas barras
    for bar in bars:
        w = bar.get_width()
        ax.text(w * 1.005, bar.get_y() + bar.get_height() / 2,
                f"{w:,.0f}", va='center', ha='left', fontsize=9)

    ax.set_title("Top 10 Estados — Indicador de Saúde Acumulado", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Total do Indicador", fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close()
    print(f"[OK]   Gráfico salvo: {caminho}")


# ─────────────────────────────────────────
# 7. BANCO DE DADOS
# ─────────────────────────────────────────

def salvar_no_banco(df: pd.DataFrame, config: dict) -> None:
    """Salva o DataFrame filtrado em uma tabela SQLite."""
    caminho_banco = config["output_config"]["database_path"]
    nome_tabela = config["output_config"]["table_name"]

    conn = sqlite3.connect(caminho_banco)
    df.to_sql(nome_tabela, conn, if_exists="replace", index=False)
    conn.close()
    print(f"[OK]   Dados salvos no banco SQLite: '{caminho_banco}' → tabela '{nome_tabela}'")


# ─────────────────────────────────────────
# 8. MAIN — PIPELINE COMPLETO
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("  PIPELINE DE DADOS GOVERNAMENTAIS — SAÚDE")
    print("=" * 50 + "\n")

    # 1. Config
    config = carregar_config("config.json")

    # 2. Coleta (download automático se necessário)
    baixar_csv(config)

    # 3. Carregamento e tratamento
    df = carregar_dados(config)

    # 4. Filtro: últimos 10 anos
    df_filtrado = filtrar_ultimos_anos(df, config)

    # 5. Estatísticas
    stats = calcular_estatisticas(df_filtrado, config)
    print("\n── ESTATÍSTICAS GERAIS (indicador municipal) ──")
    g = stats["geral"]
    print(f"  Média:     {g['mean']:>15,.2f}")
    print(f"  Máximo:    {g['max']:>15,.2f}")
    print(f"  Mínimo:    {g['min']:>15,.2f}")
    print(f"  Soma:      {g['sum']:>15,.2f}")
    print(f"  Variância: {g['variance']:>15,.2f}")
    print(f"  Desvio P.: {g['std']:>15,.2f}")

    # 6. Gráficos
    print("\n── GERANDO GRÁFICOS ──")
    gerar_grafico_por_ano(df_filtrado, config)
    gerar_grafico_por_regiao(df_filtrado, config)
    gerar_grafico_top10_uf(df_filtrado, config)

    # 7. Banco de dados
    print("\n── SALVANDO NO BANCO ──")
    salvar_no_banco(df_filtrado, config)

    print("\n" + "=" * 50)
    print("  PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()