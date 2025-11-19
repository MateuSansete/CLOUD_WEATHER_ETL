# CLOUD_WEATHER_ETL: Pipeline Serverless de Ingestão de API (GCP)

Este projeto implementa uma solução **Serverless (sem servidor)** para coleta, transformação e ingestão de dados da API OpenWeatherMap, demonstrando um fluxo de trabalho moderno de Engenharia de Dados na Nuvem.

O objetivo é automatizar a ingestão de dados em tempo real, utilizando serviços gerenciados da Google Cloud Platform (GCP) para garantir escalabilidade e baixo custo operacional.

## Arquitetura do Pipeline

O pipeline segue o padrão moderno de **ELT (Extract, Load, Transform)**:

1. **Extract (E) & Load (L):** Um **Cloud Scheduler** dispara uma **Cloud Function** (código Python). A função extrai dados da API OpenWeatherMap e salva o arquivo processado em formato **Parquet** no **GCS (Google Cloud Storage)**, atuando como a camada Bronze (Raw Data).
2. **Transform (T):** Um job de `Load` no BigQuery move os dados do GCS para uma tabela final de análise.
3. **Data Warehouse:** **BigQuery** é usado para o armazenamento final e consulta dos dados.

## Tecnologias Utilizadas

| Categoria | Ferramenta | Uso no Projeto |
| :--- | :--- | :--- |
| **Computação** | **Google Cloud Functions** | Ambiente Serverless para rodar o código Python (ETL/ELT). |
| **Automação** | **Google Cloud Scheduler** | Agendamento da Cloud Function (Execução diária/horária). |
| **Armazenamento** | **Google Cloud Storage (GCS)** | Data Lake para armazenar os dados brutos/processados em Parquet. |
| **Data Warehouse** | **Google BigQuery** | Destino final para análise escalável via SQL. |
| **Linguagem/Bibliotecas** | **Python, Pandas, Requests, pyarrow** | Extração de API, Transformação de JSON para DataFrame e serialização Parquet. |

## Como Implantar e Executar o Projeto (Fase 3)

### Pré-requisitos

1. Conta ativa no **Google Cloud Platform (GCP)** com faturamento habilitado.
2. **Google Cloud CLI (gcloud)** instalado e autenticado (`gcloud auth login`).
3. APIs habilitadas: Cloud Functions API, Cloud Storage API, BigQuery API, Cloud Scheduler API.
4. Chave da API OpenWeatherMap.

### 1. Configuração Local e Credenciais

Crie o arquivo `.env` (ou exporte as variáveis de ambiente) e crie o arquivo de dependências.

```bash
# 1. Instalar dependências locais para desenvolvimento e teste
pip install -r requirements.txt

# 2. Criar e preencher o arquivo .env (com a API Key)
# Exemplo: OPENWEATHER_API_KEY=sua_chave_aqui
```

### 2. Criação dos Recursos na Nuvem

Você precisará criar os recursos de armazenamento e o Data Warehouse.

```bash
# Definir variáveis de ambiente GCP
export GCP_PROJECT_ID="SEU_ID_DO_PROJETO"
export GCS_BUCKET_NAME="weather-etl-bucket-seu-nome"
export BQ_DATASET_NAME="weather_data_lake"

# Criação do GCS Bucket
gsutil mb gs://${GCS_BUCKET_NAME}

# Criação do Dataset BigQuery
bq mk ${BQ_DATASET_NAME}
```

### 3. Implantação da Cloud Function

O gcloud fará o deploy do seu arquivo main.py como a Cloud Function que rodará o ETL.

```bash
gcloud functions deploy run_weather_etl \
  --runtime python39 \
  --trigger-http \
  --entry-point run_weather_etl \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=SUA_CHAVE_AQUI
```

(Nota: O valor da API Key deve ser injetado diretamente na linha de comando ou via Secret Manager no ambiente de produção real.)

### 4. Automação (Cloud Scheduler)

Crie um job no Cloud Scheduler para disparar a URL da sua Cloud Function diariamente.

### 5. Validação

Acesse o console do BigQuery e rode a consulta para verificar se os dados estão sendo carregados na tabela a cada execução agendada.

```sql
```sql
SELECT * FROM `seu-projeto.weather_data_lake.raw_weather` LIMIT 10;
```