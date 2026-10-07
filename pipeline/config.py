from pathlib import Path

BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
ENDPOINTS = {
    "estados": f"{BASE_URL}/estados",
    "municipios": f"{BASE_URL}/municipios",
}

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_PATH = Path("data/warehouse.db")

TIMEOUT = 30