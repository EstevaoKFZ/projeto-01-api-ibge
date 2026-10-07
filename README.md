# projeto-01-api-ibge
# Pipeline de dados do IBGE: estados e municípios

Pipeline ETL em Python que extrai dados de localidades da API pública do IBGE,
valida a qualidade, e carrega em arquivos Parquet/CSV e em um banco SQLite.

> Projeto em evolução, construído como parte dos meus estudos em Engenharia de Dados.

## O que o pipeline faz

1. **Extrai** estados e municípios da API do IBGE (com tentativas automáticas em caso de falha)
2. **Guarda o JSON bruto** em `data/raw/`, para não depender de chamar a API de novo
3. **Transforma** o JSON aninhado em tabelas planas com nomes padronizados
4. **Valida** os dados (quantidade esperada, duplicados, nulos, integridade entre tabelas)
5. **Carrega** em Parquet/CSV (`data/processed/`) e em SQLite (`data/warehouse.db`)

## Arquitetura

```
API IBGE → extração (JSON bruto) → transformação → validação → Parquet/CSV + SQLite
```

## Tecnologias

Python, pandas, requests, pyarrow, SQLite, pytest, Git/GitHub

## Como rodar

```bash
git clone https://github.com/EstevaoKFZ/projeto-01-api-ibge.git
cd projeto-01-api-ibge
python -m venv .venv
.venv\Scripts\activate          # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

python -m pipeline.main         # executa o pipeline
python -m pytest                # executa os testes
```

## Estrutura

```
pipeline/
  config.py      # URLs e caminhos
  extract.py     # coleta da API e dado bruto
  transform.py   # limpeza e padronização
  validate.py    # regras de qualidade
  load.py        # saída em arquivos e banco
  main.py        # orquestra as etapas
tests/
  test_pipeline.py
```

## Tabelas geradas

- `dim_estado`: 27 UFs com região
- `dim_municipio`: 5.571 municípios com a UF a que pertencem

## Próximos passos

- [ ] Tabela fato de população por município (SIDRA/IBGE)
- [ ] Consultas SQL analíticas sobre o banco
- [ ] Trocar SQLite por PostgreSQL com Docker
- [ ] Orquestração com Airflow e transformações com dbt
- [ ] Testes automáticos com GitHub Actions