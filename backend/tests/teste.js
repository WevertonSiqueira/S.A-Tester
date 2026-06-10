// Script de Teste de Carga com k6
// Sistema de Monitoramento Industrial
// Testa a API Flask com diferentes cenários de carga

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Configuração de métricas personalizadas
const errorRate = new Rate('errors');

// Configuração base da API
const BASE_URL = 'http://localhost:5000';

// Função para gerar dados aleatórios de sensor
function generateSensorData() {
    const equipmentIds = [1, 2, 3]; // IDs dos equipamentos disponíveis
    const statuses = ['Normal', 'Alerta', 'Falha'];
    
    // Gerar valores aleatórios realistas
    const temperatura = (Math.random() * 100 + 20).toFixed(1); // 20-120°C
    const pressao = (Math.random() * 20 + 5).toFixed(1); // 5-25 bar
    const corrente = (Math.random() * 30 + 5).toFixed(1); // 5-35 A
    const voltagem = (Math.random() * 20 + 210).toFixed(0); // 210-230 V
    
    // Status baseado na temperatura (simulação realista)
    let status = 'Normal';
    if (parseFloat(temperatura) > 90) {
        status = 'Falha';
    } else if (parseFloat(temperatura) > 80) {
        status = 'Alerta';
    }
    
    return {
        id_equipamento: equipmentIds[Math.floor(Math.random() * equipmentIds.length)],
        temperatura: parseFloat(temperatura),
        pressao: parseFloat(pressao),
        corrente: parseFloat(corrente),
        voltagem: parseInt(voltagem),
        status_leitura: status
    };
}

// Função para enviar leitura de sensor
function sendSensorReading() {
    const payload = JSON.stringify(generateSensorData());
    
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const response = http.post(`${BASE_URL}/sensor`, payload, params);
    
    // Verificar se a requisição foi bem-sucedida
    const success = check(response, {
        'status é 201': (r) => r.status === 201,
        'resposta tem status success': (r) => r.json('status') === 'success',
        'tempo de resposta < 500ms': (r) => r.timings.duration < 500,
    });
    
    errorRate.add(!success);
    
    return response;
}

// Função para verificar saúde da API
function checkHealth() {
    const response = http.get(`${BASE_URL}/health`);
    
    const success = check(response, {
        'status é 200': (r) => r.status === 200,
        'status é online': (r) => r.json('status') === 'online',
    });
    
    errorRate.add(!success);
    
    return response;
}

// Configuração dos cenários de teste
export const options = {
    scenarios: {
        // Cenário 1: Carga leve - 10 usuários por 30 segundos
        carga_leve: {
            executor: 'constant-vus',
            vus: 10,
            duration: '30s',
            exec: 'cargaLeve',
            startTime: '0s',
        },
        
        // Cenário 2: Carga média - 50 usuários por 1 minuto
        carga_media: {
            executor: 'constant-vus',
            vus: 50,
            duration: '1m',
            exec: 'cargaMedia',
            startTime: '30s',
        },
        
        // Cenário 3: Carga pesada - 100 usuários por 2 minutos
        carga_pesada: {
            executor: 'constant-vus',
            vus: 100,
            duration: '2m',
            exec: 'cargaPesada',
            startTime: '90s',
        },
    },
    
    // Limites de desempenho (thresholds)
    thresholds: {
        http_req_duration: ['p(95)<500', 'p(99)<1000'], // 95% das requisições < 500ms
        http_req_failed: ['rate<0.01'], // Taxa de erro < 1%
        errors: ['rate<0.01'], // Taxa de erros customizados < 1%
    },
};

// Cenário 1: Carga leve
export function cargaLeve() {
    // Verificar saúde a cada 10 requisições
    if (__ITER % 10 === 0) {
        checkHealth();
    }
    
    sendSensorReading();
    sleep(1); // Pausa de 1 segundo entre requisições
}

// Cenário 2: Carga média
export function cargaMedia() {
    // Verificar saúde a cada 20 requisições
    if (__ITER % 20 === 0) {
        checkHealth();
    }
    
    sendSensorReading();
    sleep(0.5); // Pausa de 0.5 segundo entre requisições
}

// Cenário 3: Carga pesada
export function cargaPesada() {
    // Verificar saúde a cada 50 requisições
    if (__ITER % 50 === 0) {
        checkHealth();
    }
    
    sendSensorReading();
    sleep(0.2); // Pausa de 0.2 segundo entre requisições
}
