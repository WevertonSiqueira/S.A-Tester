# Sistema de Monitoramento Industrial

## Tecnologias Utilizadas

### Python
Linguagem utilizada no desenvolvimento do backend da aplicação, responsável pelo processamento das requisições, comunicação com o banco de dados e disponibilização da API.

### Flask
Framework utilizado para desenvolver a API REST responsável por receber, processar e disponibilizar os dados dos sensores industriais.

### SQLite
Banco de dados relacional utilizado para armazenar as informações dos equipamentos e das leituras realizadas pelos sensores.

### Prometheus
Ferramenta responsável pela coleta e armazenamento das métricas da aplicação, permitindo acompanhar o desempenho do sistema em tempo real.

### Grafana
Plataforma utilizada para visualizar as métricas coletadas pelo Prometheus através de dashboards, gráficos e indicadores.

### k6
Ferramenta de testes de carga utilizada para simular múltiplos usuários realizando requisições simultaneamente à API, permitindo avaliar o desempenho do sistema.

---

# Ferramentas Utilizadas

| Ferramenta | Finalidade |
|------------|------------|
| Python 3.12 | Desenvolvimento do backend |
| Flask | Criação da API REST |
| SQLite | Armazenamento dos dados |
| Prometheus | Coleta de métricas |
| Grafana | Visualização das métricas |
| k6 | Testes de carga e desempenho |
| VS Code | Desenvolvimento do projeto |
| Git | Controle de versão |

---

# Plano de Testes

O plano de testes foi elaborado para verificar o funcionamento da aplicação, garantir a integridade dos dados e avaliar o desempenho do sistema sob diferentes níveis de carga.

## Objetivos

- Validar o funcionamento da API.
- Verificar o armazenamento correto das informações no banco de dados.
- Monitorar métricas de desempenho utilizando Prometheus.
- Visualizar indicadores em tempo real no Grafana.
- Avaliar a capacidade da aplicação sob diferentes volumes de requisições.

## Ambiente de Testes

- Sistema Operacional: Windows
- Linguagem: Python 3.12
- Banco de Dados: SQLite
- API: Flask
- Monitoramento: Prometheus
- Dashboard: Grafana
- Testes de carga: k6

---

# Testes Realizados

## 1. Teste da API

Objetivo:

Verificar se a API recebe corretamente requisições HTTP e retorna respostas válidas.

Resultado esperado:

- API disponível.
- Recebimento correto dos dados.
- Inserção das informações no banco de dados.

---

## 2. Teste do Banco de Dados

Objetivo:

Validar o armazenamento das leituras dos sensores.

Resultado esperado:

- Dados gravados corretamente no SQLite.
- Integridade das informações armazenadas.

---

## 3. Teste de Monitoramento

Objetivo:

Verificar se o Prometheus coleta corretamente as métricas disponibilizadas pela aplicação.

Resultado esperado:

- Coleta contínua das métricas.
- Atualização automática dos indicadores.

---

## 4. Teste de Visualização

Objetivo:

Validar a exibição das métricas no Grafana.

Resultado esperado:

- Dashboards funcionando corretamente.
- Atualização em tempo real dos gráficos.

---

## 5. Teste de Carga

Os testes de carga foram realizados utilizando o k6 para avaliar o comportamento da aplicação em diferentes cenários.

### Cenário 1 – Carga Leve

- 10 usuários virtuais
- Duração: 30 segundos

Objetivo:

Avaliar o funcionamento da aplicação sob baixa carga.

---

### Cenário 2 – Carga Média

- 50 usuários virtuais
- Duração: 1 minuto

Objetivo:

Verificar a estabilidade da aplicação durante uma quantidade moderada de acessos simultâneos.

---

### Cenário 3 – Carga Pesada

- 100 usuários virtuais
- Duração: 2 minutos

Objetivo:

Avaliar o desempenho da API sob alta demanda e verificar possíveis perdas de desempenho ou aumento do tempo de resposta.

---

# Resultados Esperados

Durante os testes espera-se observar:

- API respondendo corretamente às requisições.
- Armazenamento consistente das informações.
- Coleta contínua das métricas pelo Prometheus.
- Visualização em tempo real dos indicadores no Grafana.
- Estabilidade da aplicação mesmo sob múltiplos acessos simultâneos.

---

# Conclusão

Os testes realizados permitiram validar o funcionamento da aplicação em relação às funcionalidades principais, armazenamento dos dados, monitoramento e desempenho. A utilização conjunta do Flask, SQLite, Prometheus, Grafana e k6 possibilitou analisar tanto o comportamento funcional quanto a capacidade da aplicação de suportar diferentes níveis de carga, fornecendo indicadores importantes para sua avaliação.
