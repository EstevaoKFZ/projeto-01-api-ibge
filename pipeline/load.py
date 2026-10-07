import logging
import sqlite3
from contextlib import closing

from .config import DB_PATH, PROCESSED_DIR

logger = logging.getLogger(__name__)


def salvar_arquivos(df, nome):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED_DIR / f"{nome}.parquet", index=False)
    df.to_csv(PROCESSED_DIR / f"{nome}.csv", index=False, encoding="utf-8")
    logger.info("'%s' salvo em %s (parquet e csv)", nome, PROCESSED_DIR)


def carregar_sqlite(df, tabela):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        df.to_sql(tabela, conn, if_exists="replace", index=False)
    logger.info("tabela '%s' carregada em %s (%d linhas)", tabela, DB_PATH, len(df))