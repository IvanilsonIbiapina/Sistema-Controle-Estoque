from Produto import Produto
from Estoque import Estoque


def main():
    # Instância de classes
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
                    update = input("Digite o nome do produto a ser alterado: ")
                    produto.atualizarProduto(update)
                    break
                case "4":
                    produto.listarProdutos()
                    break
                case "5":
                    consulta = input("Digite o nome do produto a ser consultado: ")
                    print(produto.consultarProduto(consulta))
                    break
        elif opcao == '2': # Estoque
            pass
        else:
            print("Opção inválida")

if __name__ == '__main__':
    main()