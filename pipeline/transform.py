import pandas as pd


def transformar_estados(dados):
    """Estados: tabela plana com nomes de colunas padronizados."""
    df = pd.json_normalize(dados)
    df = df[["id", "sigla", "nome", "regiao.sigla", "regiao.nome"]]
    df = df.rename(columns={
        "id": "estado_id",
        "sigla": "estado_sigla",
        "nome": "estado_nome",
        "regiao.sigla": "regiao_sigla",
        "regiao.nome": "regiao_nome",
    })
    return df.sort_values("estado_nome").reset_index(drop=True)


def _extrair_uf(item):
    """Os municípios têm a UF aninhada em caminhos diferentes. Tenta os dois."""
    imediata = item.get("regiao-imediata") or {}
    uf = (imediata.get("regiao-intermediaria") or {}).get("UF")
    if uf:
        return uf
    micro = item.get("microrregiao") or {}
    return (micro.get("mesorregiao") or {}).get("UF") or {}


def transformar_municipios(dados):
    """Municípios: um registro por município, com a UF a que pertence."""
    linhas = []
    for item in dados:
        uf = _extrair_uf(item)
        linhas.append({
            "municipio_id": item["id"],
            "municipio_nome": item["nome"],
            "estado_id": uf.get("id"),
            "estado_sigla": uf.get("sigla"),
        })
    df = pd.DataFrame(linhas)
    return df.sort_values("municipio_nome").reset_index(drop=True)