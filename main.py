import sqlite3
import asyncio
import os

class Banco():
    def __init__(self, bd="estoque.db") -> None:
        self.conexao = sqlite3.connect(bd)
        self.cursor = self.conexao.cursor()


class Produto(Banco):
    def __init__(self,  bd="estoque.db") -> None:
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
            self.cursor.execute("""
                INSERT INTO produtos (categoria, nome, preco_custo, preco_de_venda) 
                VALUES (?, ?, ?, ?)
            """, (categoria, nomeProduto, precoCusto, precoVenda))
            
            self.conexao.commit()
            return f"Operação realizada com sucesso, {nomeProduto} foi cadastrado com sucesso."
        
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao realizar a operação: {e}"
      
    def deletarProduto(self, nomeProduto):
        try:
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
        escolha = input("Deseja alterar uma ou todas as informações do produto? \n 1 para uma alteração \n 2 para alterar todas")

        if escolha == '1':
            alteração = input("O que deseja alterar:\n categoria \n nome, \n precoCusto \n precoVenda").lower()
            update = input("Digite a alteração a ser realizada: ").lower()
            try:
                self.cursor.execute(f"""
                UPDATE produtos SET {alteração} = {update} WHERE nome = {nomeProduto}
""")        
                self.conexao.commit()
                return "Operação realizada com sucesso."
            except Exception as e:
                print(f"Erro ao realizar a operação: {e}")
                return f"Erro ao realizar a operação, talvez você tenha errado. Sua escolha {alteração}, sua atualização: {update}."
            
        elif escolha == '2':
            elementos = ['categoria', 'nome', 'precoCusto', 'precoVenda']
            alteracoes = []
            for elemento in elementos:
                alt = input(f"Digite a alteração de {elemento}: ")
                alteracoes.append(alt)
            
            try: 
                self.cursor.execute(f"""
                    UPDATE produtos 
                    SET categoria = ?, nome = ?, precoCusto = ?, precoVenda = ?
                    WHERE nome = ?
""", *alteracoes, nomeProduto)
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

class Estoque(Banco):
    def __init__(self, bd="estoque.db") -> None:
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

def menu():
    estoque = Estoque()
    produto = Produto()
    while True:
    
        print("Sistema de Controle de Estoque")
        opcao = input("Selecione a opção desejada abaixo: \n1 - Produtos \n2 - Estoque \n Sua escolha: ")

        if opcao == '1': # Produtos
            entrada = input("\n1 - Cadastrar Produto \n2 - Deletar Produto \n3 - Atualizar Produto \n4 - Listar Produtos \n5 - Consultar Produto \nSua escolha: ")
            match entrada:
                case "1":
                    categoria = str(input("Digite a categoria do produto: "))
                    nome = str(input("Digite o nome do produto: "))
                    precoCusto = float(input("Digite o preço de custo do produto: "))
                    precoVenda = float(input("Digite o preço de venda do produto: "))
                    produto.cadastrarProduto(categoria, nome, precoCusto, precoVenda)
                    break
                case "2":
                    deletarProduto = str(input("Digite o nome do produto a ser deletado: "))
                    produto.deletarProduto(deletarProduto)
                    break
                case "3":
                    pass
                case "4":
                    produto.listarProdutos()
                case "5":
                    consulta = input("Digite o nome do produto a ser consultado: ")
                    print(produto.consultarProduto(consulta))
                    break
        elif opcao == '2': # Estoque
            pass
        else:
            print("Opção inválida")
       # return await limpar_tela()

if __name__ == '__main__':
    menu()