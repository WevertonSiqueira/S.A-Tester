-- Script de Inicialização do Banco de Dados
-- Sistema de Monitoramento Industrial
-- SQLite

-- Criar tabela Equipamento
CREATE TABLE IF NOT EXISTS Equipamento (
    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    setor TEXT,
    status TEXT CHECK(status IN ('Ativo', 'Inativo'))
);

-- Criar tabela LeituraSensor
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

-- Inserir equipamentos de exemplo (apenas se não existirem)
INSERT OR IGNORE INTO Equipamento(nome, setor, status)
VALUES
('Transformador T1', 'Produção', 'Ativo'),
('Transformador T2', 'Produção', 'Ativo'),
('Painel P1', 'Montagem', 'Ativo');

-- Criar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_leitura_equipamento ON LeituraSensor(id_equipamento);
CREATE INDEX IF NOT EXISTS idx_leitura_data_hora ON LeituraSensor(data_hora);
CREATE INDEX IF NOT EXISTS idx_leitura_status ON LeituraSensor(status_leitura);

-- Exibir estrutura das tabelas
SELECT 'Tabela Equipamento criada com sucesso' AS mensagem;
.schema Equipamento

SELECT 'Tabela LeituraSensor criada com sucesso' AS mensagem;
.schema LeituraSensor

SELECT 'Equipamentos inseridos:' AS mensagem;
SELECT * FROM Equipamento;
