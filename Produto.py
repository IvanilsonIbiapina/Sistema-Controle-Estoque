import sqlite3
from database import Banco

class Produto(Banco):
    def __init__(self,  bd="banco_de_dados.db") -> None:
        super().__init__(bd)
        self.criarTabela()

    def criarTabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT(20) NOT NULL,
                nome TEXT(20) NOT NULL,
                preco_custo REAL NOT NULL,
                preco_de_venda REAL NOT NULL
            )
""")    
        self.conexao.commit()

    def cadastrarProduto(self, categoria, nomeProduto, precoCusto, precoVenda):
        try:
            # Insere no banco de dados
            self.cursor.execute("""
                INSERT INTO produtos (categoria, nome, preco_custo, preco_de_venda) 
                VALUES (?, ?, ?, ?)
            """, (categoria, nomeProduto, precoCusto, precoVenda))
            # Salva a inserção
            self.conexao.commit()
            return f"Operação realizada com sucesso, {nomeProduto} foi cadastrado com sucesso."
        # Erro de sql
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao realizar a operação: {e}"
      
    def deletarProduto(self, nomeProduto):
        try:
            # 
            self.cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nomeProduto,))
            resultado = self.cursor.fetchone()
        
            if resultado is None:
                return f"O produto {nomeProduto} não foi encontrado."
            self.cursor.execute("""
                DELETE FROM produtos WHERE nome = ?
""", (nomeProduto, ))
            self.conexao.commit()
            return f"Operação realizada com sucesso, {nomeProduto} foi deletado"  
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao realizar a operação: {e}"
        
    def atualizarProduto(self, nomeProduto):
        escolha = input("Deseja alterar uma ou todas as informações do produto? \n 1 - para uma alteração \n 2 - para alterar todas \n")

        if escolha == '1':
            colunas_validas = ['categoria', 'nome', 'preco_custo', 'preco_de_venda']
            alteração = input("O que deseja alterar:\n categoria \n nome, \n preco_custo \n preco_de_venda \n").lower()
            update = input("Digite a nova informação que irá substiruir a atual: ").lower()
            if alteração in colunas_validas:
                try:
                    self.cursor.execute(f"""
                        UPDATE produtos SET {alteração} = ? WHERE nome = ?
""", (update, nomeProduto))        
                    self.conexao.commit()
                    return "Operação realizada com sucesso."
                except Exception as e:
                    print(f"Erro ao realizar a operação: {e}")
            else:
                print("Coluna inválida")
            
        elif escolha == '2':
            elementos = ['categoria', 'nome', 'precoCusto', 'precoVenda']
            alteracoes = []
            for elemento in elementos:
                alt = input(f"Digite a alteração de {elemento}: ")
                alteracoes.append(alt)
            
            try: 
                self.cursor.execute(f"""
                    UPDATE produtos 
                    SET categoria = ?, nome = ?, preco_custo = ?, preco_de_venda = ?
                    WHERE nome = ?
""", (*alteracoes, nomeProduto))
                self.conexao.commit()
            except Exception as e:
                print(f"Erro ao realizar a operação: {e}")
        else:
            print("Opção inválida, tente novamente.")

    def listarProdutos(self):
        try:
            self.cursor.execute("SELECT * FROM produtos")
            resultado = self.cursor.fetchall()
            
            if not resultado:
                return "Nenhum produto encontrado."
            
            for produto in resultado:
                id_produto, categoria_produto, nome_produto, preco_custo, preco_venda = produto
                print(f"\nID: {id_produto}, \nCategoria: {categoria_produto}, \nNome: {nome_produto}, \nPreço de Custo: {preco_custo}, \nPreço de Venda: {preco_venda}\n")
            
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao listar os produtos: {e}"

    def consultarProduto(self, nomeProduto):
        try: 
            self.cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nomeProduto,))
            resultado = self.cursor.fetchone()
            # verificar se existe no banco de dados
            if resultado is None:
                print(f"O produto {nomeProduto} não foi encontrado.")
            else:
                id_produto, categoria_produto, nome_produto, preco_custo, preco_venda = resultado
                print(f"\nID: {id_produto}, \nCategoria: {categoria_produto}, \nNome: {nome_produto}, \nPreço de Custo: {preco_custo}, \nPreço de Venda: {preco_venda}\n")
        # Erro de sql
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao realizar a operação: {e}"