# Sistema de Monitoramento Industrial

Backend completo em Python para monitoramento industrial com testes de estresse, observabilidade e monitoramento de desempenho.

##  Visão Geral

Sistema para monitoramento de sensores industriais com:
- API REST Flask para receber leituras de sensores
- Banco de dados SQLite para armazenamento
- Prometheus para coleta de métricas
- Grafana para visualização gráfica
- k6 para testes de carga

##  Arquitetura

```
k6 (Teste de Carga)
    ↓
Flask API (Backend)
    ↓
SQLite (Banco de Dados)

Prometheus (Coleta de Métricas)
    ↓
Grafana (Visualização)
```

## 🛠️ Tecnologias

- **Python 3.12+** - Linguagem de programação
- **Flask** - Framework Web para API REST
- **SQLite** - Banco de dados (built-in no Python)
- **Prometheus** - Sistema de monitoramento de métricas
- **Grafana** - Plataforma de visualização de métricas
- **k6** - Ferramenta de teste de carga
- **prometheus-client** - Cliente Python para Prometheus
- **python-dotenv** - Gerenciamento de variáveis de ambiente

##  O que é Prometheus?

**Prometheus** é um sistema de monitoramento de código aberto que coleta e armazena métricas como dados de séries temporais. Ele:

- Coleta métricas de aplicações via endpoints HTTP
- Armazena dados em formato de séries temporais
- Possui linguagem de consulta poderosa (PromQL)
- Alertas baseados em métricas
- Integração nativa com Grafana

**Neste sistema:** O Prometheus coleta métricas da API Flask a cada 15 segundos do endpoint `/metrics`.

##  O que é Grafana?

**Grafana** é uma plataforma de visualização e análise de métricas de código aberto. Ela:

- Cria dashboards interativos e bonitos
- Conecta-se a múltiplas fontes de dados (Prometheus, Elasticsearch, etc.)
- Permite criar alertas visuais
- Oferece visualizações em tempo real
- Suporta compartilhamento de dashboards

**Neste sistema:** O Grafana visualiza as métricas coletadas pelo Prometheus, mostrando gráficos de requisições, erros, tempo de resposta e leituras de sensores.

## Como Executar o Sistema

### Pré-requisitos

1. **Python 3.12+**
   - Download: https://www.python.org/downloads/
   - SQLite é built-in no Python

2. **Prometheus**
   - Baixado em: `C:\Users\wevertondonato\Downloads\prometheus-3.12.0.windows-amd64.zip`
   - Extraído em: `prometheus/prometheus-3.12.0.windows-amd64/`

3. **Grafana**
   - Instalado em: `C:\Program Files\GrafanaLabs\grafana\`
   - Configuração customizada em: `grafana-data/custom.ini`

### Passo 1: Instalar Dependências Python

```bash
cd backend
python -m pip install -r requirements.txt
```

### Passo 2: Inicializar Banco de Dados

```bash
cd backend
python database.py
```

**Saída esperada:**
```
2026-06-10 00:52:55,854 - __main__ - INFO - Tabela Equipamento criada/verificada
2026-06-10 00:52:55,854 - __main__ - INFO - Tabela LeituraSensor criada/verificada
2026-06-10 00:52:55,854 - __main__ - INFO - Banco de dados SQLite inicializado com sucesso: producao1.db
```

### Passo 3: Iniciar API Flask

```bash
cd backend
python app.py
```

**Saída esperada:**
```
2026-06-10 00:36:21,605 - database - INFO - Conexão com SQLite estabelecida: producao1.db
2026-06-10 00:36:21,607 - __main__ - INFO - Iniciando API Flask...
2026-06-10 00:36:21,607 - __main__ - INFO - Host: 0.0.0.0
2026-06-10 00:36:21,607 - __main__ - INFO - Port: 5000
2026-06-10 00:36:21,607 - __main__ - INFO - Debug: True
2026-06-10 00:36:21,613 - werkzeug - WARNING -  * Debugger is active!
2026-06-10 00:36:21,618 - werkzeug - INFO -  * Running on http://0.0.0.0:5000
```

**API disponível em:** `http://localhost:5000`

### Passo 4: Iniciar Prometheus

```bash
.\prometheus\prometheus-3.12.0.windows-amd64\prometheus.exe --config.file=backend\prometheus.yml
```

**Saída esperada:**
```
time=2026-06-10T01:17:01.960-03:00 level=INFO source=main.go:1708 msg="Starting Prometheus Server"
time=2026-06-10T01:17:02.037-03:00 level=INFO source=web.go:718 msg="Start listening for connections" component=web address=0.0.0.0:9090
```

**Prometheus disponível em:** `http://localhost:9090`

### Passo 5: Iniciar Grafana

```bash
& "C:\Program Files\GrafanaLabs\grafana\bin\grafana.exe" server --homepath="C:\Program Files\GrafanaLabs\grafana" --config="C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\custom.ini"
```

**Saída esperada:**
```
INFO [06-10|01:48:03] Starting Grafana logger=settings version=13.0.2
INFO [06-10|01:48:03] HTTP Server Listen logger=httpserver address=[::]:3000 protocol=http subUrl=/ socketPath=
```

**Grafana disponível em:** `http://localhost:3000`
- **Login:** `admin`
- **Senha:** `admin` (alterar no primeiro acesso)

##  Comandos de Teste

### Testar API Flask

**Verificar status da API:**
```bash
curl http://localhost:5000/health
```

**Resposta esperada:**
```json
{
  "database_connected": true,
  "status": "online"
}
```

**Verificar métricas Prometheus:**
```bash
curl http://localhost:5000/metrics
```

**Enviar leitura de sensor:**
```bash
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":75.5,\"pressao\":12.3,\"corrente\":15.8,\"voltagem\":220,\"status_leitura\":\"Normal\"}"
```

**Resposta esperada:**
```json
{
  "message": "Leitura inserida com sucesso",
  "id_leitura": 1
}
```

### Testar Prometheus

**Acessar interface web:**
```
http://localhost:9090
```

**Consultar métricas no Prometheus:**
- Acesse `http://localhost:9090/graph`
- Digite: `flask_app_requests_total`
- Clique em "Execute"

**Consultas úteis:**
```
flask_app_requests_total              # Total de requisições
flask_app_errors_total                # Total de erros
sensor_readings_total                 # Total de leituras de sensor
flask_app_request_duration_seconds_sum # Soma do tempo de resposta
```

### Testar Grafana

**Acessar interface web:**
```
http://localhost:3000
```

**Configurar Prometheus como Data Source:**
1. Vá em: Configuration → Data Sources → Add data source
2. Selecione "Prometheus"
3. Configure:
   - **URL**: `http://localhost:9090`
   - Clique em "Save & Test"

**Criar Dashboard:**
1. Create → Dashboard → Add visualization
2. Selecione "Prometheus"
3. Use as queries:
   - `rate(flask_app_requests_total[5m])` - Taxa de requisições por minuto
   - `rate(flask_app_request_duration_seconds_sum[5m]) / rate(flask_app_request_duration_seconds_count[5m])` - Tempo médio de resposta
   - `rate(flask_app_errors_total[5m])` - Taxa de erros
   - `rate(sensor_readings_total[5m])` - Taxa de leituras de sensor

### Testar com k6

**Executar teste de carga completo:**
```bash
k6 run backend/tests/teste.js
```

**Saída esperada:**
```
running (3m30.3s), 000/150 VUs, 166053 complete and 0 interrupted iterations
carga_leve   ✓ [======================================] 10 VUs   30s
carga_media  ✓ [======================================] 50 VUs   1m0s
carga_pesada ✓ [======================================] 100 VUs  2m0s
```

**Testes individuais:**

**Cenário 1 - Carga Leve (10 usuários, 30 segundos):**
```bash
k6 run --stage 30s:10 backend/tests/teste.js
```

**Cenário 2 - Carga Média (50 usuários, 1 minuto):**
```bash
k6 run --stage 60s:50 backend/tests/teste.js
```

**Cenário 3 - Carga Pesada (100 usuários, 2 minutos):**
```bash
k6 run --stage 120s:100 backend/tests/teste.js
```

##  Sugestões de Teste para Apresentação

### Teste 1: Demonstração Básica (5 minutos)

**Objetivo:** Mostrar o funcionamento básico do sistema

**Passos:**
1. Iniciar API Flask
2. Enviar 5 leituras de sensor manualmente via curl
3. Verificar dados no banco de dados
4. Mostrar métricas no Prometheus
5. Mostrar gráficos no Grafana

**Comandos:**
```bash
# 1. Iniciar API
cd backend
python app.py

# 2. Enviar leituras
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":75.5,\"pressao\":12.3,\"corrente\":15.8,\"voltagem\":220,\"status_leitura\":\"Normal\"}"
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":2,\"temperatura\":80.2,\"pressao\":15.1,\"corrente\":18.2,\"voltagem\":220,\"status_leitura\":\"Alerta\"}"
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":3,\"temperatura\":65.8,\"pressao\":10.5,\"corrente\":12.1,\"voltagem\":220,\"status_leitura\":\"Normal\"}"

# 3. Verificar banco de dados
python -c "import sqlite3; conn = sqlite3.connect('backend/producao1.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM LeituraSensor'); print(cursor.fetchall()); conn.close()"

# 4. Acessar Prometheus
# Abrir navegador em http://localhost:9090
# Consultar: flask_app_requests_total

# 5. Acessar Grafana
# Abrir navegador em http://localhost:3000
# Ver dashboard criado
```

### Teste 2: Teste de Carga Leve (2 minutos)

**Objetivo:** Mostrar o sistema sob carga moderada

**Passos:**
1. Iniciar todos os componentes (Flask, Prometheus, Grafana)
2. Executar teste k6 com 10 usuários por 30 segundos
3. Monitorar métricas em tempo real no Grafana
4. Mostrar gráficos de performance

**Comandos:**
```bash
# 1. Iniciar componentes (em terminais separados)
cd backend
python app.py

.\prometheus\prometheus-3.12.0.windows-amd64\prometheus.exe --config.file=backend\prometheus.yml

& "C:\Program Files\GrafanaLabs\grafana\bin\grafana.exe" server --homepath="C:\Program Files\GrafanaLabs\grafana" --config="C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\custom.ini"

# 2. Executar teste de carga
k6 run backend/tests/teste.js --stage 30s:10

# 3. Monitorar em tempo real
# Abrir http://localhost:3000
# Ver gráficos atualizando
```

### Teste 3: Teste de Carga Pesada (5 minutos)

**Objetivo:** Mostrar escalabilidade e performance

**Passos:**
1. Iniciar todos os componentes
2. Executar teste k6 completo (3 cenários)
3. Monitorar métricas durante o teste
4. Analisar resultados após o teste

**Comandos:**
```bash
# 1. Iniciar componentes (em terminais separados)
cd backend
python app.py

.\prometheus\prometheus-3.12.0.windows-amd64\prometheus.exe --config.file=backend\prometheus.yml

& "C:\Program Files\GrafanaLabs\grafana\bin\grafana.exe" server --homepath="C:\Program Files\GrafanaLabs\grafana" --config="C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\custom.ini"

# 2. Executar teste completo
k6 run backend/tests/teste.js

# 3. Monitorar durante o teste
# Abrir http://localhost:3000
# Ver gráficos de:
# - Taxa de requisições
# - Tempo de resposta
# - Taxa de erros
# - Leituras de sensor
```

### Teste 4: Demonstração de Observabilidade (3 minutos)

**Objetivo:** Mostrar poder de observabilidade com Prometheus + Grafana

**Passos:**
1. Iniciar todos os componentes
2. Enviar dados com diferentes status (Normal, Alerta, Falha)
3. Mostrar métricas específicas no Prometheus
4. Criar dashboard customizado no Grafana
5. Mostrar correlação entre métricas

**Comandos:**
```bash
# 1. Iniciar componentes
cd backend
python app.py

# 2. Enviar dados variados
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":75.5,\"pressao\":12.3,\"corrente\":15.8,\"voltagem\":220,\"status_leitura\":\"Normal\"}"
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":95.5,\"pressao\":18.3,\"corrente\":20.8,\"voltagem\":220,\"status_leitura\":\"Alerta\"}"
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":105.5,\"pressao\":22.3,\"corrente\":25.8,\"voltagem\":220,\"status_leitura\":\"Falha\"}"

# 3. Consultar Prometheus
# http://localhost:9090
# Consultas:
# - sensor_readings_total
# - flask_app_errors_total
# - rate(sensor_readings_total[5m])

# 4. Criar dashboard no Grafana
# http://localhost:3000
# Adicionar painéis para:
# - Leituras por status
# - Temperatura média
# - Taxa de erros
```

##  Estrutura do Projeto

```
S.A -Tester/
│
├── backend/
│   ├── app.py                 # Aplicação Flask principal
│   ├── database.py            # Conexão e operações SQLite
│   ├── config.py              # Configurações centralizadas
│   ├── requirements.txt       # Dependências Python
│   ├── .env                   # Variáveis de ambiente
│   ├── prometheus.yml         # Configuração Prometheus
│   ├── init_database.sql      # Script de inicialização do DB
│   ├── README.md              # Documentação do backend
│   └── tests/
│       └── teste.js           # Script de teste k6
│
├── grafana-data/              # Dados e configuração do Grafana
│   ├── custom.ini             # Configuração customizada
│   ├── grafana.db             # Banco de dados do Grafana
│   ├── logs/                  # Logs do Grafana
│   ├── plugins/               # Plugins do Grafana
│   └── provisioning/          # Provisioning do Grafana
│
├── prometheus/                # Executável do Prometheus
│   └── prometheus-3.12.0.windows-amd64/
│       └── prometheus.exe
│
├── producao1.db               # Banco de dados SQLite
└── README.md                  # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```bash
DB_PATH=producao1.db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
LOG_LEVEL=INFO
```

### Configuração Prometheus (prometheus.yml)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask_api'
    static_configs:
      - targets: ['localhost:5000']
```

### Configuração Grafana (grafana-data/custom.ini)

```ini
[server]
http_port = 3000

[paths]
data = C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data
logs = C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\logs
plugins = C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\plugins
provisioning = C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\provisioning

[database]
path = C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\grafana.db
```

##  Métricas Disponíveis

### Métricas da API Flask

- `flask_app_requests_total` - Total de requisições recebidas
- `flask_app_errors_total` - Total de erros ocorridos
- `flask_app_request_duration_seconds_sum` - Soma do tempo de resposta
- `flask_app_request_duration_seconds_count` - Contagem de requisições para cálculo de média
- `sensor_readings_total` - Total de leituras de sensor recebidas

### Consultas Prometheus Úteis

```promql
# Taxa de requisições por minuto
rate(flask_app_requests_total[5m])

# Tempo médio de resposta
rate(flask_app_request_duration_seconds_sum[5m]) / rate(flask_app_request_duration_seconds_count[5m])

# Taxa de erros
rate(flask_app_errors_total[5m])

# Taxa de leituras de sensor
rate(sensor_readings_total[5m])

# Percentil 95 do tempo de resposta
histogram_quantile(0.95, rate(flask_app_request_duration_seconds_bucket[5m]))
```

##  Troubleshooting

### Erro: Porta já em uso

**Problema:** A porta 5000, 9090 ou 3000 já está sendo usada.

**Solução:**
```bash
# Verificar processo usando a porta
Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess
Get-Process -Id <PID> | Stop-Process -Force
```

### Erro: Banco de dados não encontrado

**Problema:** O arquivo `producao1.db` não existe.

**Solução:**
```bash
cd backend
python database.py
```

### Erro: Grafana não inicia

**Problema:** Permissões no diretório de dados.

**Solução:** Use a configuração customizada em `grafana-data/custom.ini`.

### Erro: Prometheus não coleta métricas

**Problema:** API Flask não está rodando ou endpoint `/metrics` inacessível.

**Solução:**
```bash
# Verificar se API está rodando
curl http://localhost:5000/health

# Verificar endpoint de métricas
curl http://localhost:5000/metrics
```

##  Resumo de Comandos para Apresentação

### Inicialização Completa (3 terminais)

**Terminal 1 - API Flask:**
```bash
cd backend
python -m pip install -r requirements.txt
python database.py
python app.py
```

**Terminal 2 - Prometheus:**
```bash
.\prometheus\prometheus-3.12.0.windows-amd64\prometheus.exe --config.file=backend\prometheus.yml
```

**Terminal 3 - Grafana:**
```bash
& "C:\Program Files\GrafanaLabs\grafana\bin\grafana.exe" server --homepath="C:\Program Files\GrafanaLabs\grafana" --config="C:\Users\wevertondonato\OneDrive\Imagens\Capturas de tela\Área de Trabalho\S.A -Tester\grafana-data\custom.ini"
```

### Testes Rápidos

**Verificar saúde do sistema:**
```bash
curl http://localhost:5000/health
```

**Enviar dados de teste:**
```bash
curl -X POST http://localhost:5000/sensor -H "Content-Type: application/json" -d "{\"id_equipamento\":1,\"temperatura\":75.5,\"pressao\":12.3,\"corrente\":15.8,\"voltagem\":220,\"status_leitura\":\"Normal\"}"
```

**Executar teste de carga:**
```bash
k6 run backend/tests/teste.js
```

### Acessos Web

- **API Flask:** http://localhost:5000
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

##  Pontos Chave para Apresentação

1. **Arquitetura Moderna:** Flask + SQLite + Prometheus + Grafana
2. **Observabilidade:** Métricas em tempo real
3. **Escalabilidade:** Testes de carga com k6
4. **Simplicidade:** SQLite built-in, fácil instalação
5. **Visualização:** Dashboards interativos no Grafana
6. **Monitoramento:** Alertas e métricas detalhadas

##  Licença

Este projeto foi desenvolvido para fins de monitoramento industrial e testes de estresse.
