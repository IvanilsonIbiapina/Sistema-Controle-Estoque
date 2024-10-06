import sqlite3

class Banco():
    def __init__(self, bd="banco_de_dados.db") -> None:
        self.conexao = sqlite3.connect(bd)
        self.cursor = self.conexao.cursor()
