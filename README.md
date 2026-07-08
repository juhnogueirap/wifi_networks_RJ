# WiFi Networks RJ

## Sobre o repositório

Este repositório contém os scripts desenvolvidos para o Trabalho de Conclusão de Curso (TCC) **Análise da Distribuição Espacial de Redes Wi-Fi no Estado do Rio de Janeiro**. O objetivo deste projeto é coletar informações públicas sobre redes Wi-Fi disponibilizadas pelo WiGLE e utilizá-las em análises espaciais da distribuição dessas redes no estado do Rio de Janeiro, permitindo sua comparação com indicadores socioeconômicos em diferentes recortes territoriais.

O projeto é dividido em duas etapas principais:

- **ETL**: coleta e preparação dos dados obtidos por meio da API do WiGLE;
- **Análise**: processamento, integração com dados geográficos e geração das análises utilizadas no trabalho.

---

## Requisitos

- Python 3.12+
- Pipenv (opcional, recomendado)

---

## Instalação

### Utilizando Pipenv (recomendado)

Instale as dependências:

```bash
pipenv install
```

Ative o ambiente virtual:

```bash
pipenv shell
```

### Utilizando pip

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```
---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
API_TOKEN="seu_token"
```

O token pode ser obtido em sua conta no WiGLE.

---

## Estrutura do projeto

```
├── analysis_scripts/       # Scripts de análise e geração de mapas
├── etl_scripts/            # Scripts de coleta e preparação dos dados
├── utils/                  # Funções auxiliares compartilhadas
├── wigle_data/             # Dados coletados da API do WiGLE
├── results/                # Resultados produzidos pelos scripts de análise
├── socioeconomic_data/     # Indicadores socioeconômicos utilizados
├── RJ_Municipios_2023/     # Shapefile dos municípios do RJ (IBGE)
├── Cidade_RJ_APs/          # Shapefile das Áreas de Planejamento do Rio de Janeiro
├── Bairros_Rio/            # Shapefile dos bairros da cidade do Rio de Janeiro
```

---

## Fluxo de execução

Os scripts devem ser executados na seguinte ordem:

```
01_slice_grid.py
        │
        ▼
02_request_wigle.py
        │
        ▼
03_join_results.py
        │
        ▼
map_networks_per_city_per_features.py
        │
        ├── networks_per_city.py
        ├── networks_per_APs.py
        ├── networks_per_bairro_Rio.py
        └── map_networks_per_city.py
```

---

## Scripts de ETL

Os scripts responsáveis pela coleta e preparação dos dados encontram-se na pasta `etl_scripts`.

### 01_slice_grid.py

Este script utiliza o shapefile dos municípios do estado do Rio de Janeiro (`RJ_Municipios_2023/RJ_Municipios_2023.shp`) para gerar uma grade regular de quadrantes de **0,05° × 0,05°** em latitude e longitude.

Cada quadrante representa uma área que será utilizada posteriormente nas consultas à API do WiGLE.

Ao final da execução é gerado o arquivo:

```
etl_scripts/quadrants_rj.csv
```

contendo os **1.773 quadrantes** e suas respectivas coordenadas geográficas.

---

### 02_request_wigle.py

Este script realiza a coleta de dados na API do WiGLE.

O arquivo `quadrants_rj.csv`, gerado na etapa anterior, é utilizado como entrada. Para cada quadrante é realizada uma consulta à API.

Os resultados são armazenados em:

```
wigle_data/wigleRJ-results/results_rj/
```

Os arquivos de log são salvos em:

```
wigle_data/wigleRJ-results/resume_logs/
```


  #### Continuação da coleta

  Como a API do WiGLE limita a quantidade de registros retornados por requisição, o script utiliza o parâmetro **SearchAfter** para realizar a paginação dos resultados.

  Após cada consulta, o valor de `SearchAfter` é salvo em um arquivo de log. Caso a execução seja interrompida, basta executá-la novamente para que a coleta continue a partir do último ponto processado.

  Quando todos os registros de um quadrante forem coletados, o log correspondente recebe o valor "complete", indicando que aquele quadrante não precisa mais ser consultado.

  > **Observação:** por padrão, as consultas não utilizam filtros temporais. Caso seja necessário limitar a coleta a um determinado período, os parâmetros da requisição podem ser modificados diretamente no script.

---

### 03_join_results.py

Após a conclusão da coleta, este script reúne todos os arquivos CSV obtidos na etapa anterior em um único arquivo.

O resultado é um dataset consolidado contendo todas as redes Wi-Fi coletadas para o estado do Rio de Janeiro.

---

## Scripts de análise

Os scripts de análise encontram-se na pasta `analysis_scripts`.

Esses scripts utilizam os dados consolidados obtidos na etapa de ETL para:

- contabilizar redes Wi-Fi por município;
- calcular estatísticas sobre as características das redes;
- gerar tabelas e mapas utilizados nas análises do TCC.

### map_networks_per_city_per_features.py

Este script realiza a contagem de redes Wi-Fi por município do estado do Rio de Janeiro e contabiliza algumas características das redes encontradas, incluindo:

- tipo de infraestrutura (Infraestruturada ou Ad-Hoc);
- protocolo de segurança (Aberta, WEP, WPA e WPA2);
- frequência de operação (2,4 GHz, 5 GHz e 6 GHz).

Como entrada, o script utiliza o arquivo consolidado:

```
wigle_data/wigle_results.csv
```

O parâmetro `CUTOFF_DATE` permite aplicar um recorte temporal às redes consideradas na análise, descartando registros cuja última detecção seja anterior à data especificada.

Como saída, é gerado o arquivo:

```
results/networks_per_city_per_features.csv
```

com a seguinte estrutura:

```csv
NM_MUN,network_count,infra_count,adhoc_count,wep_count,wpa_count,wpa2_count,open_count,freq_24ghz_count,freq_5ghz_count,freq_6ghz_count
```

Esse arquivo serve como base para as demais análises e visualizações desenvolvidas no trabalho.

## Resultados

Os resultados das análises estão na pasta `results`.

## Fontes de dados

O projeto utiliza dados provenientes de:

- WiGLE — Base colaborativa de redes Wi-Fi.
- IBGE — Malha municipal do estado do Rio de Janeiro.
- Atlas Brasil — Índice de Desenvolvimento Humano Municipal (IDHM).
- Data Rio — Dados geográficos dos bairros e Áreas de Planejamento do município do Rio de Janeiro.

## Limitações

- Os dados do WiGLE são colaborativos e dependem das contribuições dos usuários da plataforma.
- A cobertura espacial não representa necessariamente todas as redes Wi-Fi existentes.
- As consultas estão sujeitas aos limites de requisições impostos pela API do WiGLE.

## Citação


Caso este repositório contribua para sua pesquisa, cite:

```bibtex
@bachelorsthesis{peixoto2026,
  author = {Juliana Peixoto},
  title = {Análise da Distribuição Espacial de Redes Wi-Fi no Estado do Rio de Janeiro},
  school = {Universidade Federal Rural do Rio de Janeiro},
  address = {Nova Iguaçu, RJ},
  year = {2026},
  type = {Trabalho de Conclusão de Curso}
}
```
