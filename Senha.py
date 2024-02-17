import random
from pandas import read_csv

def main():
    """Implementa o mecanismo principal do jogo."""
    print('\nBem-Vindo ao Jogo de Senha da FEA.dev!\n')
    print('As regras são simples:', '1. Seu objetivo é adivinhar a palavra secreta, que tem número aleatório de letras.', '2. A cada chute, será mostrado quais letras você errou (_), quais estão na palavra mas no lugar errado (+) e quais você acertou o lugar (*).', '3. Também a cada chute, serão mostradas todas as suas tentativas e o teclado atualizado, sem as letras que não estão na palavra', sep='\n')
    
    sorteio = random.randint(0, 2)

    # Carrega lista de palavras do arquivo correspondente
    if sorteio == 0:
        print('\nO tema do Jogo será: Frutas')
        lista_palavras = cria_lista_palavras('frutas.txt')
    elif sorteio == 1:
        print('\nO tema do Jogo será: Sobremesas')
        lista_palavras = cria_lista_palavras('sobremesas.txt')
    else:
        print('\nO tema do Jogo será: Geral')
        lista_palavras = cria_lista_palavras('palavras.txt')
    print('\nBOA SORTE!')

    # Sorteia uma palavra aleatória da lista
    palavra = lista_palavras[random.randint(0, len(lista_palavras) - 1)]
    NUM_LETRAS = len(palavra)

    num_tentativas = 0
    lista_tentativas = []
    ganhou = False
    teclado = inicializa_teclado()
    marca = [0]*NUM_LETRAS

    imprime_teclado(teclado)
    ct = input(f'Digite a palavra ({NUM_LETRAS} letras): ')
    chute = formatar(ct)

    while True:
        if len(chute) == NUM_LETRAS and chute in lista_palavras and not any(chute in lista for lista in lista_tentativas):
            checa_tentativa(palavra, chute, marca)
            linha = [ct, marca[:]]
            lista_tentativas.append(linha[:])
            atualiza_teclado(chute, marca, teclado)
            imprime_resultado(lista_tentativas)

            num_tentativas += 1
            if chute != palavra:
                if num_tentativas == NUM_LETRAS:
                    break
                imprime_teclado(teclado)
                ct = input(f'Digite a palavra (Restam {NUM_LETRAS - num_tentativas} chances): ')
                chute = formatar(ct)
            else:
                ganhou = True
                break
        else:
            if len(chute) != NUM_LETRAS:
                print(f'Palavra inválida! Lembre-se que o número de letras é {NUM_LETRAS}\n')
                ct = input('Digite a palavra: ')
                chute = formatar(ct)
            elif chute not in lista_palavras:
                print(f'Ops! A palavra não é válida...Tente de novo\n')
                ct = input('Digite a palavra: ')
                chute = formatar(ct)
            else:
                print(f'Palavra repetida! Tente novamente\n')
                ct = input('Digite a palavra: ')
                chute = formatar(ct)
    if ganhou:
        print(f'PARABÉNS! Você acertou! A palavra era {palavra}.')
    else:
        imprime_resultado(lista_tentativas)
        print(f'Que pena... A palavra era {palavra}.')


def cria_lista_palavras(nome_arquivo):
    """Recebe uma string com o nome do arquivo e devolve uma lista contendo as palavras do arquivo."""
    lista_palavras = list(read_csv(f'JogoSenha/Listas de Palavras/{nome_arquivo}', header=None)[0])
    # Formata cada palavra da lista
    lista_formatada = []
    for i in range(len(lista_palavras) - 1):
        lista_formatada.append(formatar(lista_palavras[i]))

    return lista_formatada


def formatar(palavra):
    """Formata a palavra, removendo maiúsculas e acentos."""
    letras_palavra = list(palavra.lower())

    for i in range(len(palavra)):
        if 224 <= ord(letras_palavra[i]) <= 229:
            letras_palavra[i] = 'a'
        elif 232 <= ord(letras_palavra[i]) <= 235:
            letras_palavra[i] = 'e'
        elif 236 <= ord(letras_palavra[i]) <= 239:
            letras_palavra[i] = 'i'
        elif 242 <= ord(letras_palavra[i]) <= 246:
            letras_palavra[i] = 'o'
        elif 249 <= ord(letras_palavra[i]) <= 252:
            letras_palavra[i] = 'u'
        elif ord(letras_palavra[i]) == 231:
            letras_palavra[i] = 'c'

    nova_palavra = ''
    for letra in letras_palavra:
        nova_palavra += letra

    return nova_palavra


def inicializa_teclado():
    """Inicializa o teclado com as teclas na ordem."""
    teclado = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
               ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
               ['z', 'x', 'c', 'v', 'b', 'n', 'm']]
    return teclado


def imprime_teclado(teclado):
    """Exibe o teclado com as letras possíveis."""
    print('-----------------------------------------')
    for linha in teclado:
        for letra in linha:
            print(letra, end=' ')
        print()
    print('-----------------------------------------')


def checa_tentativa(palavra, chute, marca):
    """Recebe a palavra secreta e o chute do usuario e verifica:
    se possui letras certas no lugar certo -> atualiza a posicao da lista marca correspondente com 1 (verde),
    se possui letra certa no lugar errado -> atualiza a posicao da lista marca com 2 (amarelo)
    e -> 0 caso contrário."""
    for i in range(len(chute)):
        if chute[i] in palavra:
            if chute[i] == palavra[i]:
                marca[i] = 1
            else:
                marca[i] = 2
        else:
            marca[i] = 0


def atualiza_teclado(chute, marca, teclado):
    """Modifica o teclado para que as letras do chute que não estejam na palavra secreta sejam substituídas por espaços."""
    for i in range(len(chute)):
        if marca[i] == 0:
            for l in range(len(teclado)):
                for c in range(len(teclado[l])):
                    if teclado[l][c] == chute[i]:
                        teclado[l][c] = ' '


def imprime_resultado(lista):
    """Recebe a lista de tentativas e as imprime, 
       usando * para verde, + para amarelo e _ para preto."""
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            if j % 2 == 0:
                print(lista[i][j])
            else:
                marca_str = ''
                for caracter in lista[i][j]:
                    if caracter == 1:
                        marca_str += '*'
                    elif caracter == 2:
                        marca_str += '+'
                    else:
                        marca_str += '_'
                print(marca_str)


if __name__ == "__main__":
    main()
