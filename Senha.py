import random
import io

MAX_TENTATIVAS = 6

def main():
    """Implementa o mecanismo principal do jogo."""
    print('\nBem-Vindo ao Jogo de Senha da FEA.dev!\n')
    print('As regras são simples:', '1. Seu objetivo é adivinhar a palavra secreta, que tem número aleatório de letras.', '2. A cada chute, será mostrado quais letras você errou (_), quais têm na palavra (+) e quais têm e você acertou o lugar (*).', '3. Também a cada chute, serão mostradas todas as suas tentativas e o teclado atualizado sem as letras que não estão na palavra', '\nBOA SORTE!', sep='\n')
    '''# Pede opção de lingua
    lingua = ''
    while lingua != 'P' and lingua != 'I':
        lingua = input("Qual o idioma? (P para português ou I para inglês) ")

    # Carrega lista de palavras do arquivo correspondente
    if lingua == 'P':
        lista_palavras = cria_lista_palavras('palavras.txt')
    elif lingua == 'I':
        lista_palavras = cria_lista_palavras('words.txt')'''
    lista_palavras = cria_lista_palavras('palavras.txt')

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

    while num_tentativas < MAX_TENTATIVAS and not ganhou:
        if len(chute) == NUM_LETRAS:
            checa_tentativa(palavra, chute, marca)
            linha = [ct, marca[:]]
            lista_tentativas.append(linha[:])
            atualiza_teclado(chute, marca, teclado)
            imprime_resultado(lista_tentativas)

            if chute != palavra:
                imprime_teclado(teclado)
                ct = input('Digite a palavra: ')
                chute = formatar(ct)
            else:
                ganhou = True
            num_tentativas += 1
        else:
            print(f'Palavra inválida! Lembre-se que o número de letras é {NUM_LETRAS}')
            ct = input('Digite a palavra: ')
            chute = formatar(ct)
    if ganhou:
        print('PARABÉNS!')
    else:
        imprime_resultado(lista_tentativas)
        print(f'Que pena... A palavra era {palavra}.')


def cria_lista_palavras(nome_arquivo):
    """Recebe uma string com o nome do arquivo e devolve uma lista contendo as palavras do arquivo."""
    ref = io.open(f"JogoSenha/Listas de Palavras/{nome_arquivo}", "r", encoding="utf8")
    conteudo = ref.read()
    ref.close()
    lista_palavras = conteudo.split('\n')
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
