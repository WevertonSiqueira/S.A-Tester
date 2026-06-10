# Sistema de Monitoramento Industrial

Backend completo em Python para monitoramento industrial com testes de estresse, observabilidade e monitoramento de desempenho.

## Arquitetura

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

## Tecnologias

- **Python 3.12+**
- **Flask** - Framework Web
- **sqlite3** - Banco de dados SQLite (built-in no Python)
- **prometheus-client** - Métricas Prometheus
- **python-dotenv** - Variáveis de ambiente
- **Prometheus** - Monitoramento de métricas
- **Grafana** - Visualização de métricas
- **k6** - Teste de carga

## Estrutura do Projeto

```
backend/
│
├── app.py                 # Aplicação Flask principal
├── database.py            # Conexão e operações SQLite
├── config.py              # Configurações centralizadas
├── requirements.txt       # Dependências Python
├── .env                   # Variáveis de ambiente
├── prometheus.yml         # Configuração Prometheus
├── init_database.sql      # Script de inicialização do DB
├── README.md              # Este arquivo
└── tests/
    └── teste.js           # Script de teste k6
```

## Pré-requisitos

1. **Python 3.12+**
   - Download: https://www.python.org/downloads/
   - SQLite é built-in no Python, não requer instalação adicional

2. **Prometheus**
   - Download: https://prometheus.io/download/
   - Extrair e executar `prometheus.exe`

3. **Grafana**
   - Download: https://grafana.com/grafana/download
   - Instalar e iniciar o serviço

4. **k6**
   - Download: https://k6.io/docs/getting-started/installation/
   - Para Windows: `choco install k6` ou baixar o binário

## Instalação

### 1. Configurar Banco de Dados SQLite

O banco de dados SQLite será criado automaticamente ao executar a aplicação. Para inicializar manualmente:

```bash
python database.py
```

Ou execute o script SQL usando sqlite3:

```bash
sqlite3 producao1.db < init_database.sql
```

Ou execute manualmente usando sqlite3:

```bash
sqlite3 producao1.db
```

```sql
CREATE TABLE IF NOT EXISTS Equipamento (
    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    setor TEXT,
    status TEXT CHECK(status IN ('Ativo', 'Inativo'))
);

CREATE TABLE IF NOT EXISTS LeituraSensor (
    id_leitura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipamento INTEGER NOT NULL,
    temperatura REAL,
    pressao REAL,
    corrente REAL,
    voltagem REAL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_leitura TEXT CHECK(status_leitura IN ('Normal', 'Alerta', 'Falha')),
    FOREIGN KEY (id_equipamento)
    REFERENCES Equipamento(id_equipamento)
);

INSERT OR IGNORE INTO Equipamento(nome, setor, status)
VALUES
('Transformador T1', 'Produção', 'Ativo'),
('Transformador T2', 'Produção', 'Ativo'),
('Painel P1', 'Montagem', 'Ativo');
```

### 2. Instalar Dependências Python

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado com:

```
DB_PATH=producao1.db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
LOG_LEVEL=INFO
```

## Execução

### Iniciar a API Flask

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

### Inicializar Banco de Dados (opcional)

Se preferir inicializar via Python:

```bash
python database.py
```

### Iniciar Prometheus

```bash
# No diretório do Prometheus
prometheus.exe --config.file=prometheus.yml
```

Copie o arquivo `prometheus.yml` para o diretório do Prometheus ou configure o caminho correto.

### Iniciar Grafana

```bash
# Windows Service
net start grafana

# Ou executável
grafana-server.exe
```

Acesse Grafana em: `http://localhost:3000`
- Usuário padrão: `admin`
- Senha padrão: `admin`

### Configurar Grafana

1. Adicionar datasource Prometheus:
   - Settings → Data Sources → Add data source
   - Selecionar Prometheus
   - URL: `http://localhost:9090`
   - Save & Test

2. Criar dashboard:
   - Create → Dashboard
   - Adicionar panels com as métricas disponíveis

## API Endpoints

### POST /sensor

Recebe leituras de sensores industriais.

**Payload:**
```json
{
    "id_equipamento": 1,
    "temperatura": 75.5,
    "pressao": 12.3,
    "corrente": 15.8,
    "voltagem": 220,
    "status_leitura": "Normal"
}
```

**Resposta (201):**
```json
{
    "status": "success",
    "message": "Leitura recebida e armazenada",
    "id_equipamento": 1,
    "temperatura": 75.5,
    "status_leitura": "Normal"
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/sensor \
  -H "Content-Type: application/json" \
  -d "{\"id_equipamento\":1,\"temperatura\":75.5,\"pressao\":12.3,\"corrente\":15.8,\"voltagem\":220,\"status_leitura\":\"Normal\"}"
```

### GET /health

Verifica o status da API e conexão com banco de dados.

**Resposta (200):**
```json
{
    "status": "online",
    "database_connected": true
}
```

**Exemplo cURL:**
```bash
curl http://localhost:5000/health
```

### GET /metrics

Expõe métricas no formato Prometheus.

**Exemplo cURL:**
```bash
curl http://localhost:5000/metrics
```

## Métricas Prometheus

A API expõe as seguintes métricas:

- `flask_app_requests_total` - Total de requisições por método, endpoint e status
- `sensor_readings_total` - Total de leituras de sensor recebidas
- `flask_app_request_duration_seconds` - Tempo de resposta das requisições
- `flask_app_errors_total` - Total de erros por tipo

## Teste de Carga com k6

### Executar todos os cenários

```bash
k6 run tests/teste.js
```

### Cenários de Teste

**Cenário 1 - Carga Leve:**
- 10 usuários simultâneos
- Duração: 30 segundos
- Pausa: 1 segundo entre requisições

**Cenário 2 - Carga Média:**
- 50 usuários simultâneos
- Duração: 1 minuto
- Pausa: 0.5 segundo entre requisições

**Cenário 3 - Carga Pesada:**
- 100 usuários simultâneos
- Duração: 2 minutos
- Pausa: 0.2 segundo entre requisições

### Thresholds

- 95% das requisições < 500ms
- 99% das requisições < 1000ms
- Taxa de erro < 1%

## Logs

A API registra logs no console com nível INFO por padrão. Logs incluem:
- Requisições recebidas
- Respostas enviadas
- Erros e exceções
- Inserções no banco de dados

## Troubleshooting

### Erro de conexão SQLite

O arquivo do banco de dados será criado automaticamente na primeira execução. Verifique se o diretório tem permissões de escrita.

### Erro de porta em uso

Mude a porta no `.env`:
```
FLASK_PORT=5001
```

### Prometheus não coleta métricas

Verifique se a API está rodando e se o `prometheus.yml` está configurado corretamente:
```yaml
scrape_configs:
  - job_name: 'flask-api'
    static_configs:
      - targets: ['localhost:5000']
```

### k6 não conecta

Verifique se a API está rodando antes de executar os testes:
```bash
curl http://localhost:5000/health
```

## Monitoramento com Grafana

Sugestão de queries para dashboards:

**Total de Requisições:**
```
rate(flask_app_requests_total[5m])
```

**Tempo de Resposta:**
```
rate(flask_app_request_duration_seconds_sum[5m]) / rate(flask_app_request_duration_seconds_count[5m])
```

**Taxa de Erros:**
```
rate(flask_app_errors_total[5m])
```

**Leituras de Sensor:**
```
rate(sensor_readings_total[5m])
```

## Segurança

⚠️ **Atenção:** Este é um ambiente de desenvolvimento. Para produção:
- Use HTTPS
- Implemente autenticação e autorização
- Valide e sanitize todos os inputs
- Use secrets management para credenciais
- Implemente rate limiting
- Configure firewall adequado

## Licença

Este projeto foi desenvolvido para fins de monitoramento industrial e testes de estresse.
