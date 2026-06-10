"""
Aplicação Flask - Sistema de Monitoramento Industrial
API REST para receber leituras de sensores industriais
"""

from flask import Flask, request, jsonify
import time
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from werkzeug.serving import WSGIRequestHandler
from database import Database
from config import Config

# Configurar logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação Flask
app = Flask(__name__)

# Inicializar banco de dados
db = Database()

# Métricas Prometheus
# Total de requisições recebidas
REQUEST_COUNT = Counter(
    'flask_app_requests_total',
    'Total de requisições recebidas pela API',
    ['method', 'endpoint', 'status']
)

# Total de leituras de sensor recebidas
SENSOR_READINGS_COUNT = Counter(
    'sensor_readings_total',
    'Total de leituras de sensor recebidas'
)

# Tempo de resposta das requisições
REQUEST_DURATION = Histogram(
    'flask_app_request_duration_seconds',
    'Tempo de resposta das requisições em segundos',
    ['method', 'endpoint']
)

# Total de erros
ERROR_COUNT = Counter(
    'flask_app_errors_total',
    'Total de erros ocorridos na API',
    ['error_type']
)


# Middleware para logging de requisições
@app.before_request
def log_request_info():
    """Registra informações da requisição antes de processar"""
    logger.info(f"Requisição recebida: {request.method} {request.path}")


# Middleware para métricas de requisições
@app.after_request
def track_request_metrics(response):
    """
    Registra métricas Prometheus após processar a requisição
    """
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    
    logger.info(f"Resposta enviada: {response.status_code}")
    return response


@app.route('/sensor', methods=['POST'])
def receive_sensor_reading():
    """
    Endpoint para receber leituras de sensores industriais
    
    Payload esperado:
    {
        "id_equipamento": 1,
        "temperatura": 75.5,
        "pressao": 12.3,
        "corrente": 15.8,
        "voltagem": 220,
        "status_leitura": "Normal"
    }
    
    Returns:
        JSON: Confirmação da inserção ou erro
    """
    start_time = time.time()
    
    try:
        # Validar se o payload é JSON
        if not request.is_json:
            logger.warning("Requisição sem JSON")
            ERROR_COUNT.labels(error_type='invalid_content_type').inc()
            return jsonify({
                'error': 'Content-Type deve ser application/json'
            }), 400
        
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = [
            'id_equipamento', 'temperatura', 'pressao', 
            'corrente', 'voltagem', 'status_leitura'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.warning(f"Campos obrigatórios faltando: {missing_fields}")
            ERROR_COUNT.labels(error_type='missing_fields').inc()
            return jsonify({
                'error': f'Campos obrigatórios faltando: {missing_fields}'
            }), 400
        
        # Extrair dados
        id_equipamento = data['id_equipamento']
        temperatura = float(data['temperatura'])
        pressao = float(data['pressao'])
        corrente = float(data['corrente'])
        voltagem = float(data['voltagem'])
        status_leitura = data['status_leitura']
        
        # Validar status_leitura
        valid_statuses = ['Normal', 'Alerta', 'Falha']
        if status_leitura not in valid_statuses:
            logger.warning(f"Status inválido: {status_leitura}")
            ERROR_COUNT.labels(error_type='invalid_status').inc()
            return jsonify({
                'error': f'Status deve ser um de: {valid_statuses}'
            }), 400
        
        # Verificar se equipamento existe e está ativo
        equipment_status = db.get_equipment_status(id_equipamento)
        if equipment_status is None:
            logger.warning(f"Equipamento {id_equipamento} não encontrado")
            ERROR_COUNT.labels(error_type='equipment_not_found').inc()
            return jsonify({
                'error': f'Equipamento {id_equipamento} não encontrado'
            }), 404
        
        if equipment_status != 'Ativo':
            logger.warning(f"Equipamento {id_equipamento} está inativo")
            ERROR_COUNT.labels(error_type='equipment_inactive').inc()
            return jsonify({
                'error': f'Equipamento {id_equipamento} está inativo'
            }), 400
        
        # Inserir leitura no banco de dados
        success = db.insert_sensor_reading(
            id_equipamento, temperatura, pressao, 
            corrente, voltagem, status_leitura
        )
        
        if success:
            SENSOR_READINGS_COUNT.inc()
            logger.info(f"Leitura recebida com sucesso: Equipamento {id_equipamento}")
            
            # Registrar tempo de resposta
            REQUEST_DURATION.labels(
                method='POST',
                endpoint='/sensor'
            ).observe(time.time() - start_time)
            
            return jsonify({
                'status': 'success',
                'message': 'Leitura recebida e armazenada',
                'id_equipamento': id_equipamento,
                'temperatura': temperatura,
                'status_leitura': status_leitura
            }), 201
        else:
            ERROR_COUNT.labels(error_type='database_error').inc()
            return jsonify({
                'error': 'Erro ao armazenar leitura no banco de dados'
            }), 500
            
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        ERROR_COUNT.labels(error_type='validation_error').inc()
        return jsonify({
            'error': f'Erro de validação: {str(e)}'
        }), 400
        
    except Exception as e:
        logger.error(f"Erro não esperado: {e}")
        ERROR_COUNT.labels(error_type='unexpected_error').inc()
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde da API
    
    Returns:
        JSON: Status da API
    """
    start_time = time.time()
    
    try:
        # Verificar conexão com banco de dados
        connection = db.get_connection()
        db_connected = connection is not None
        
        status = 'online' if db_connected else 'degraded'
        
        # Registrar tempo de resposta
        REQUEST_DURATION.labels(
            method='GET',
            endpoint='/health'
        ).observe(time.time() - start_time)
        
        logger.info(f"Health check: {status}")
        
        return jsonify({
            'status': status,
            'database_connected': db_connected
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        ERROR_COUNT.labels(error_type='health_check_error').inc()
        return jsonify({
            'status': 'offline',
            'error': str(e)
        }), 503


@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Endpoint para expor métricas no formato Prometheus
    
    Returns:
        str: Métricas em formato Prometheus
    """
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    ERROR_COUNT.labels(error_type='not_found').inc()
    logger.warning(f"Rota não encontrada: {request.path}")
    return jsonify({
        'error': 'Rota não encontrada'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handler para métodos não permitidos"""
    ERROR_COUNT.labels(error_type='method_not_allowed').inc()
    logger.warning(f"Método não permitido: {request.method} {request.path}")
    return jsonify({
        'error': 'Método não permitido'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos do servidor"""
    ERROR_COUNT.labels(error_type='internal_error').inc()
    logger.error(f"Erro interno: {error}")
    return jsonify({
        'error': 'Erro interno do servidor'
    }), 500


def main():
    """Função principal para executar a aplicação"""
    # Configurar logging do WSGI para não duplicar logs
    WSGIRequestHandler.log = lambda self, format, *args: None
    
    logger.info("Iniciando API Flask...")
    logger.info(f"Host: {Config.FLASK_HOST}")
    logger.info(f"Port: {Config.FLASK_PORT}")
    logger.info(f"Debug: {Config.FLASK_DEBUG}")
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )


if __name__ == '__main__':
    main()
