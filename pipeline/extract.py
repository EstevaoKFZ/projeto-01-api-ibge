import json
import logging
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import RAW_DIR, TIMEOUT

logger = logging.getLogger(__name__)


def criar_sessao():
    """Sessão HTTP que tenta de novo se a API falhar temporariamente."""
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    sessao = requests.Session()
    sessao.mount("https://", HTTPAdapter(max_retries=retry))
    return sessao


def extrair(nome, url):
    """Busca os dados da API e guarda uma cópia bruta em data/raw."""
    logger.info("Extraindo '%s' de %s", nome, url)
    with criar_sessao() as sessao:
        resposta = sessao.get(url, timeout=TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    caminho = RAW_DIR / f"{nome}_{datetime.now():%Y%m%d_%H%M%S}.json"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    logger.info("%d registros extraídos, cópia bruta em %s", len(dados), caminho)
    return dados