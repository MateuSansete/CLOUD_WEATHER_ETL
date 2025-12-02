import pandas as pd
import requests
import os
from dotenv import load_dotenv



from google.cloud import storage
from google.cloud import bigquery

# Nota: Em Cloud Functions, load_dotenv() não é usado, mas é essencial para testes locais.
load_dotenv()

# --- 1. CONFIGURAÇÕES GLOBAIS ---
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?" 
OUTPUT_PATH_LOCAL = 'data/raw/weather_data_latest.parquet'

# Locais para monitoramento (use os mesmos do seu AGRO_ETL)
LOCATIONS = [
    {"city": "Sao Paulo", "country": "BR"},
    {"city": "Minas Gerais", "country": "BR"},
    {"city": "Rio Grande do Sul", "country": "BR"}
]

#  Estrutura de Cloud Function

# A Cloud Function espera um argumento 'request' (embora não o usemos aqui)
def run_weather_etl(request=None):
    """Executa a extração, transformação e salva os dados climaticos em Parquet."""
    
    # 2.1. Extração (E)
    raw_data_list = []
    print("Iniciando Extração de Dados Climáticos via API...")
    
    for loc in LOCATIONS:
        city = loc['city']
        country = loc['country']
        
        url = f"{BASE_URL}q={city},{country}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            
            # Extração de campos relevantes
            record = {
                'city': city,
                'country': country,
                'current_temp_c': data['main']['temp'],
                'humidity_percent': data['main']['humidity'],
                'weather_description': data['weather'][0]['description'],
                'extraction_date': pd.Timestamp.now()
            }
            raw_data_list.append(record)
            print(f"  -> Dados de {city} coletados com sucesso.")
            
        except requests.exceptions.RequestException as e:
            print(f"  -> ERRO: Falha ao extrair dados de {city}: {e}")
            
    if not raw_data_list:
        print("Nenhum dado extraído. Encerrando.")
        return 'Nenhum dado processado', 200

    # 2.2. Transformação (T)
    df = pd.DataFrame(raw_data_list)
    print(f"Dados brutos carregados no DataFrame: {len(df)} registros.")
    
    # Exemplo T1: Garantir tipos de dados numéricos
    df['current_temp_c'] = pd.to_numeric(df['current_temp_c'])
    
    # 2.3. Output Local (Para teste da Fase 1)
    
    # Garante que a pasta existe antes de salvar
    os.makedirs(os.path.dirname(OUTPUT_PATH_LOCAL), exist_ok=True) 
    
    df.to_parquet(OUTPUT_PATH_LOCAL, index=False)
    print(f"\n--- SUCESSO! Arquivo Parquet salvo localmente em: {OUTPUT_PATH_LOCAL} ---")
    
    return 'Processamento ETL local concluído com sucesso!', 200





# adicioando novas funções 


def upload_to_gcs(bucket_name, source_file_name)
    



if __name__ == "__main__":
    print("Iniciando teste local...")
    run_weather_etl()    