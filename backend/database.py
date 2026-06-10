"""
Módulo de Conexão com Banco de Dados
Gerencia conexões SQLite e inicialização do schema
"""

import sqlite3
import logging
from config import Config

# Configurar logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Database:
    """Classe para gerenciar conexões com o banco de dados SQLite"""
    
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """
        Estabelece conexão com o banco de dados SQLite
        
        Returns:
            bool: True se conexão foi bem-sucedida, False caso contrário
        """
        try:
            db_path = Config.get_db_path()
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
            
            logger.info(f"Conexão com SQLite estabelecida: {db_path}")
            return True
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao conectar ao SQLite: {e}")
            return False
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com SQLite fechada")
    
    def get_connection(self):
        """
        Retorna a conexão ativa
        
        Returns:
            sqlite3.Connection: Objeto de conexão SQLite
        """
        # Verifica se a conexão ainda está ativa
        if not self.connection:
            self.connect()
        return self.connection
    
    def insert_sensor_reading(self, id_equipamento, temperatura, pressao, 
                             corrente, voltagem, status_leitura):
        """
        Insere uma leitura de sensor no banco de dados
        
        Args:
            id_equipamento (int): ID do equipamento
            temperatura (float): Temperatura medida
            pressao (float): Pressão medida
            corrente (float): Corrente medida
            voltagem (float): Voltagem medida
            status_leitura (str): Status da leitura (Normal, Alerta, Falha)
            
        Returns:
            bool: True se inserção foi bem-sucedida, False caso contrário
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO LeituraSensor 
            (id_equipamento, temperatura, pressao, corrente, voltagem, status_leitura)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            values = (id_equipamento, temperatura, pressao, 
                     corrente, voltagem, status_leitura)
            
            cursor.execute(query, values)
            connection.commit()
            
            logger.info(f"Leitura inserida: Equipamento {id_equipamento}, "
                       f"Temp: {temperatura}°C, Status: {status_leitura}")
            
            cursor.close()
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Erro ao inserir leitura: {e}")
            if connection:
                connection.rollback()
            return False
    
    def get_equipment_status(self, id_equipamento):
        """
        Verifica o status de um equipamento
        
        Args:
            id_equipamento (int): ID do equipamento
            
        Returns:
            str: Status do equipamento ou None se não encontrado
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT status FROM Equipamento WHERE id_equipamento = ?"
            cursor.execute(query, (id_equipamento,))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result['status']
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar status do equipamento: {e}")
            return None


def initialize_database():
    """
    Inicializa o banco de dados criando as tabelas necessárias
    Esta função deve ser executada uma vez para configurar o banco de dados
    """
    try:
        db_path = Config.get_db_path()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Criar tabela Equipamento
        create_equipamento = """
        CREATE TABLE IF NOT EXISTS Equipamento (
            id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            setor TEXT,
            status TEXT CHECK(status IN ('Ativo', 'Inativo'))
        )
        """
        cursor.execute(create_equipamento)
        logger.info("Tabela Equipamento criada/verificada")
        
        # Criar tabela LeituraSensor
        create_leitura = """
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
        )
        """
        cursor.execute(create_leitura)
        logger.info("Tabela LeituraSensor criada/verificada")
        
        # Inserir equipamentos de exemplo se não existirem
        check_equipamentos = "SELECT COUNT(*) as count FROM Equipamento"
        cursor.execute(check_equipamentos)
        count = cursor.fetchone()[0]
        
        if count == 0:
            insert_equipamentos = """
            INSERT INTO Equipamento(nome, setor, status)
            VALUES
            ('Transformador T1', 'Produção', 'Ativo'),
            ('Transformador T2', 'Produção', 'Ativo'),
            ('Painel P1', 'Montagem', 'Ativo')
            """
            cursor.execute(insert_equipamentos)
            connection.commit()
            logger.info("Equipamentos de exemplo inseridos")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info(f"Banco de dados SQLite inicializado com sucesso: {db_path}")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        return False


if __name__ == "__main__":
    # Executar inicialização do banco de dados
    initialize_database()
