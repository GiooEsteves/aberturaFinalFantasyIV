import random

dialAbertura = ['Imediato: Mestre Cecil, a tripulação está indagando se foi certo o que fizemos ao roubar o cristal das mãos de civís.',
                'Cecil: Também não gostei do que vi, mas não cabe a nós questionar a ordem do rei',
                'Cecil: Logo chegaremos ao reino de Biron e é melhor que esses comentários cessem logo ou .....',
                'Timoneiro: Monstros na proa!',
                'Cecil: Preparem-se para a batalha.']

dialFechamento = ['Imediato: Estamos condenados.',
                  'Cecil: A cada dia que se passa, monstros cada vez mais fortes nos ameaçam.']

personagens = []
cecilPos = 0

def inteiroAleatorio(inf, sup):
    return random.randint(inf, sup)

def importaImagem(arquivo):
    arq = open(arquivo)
    per = arq.read()
    arq.close()
    return per

def criaItens():
    itens = []
    qtd = inteiroAleatorio(0,2)
    atributo = ['atk', 'def', 'hp']
    for i in range(qtd):
        att = inteiroAleatorio(0,len(atributo)-1)
        itens.append([atributo[att], inteiroAleatorio(10,20)])
    return itens
    
def criaPersonagens(img, tipo, nome):
    personagem = {'nome': nome, 'imagem':img, 'tipo':tipo}
    if tipo == 'protagonista':
        personagem['atk'] = inteiroAleatorio(1, 20)
        personagem['def'] = inteiroAleatorio(1, 10)
        personagem['hp'] = inteiroAleatorio(1, 100)
        personagem['agil'] = inteiroAleatorio(0, 2)
        personagem['itens'] = criaItens()
    elif tipo == 'monstro':
        personagem['atk'] = inteiroAleatorio(1, 20)
        personagem['def'] = inteiroAleatorio(1, 10)
        personagem['hp'] = inteiroAleatorio(1, 80)
        personagem['agil'] = inteiroAleatorio(0, 2)
    else:
        personagem = None
        print('Não é possível criar um personagem para esse tipo')
    return personagem

def defineOrdem():
    global personagens
    novaOrdem = []
    for i in personagens:
        novaOrdem.insert(i['agil'],i)
    personagens = novaOrdem.copy()

def verificaEntrada(valValidos, verificar):
    while verificar not in valValidos:
        verificar = int(input('Entrada inválida. \n Informe uma entrada válida!'))    
    return verificar

def imprimePersonagem(personagem):
    for i in personagem.keys():
        print(i,personagem[i], sep=': ')

def imprimeMenu(opcoes):
    for i in range(len(opcoes)):
        print(i, opcoes[i], sep=' - ')

def abertura():
    for i in dialAbertura:
        print('='*120)
        print(i)
        print('='*120)
        print()
        input('Pressione Enter para continuar.')
        print()

def retCecilPos():
    global cecilPos
    cecilPos = 2
    for i in range(2):
        if personagens[i]['nome'] == 'Cecil':
            cecilPos = i

def verificaFim():
    ret = True
    if personagens[cecilPos]['hp'] <= 0:
        ret = 'Perdeu'
    elif len(personagens) == 1:
        ret = 'Ganhou'
    return ret

def batalhar(p1, p2):
    global cecilPos
    if p1['atk'] > p2['def']:
        p2['hp'] = p2['hp'] - (p1['atk']-p2['def'])
        print('='*120)
        print(p2['nome'], 'sofreu dano e perdeu', (p1['atk']-p2['def']), 'pontos de vida')
        print('='*120)
        if p2['hp'] <= 0 and p2['tipo'] == 'monstro':
            personagens.remove(p2)
            if cecilPos > 0:
                cecilPos -= cecilPos
    else:
        print('='*120)
        print('O ataque não surtiu efeito.')
        print('='*120)
    
def usaItem(item, pos):
    print('='*120)
    print('O atributo', item, 'de Cecil aumentou de', personagens[cecilPos][item], end=' ')
    personagens[cecilPos][item] = personagens[cecilPos][item] + personagens[cecilPos]['itens'][pos][1]
    print('para', personagens[cecilPos][item])
    print('='*120)
    personagens[cecilPos]['itens'].pop(pos)
    
##Início do Jogo    
abertura()

##Cria personagens e define ordem
personagens.append(criaPersonagens(importaImagem('cecil.txt'), 'protagonista', 'Cecil'))
personagens.append(criaPersonagens(importaImagem('monster.txt'), 'monstro', 'Olhão'))
personagens.append(criaPersonagens(importaImagem('monster.txt'), 'monstro', 'Olhudo'))

defineOrdem()
retCecilPos()

##Loop principal do jogo
while verificaFim() == True:
    ##Inicia batalha
    for p in personagens:
        if p['tipo'] == 'monstro':
            imprimePersonagem(p)
            batalhar(p, personagens[cecilPos])
        else:
            imprimePersonagem(p)
            print('Opções:')
            imprimeMenu(['Atacar', 'Usar item', 'Fugir'])
            opt = verificaEntrada([0,1,2], int(input()))
            match opt:
                case 0:
                    nomes =[]
                    for i in personagens:
                        nomes.append(i['nome'])
                    print('Escolha um monstro para atacar: ')
                    imprimeMenu(nomes)
                    validos = [0,1,2]
                    validos.remove(cecilPos)
                    op = verificaEntrada(validos, int(input()))
                    batalhar(personagens[cecilPos], personagens[op])
                case 1:
                    chaves = []
                    for i in range(len(personagens[cecilPos]['itens'])):
                        chaves.append(personagens[cecilPos]['itens'][i][0])
                    if len(chaves) == 0:
                        print('Não há itens no inventário')
                    else:
                        print('Escolha um item para ser usado:')
                        imprimeMenu(chaves)
                        op = verificaEntrada(list(range(len(chaves))) , int(input()))
                        usaItem(chaves[op], op)
                case 2:
                    personagens[cecilPos]['hp'] = 0
                    break
        input('Pressione Enter para continuar.')

print('='*120)
if verificaFim() == 'Perdeu':
    print(dialFechamento[0])
else:
    print(dialFechamento[1])
print('='*120)