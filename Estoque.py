import sqlite3
from database import Banco

class Estoque(Banco):
    def __init__(self, bd="banco_de_dados.db") -> None:
        super().__init__(bd)
        self.criarTabela()

    def criarTabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fk_id_produto TEXT(20) NOT NULL,
                quantidade INT NOT NULL,
                FOREIGN KEY (fk_id_produto)
                    REFERENCES produtos (id)
            )
""")    
        self.conexao.commit()

    def adicionar_produto_ao_estoque(self):
        pass
    def remover_produto_do_estoque(self):
        pass
