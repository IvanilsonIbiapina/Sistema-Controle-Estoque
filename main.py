from Produto import Produto
from Estoque import Estoque


def main():
    # Instância de classes
    estoque = Estoque()
    produto = Produto()
    
    while True:
    
        print("\nSistema de Controle de Estoque")
        opcao = input("Selecione a opção desejada abaixo: \n1 - Produtos \n2 - Estoque \n0 - Sair \n Sua escolha: ")

        if opcao == '1': # Produtos
            entrada = input("\n1 - Cadastrar Produto \n2 - Deletar Produto \n3 - Atualizar Produto \n4 - Listar Produtos \n5 - Consultar Produto \nSua escolha: ")
            match entrada:
                case "1":
                    categoria = str(input("Digite a categoria do produto: "))
                    nome = str(input("Digite o nome do produto: "))
                    precoCusto = float(input("Digite o preço de custo do produto: "))
                    precoVenda = float(input("Digite o preço de venda do produto: "))
                    mensagem = produto.cadastrarProduto(categoria, nome, precoCusto, precoVenda)
                    print(mensagem)
                    break
                case "2":
                    deletarProduto = str(input("Digite o nome do produto a ser deletado: "))
                    mensagem = produto.deletarProduto(deletarProduto)
                    print(mensagem)
                    break
                case "3":
                    update = input("Digite o nome do produto a ser alterado: ")
                    mensagem = produto.atualizarProduto(update)
                    print(mensagem)
                    break
                case "4":
                    mensagem = produto.listarProdutos()
                    print(mensagem)
                    break
                case "5":
                    consulta = input("Digite o nome do produto a ser consultado: ")
                    print(produto.consultarProduto(consulta))
                    break
                case '_':
                    print("Opção inválida.")
        elif opcao == '2': # Estoque
            entrada = input("1 - Adicionar produto ao estoque \n2 - Remover produto do estoque \n3 - Consultar Estoque \n4 - Consultar produto no estoque \nOpção desejada: ")
            match entrada:
                case '1':
                    produtoAdd = input("Digite o nome do produto que deseja adicionar ao estoque: ")
                    quantidade = int(input("Quantidade a ser adicionada: "))
                    mensagem = estoque.adicionar_produto_ao_estoque(produtoAdd, quantidade)
                    print(mensagem)
                case '2':
                    produtoRemove = input("Digite o nome do produto que deseja remover do estoque: ")
                    quantidade = int(input("Quantidade a ser removida: "))
                    mensagem = estoque.remover_produto_do_estoque(produtoRemove, quantidade)
                    print(mensagem)
                case '3':
                    pass
                case '4':
                    pass
                case '5':
                    pass
                case '_':
                    print("Opção inválida.")
        elif opcao == '0':
            print('\n Programa encerrando...')
            break
        else:
            print("Opção inválida")

if __name__ == '__main__':
    main()