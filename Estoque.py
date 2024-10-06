import sqlite3
from Database import Banco

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

    def adicionar_produto_ao_estoque(self, nomeProduto, quantidade):
        idProduto = self.pegarIdProduto(nomeProduto)
        verificacao = self.verificaProdutoEstoque(nomeProduto)
        
        if verificacao == 2:
            return "\nProduto não cadastrado no sistema\n"
        elif not verificacao:
            self.cursor.execute("""
                INSERT INTO estoque (fk_id_produto, quantidade) VALUES (?,?)
""", (idProduto, quantidade))
            self.conexao.commit()
            return "\nProduto adicionado com sucesso ao estoque\n"
        else: # Caso esteja no estoque, então devemos atualizar a quantidade do produto
            self.cursor.execute("""
                UPDATE estoque SET quantidade = quantidade + ? WHERE fk_id_produto = ?
""", (quantidade, idProduto))
            self.conexao.commit()
            return "\nProduto atualizado no estoque com sucesso\n"
            
    def remover_produto_do_estoque(self, nomeProduto, quantidade):
        idProduto = self.pegarIdProduto(nomeProduto)
        verificacao = self.verificaProdutoEstoque(nomeProduto)

        if verificacao == 2:
            return "\nProduto não cadastrado no sistema\n"
        elif not verificacao:
            return "\nProduto não está no estoque."
        
        verifica_quant_no_estoque = self.cursor.execute("""
            SELECT quantidade FROM estoque WHERE fk_id_produto = ?
        """, (idProduto,)).fetchone()

        if verifica_quant_no_estoque is None:
            return "Produto sem unidades no estoque."
        
        col_quanti = verifica_quant_no_estoque[0]
        
        if quantidade > col_quanti:
            return "O produto não tem a quantia que deseja remover do estoque."
        elif quantidade == col_quanti:
            self.cursor.execute("""
                DELETE FROM estoque WHERE fk_id_produto = ?
            """, (idProduto,))
            self.conexao.commit()
            return "Produto deletado com sucesso devido a quantidade removida ser igual a dinsponível no estoque."
        else:  # quantidade < col_quanti
            self.cursor.execute("""
                UPDATE estoque SET quantidade = quantidade - ? WHERE fk_id_produto = ?
            """, (quantidade, idProduto))
            self.conexao.commit()
            return f"{quantidade} do produto {nomeProduto} foram removidas com sucesso"
    
    def pegarIdProduto(self, nomeProduto):
        self.cursor.execute("""
            SELECT id FROM produtos WHERE nome = ?
        """, (nomeProduto,))
        
        consulta = self.cursor.fetchone()  # Obtém o ID do produto
        if consulta is None:
            return None  # Retorna None se o produto não estiver cadastrado
        else:
            return consulta[0]  # Retorna apenas o ID

    def verificaProdutoEstoque(self, nomeProduto):
        # Pega o ID do produto, se existir
        idProduto = self.pegarIdProduto(nomeProduto)
        
        if idProduto is None:
            return 2
        
        # Verifica se o produto já está no estoque
        self.cursor.execute("""
            SELECT * FROM estoque WHERE fk_id_produto = ?
        """, (idProduto,))
        
        result = self.cursor.fetchone()  # Verifica se o produto já está na tabela estoque
        
        if result is None:
            return False
        
        return True # Retorna se o produto estiver no estoque

    def consultarEstoque(self):
        try:
            consulta = self.cursor.execute("""
                SELECT p.nome, p.preco_custo, p.preco_de_venda, e.quantidade FROM produtos AS p 
                INNER JOIN estoque AS e ON p.id = fk_id_produto
    """).fetchall()
            if consulta is None:
                return "Nenhum produto encontrado"
            for produto in consulta:
                lucro = (produto[2] - produto[1]) * produto[3]
                print(f"Produto: {produto[0]}")
                print(f"Preço de Custo: {produto[1]}")
                print(f"Preço de Venda: {produto[2]}")
                print(f"Quantidade no Estoque: {produto[3]}")
                print(f"Lucro Esperado: {lucro}")
                print("---------------")
            return "Esses são os produtos no estoque"
        except SystemError as e:
            return f"Erro ao realizar consulta devido: {e}"

    def consultar_produto_no_estoque(self, nomeProduto):
        idProduto = self.pegarIdProduto(nomeProduto)
        if idProduto is None:
            return "Produto não cadastrado no sistema."
        try: 
            consulta = self.cursor.execute("""
            SELECT p.nome, p.preco_custo, p.preco_de_venda, e.quantidade FROM produtos AS p 
            INNER JOIN estoque AS e ON p.id = fk_id_produto WHERE p.id = ?
""", (idProduto, )).fetchone()
            if consulta is None:
                return "Produto não cadastrado no estoque."
            lucro = (consulta[2] - consulta[1]) * consulta[3]
            print(f"Produto: {consulta[0]}")
            print(f"Preço de Custo: {consulta[1]}")
            print(f"Preço de Venda: {consulta[2]}")
            print(f"Quantidade no Estoque: {consulta[3]}")
            print(f"Lucro Esperado: {lucro}")
            print("---------------")
            return "Esses são os dados do produto consultado."
        except sqlite3.Error as e:
            return f"Ocorreu um erro ao realizar a operação: {e}"

