"""
Módulo de Configuração
Carrega variáveis de ambiente e fornece configurações centralizadas
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    """Classe de configuração centralizada"""
    
    # Configurações do Banco de Dados SQLite
    DB_PATH = os.getenv('DB_PATH', 'producao1.db')
    
    # Configurações do Flask
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configurações de Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_db_path(cls):
        """
        Retorna o caminho do arquivo SQLite
        
        Returns:
            str: Caminho do banco de dados SQLite
        """
        return cls.DB_PATH
