import pandas as pd
import pytest

from pipeline.transform import transformar_estados, transformar_municipios
from pipeline.validate import ErroValidacao, validar_estados


def test_transformar_estados_padroniza_colunas():
    dados = [{"id": 12, "sigla": "AC", "nome": "Acre",
              "regiao": {"id": 1, "sigla": "N", "nome": "Norte"}}]
    df = transformar_estados(dados)
    assert list(df.columns) == ["estado_id", "estado_sigla", "estado_nome",
                                "regiao_sigla", "regiao_nome"]
    assert df.loc[0, "estado_sigla"] == "AC"


def test_transformar_municipios_extrai_uf():
    dados = [{"id": 3205309, "nome": "Vitória",
              "regiao-imediata": {"regiao-intermediaria": {"UF": {"id": 32, "sigla": "ES"}}}}]
    df = transformar_municipios(dados)
    assert df.loc[0, "estado_sigla"] == "ES"


def test_validar_estados_rejeita_quantidade_errada():
    df = pd.DataFrame({"estado_id": [1, 2]})
    with pytest.raises(ErroValidacao):
        validar_estados(df)