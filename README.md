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


------



Tipo e descrição 
O commit semântico possui os elementos estruturais abaixo (tipos), que informam a intenção do seu commit ao utilizador(a) de seu código.

feat- Commits do tipo feat indicam que seu trecho de código está incluindo um novo recurso (se relaciona com o MINOR do versionamento semântico).

fix - Commits do tipo fix indicam que seu trecho de código commitado está solucionando um problema (bug fix), (se relaciona com o PATCH do versionamento semântico).

docs - Commits do tipo docs indicam que houveram mudanças na documentação, como por exemplo no Readme do seu repositório. (Não inclui alterações em código).

test - Commits do tipo test são utilizados quando são realizadas alterações em testes, seja criando, alterando ou excluindo testes unitários. (Não inclui alterações em código)

build - Commits do tipo build são utilizados quando são realizadas modificações em arquivos de build e dependências.

perf - Commits do tipo perf servem para identificar quaisquer alterações de código que estejam relacionadas a performance.

style - Commits do tipo style indicam que houveram alterações referentes a formatações de código, semicolons, trailing spaces, lint... (Não inclui alterações em código).

refactor - Commits do tipo refactor referem-se a mudanças devido a refatorações que não alterem sua funcionalidade, como por exemplo, uma alteração no formato como é processada determinada parte da tela, mas que manteve a mesma funcionalidade, ou melhorias de performance devido a um code review.

chore - Commits do tipo chore indicam atualizações de tarefas de build, configurações de administrador, pacotes... como por exemplo adicionar um pacote no gitignore. (Não inclui alterações em código)

ci - Commits do tipo ci indicam mudanças relacionadas a integração contínua (continuous integration).

raw - Commits do tipo raw indicam mudanças relacionadas a arquivos de configurações, dados, features, parâmetros.

cleanup - Commits do tipo cleanup são utilizados para remover código comentado, trechos desnecessários ou qualquer outra forma de limpeza do código-fonte, visando aprimorar sua legibilidade e manutenibilidade.

remove - Commits do tipo remove indicam a exclusão de arquivos, diretórios ou funcionalidades obsoletas ou não utilizadas, reduzindo o tamanho e a complexidade do projeto e mantendo-o mais organizado.