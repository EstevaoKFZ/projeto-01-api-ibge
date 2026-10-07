import logging

logger = logging.getLogger(__name__)


class ErroValidacao(Exception):
    """Levantado quando os dados não passam nas verificações de qualidade."""


def _checar(erros, contexto):
    if erros:
        for erro in erros:
            logger.error("[%s] %s", contexto, erro)
        raise ErroValidacao(f"{contexto}: {len(erros)} problema(s) encontrado(s)")
    logger.info("[%s] validação OK", contexto)


def validar_estados(df):
    erros = []
    if len(df) != 27:
        erros.append(f"esperado 27 UFs, encontrado {len(df)}")
    if df["estado_id"].duplicated().any():
        erros.append("há estado_id duplicado")
    if df.isna().any().any():
        erros.append("há valores nulos")
    _checar(erros, "estados")


def validar_municipios(df, estados):
    erros = []
    if len(df) < 5500:
        erros.append(f"esperado ao menos 5500 municípios, encontrado {len(df)}")
    if df["municipio_id"].duplicated().any():
        erros.append("há municipio_id duplicado")
    if df["estado_id"].isna().any():
        erros.append("há municípios sem estado")
    elif not df["estado_id"].isin(estados["estado_id"]).all():
        erros.append("há municípios ligados a estado inexistente")
    _checar(erros, "municipios")