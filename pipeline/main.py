import logging

from .config import ENDPOINTS
from .extract import extrair
from .load import carregar_sqlite, salvar_arquivos
from .transform import transformar_estados, transformar_municipios
from .validate import validar_estados, validar_municipios

logger = logging.getLogger(__name__)


def executar():
    # Extração
    estados_raw = extrair("estados", ENDPOINTS["estados"])
    municipios_raw = extrair("municipios", ENDPOINTS["municipios"])

    # Transformação
    estados = transformar_estados(estados_raw)
    municipios = transformar_municipios(municipios_raw)

    # Validação
    validar_estados(estados)
    validar_municipios(municipios, estados)

    # Carga
    salvar_arquivos(estados, "estados")
    salvar_arquivos(municipios, "municipios")
    carregar_sqlite(estados, "dim_estado")
    carregar_sqlite(municipios, "dim_municipio")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    try:
        executar()
        logger.info("Pipeline concluído com sucesso")
    except Exception:
        logger.exception("Pipeline falhou")
        raise SystemExit(1)


if __name__ == "__main__":
    main()