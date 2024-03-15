import copy

def lkg(mod):
    a = 245
    c = 907
    num=((a*sequence[-1])+c)%15445
    #print(f'{a}*{sequence[-1]}+{c}%{mod}')
    sequence.append(num)
    num=num%mod
    return num

def randomGen(mod): #Nasumicno generise jedan broj na osnovu sekvence i taj broj dodaje u sekvencu
    j = 7
    k = 10
    n = len(fibo)
    num = (fibo[n - j] + fibo[n - k]) % mod
    fibo.append(num)
    return num


def generateStart(n, k): #Generise pocetno stanje bocice kao listu listi, svaka podlista=jedna bocica
    colors = {}         #prati broj ponavljanja boja
    start = []
    empty = []
    for i in range(n - k):
        start.append([])
        colors[i] = 0
    for i in range(k):  #dodaje prazne bocice
        empty.append(['_', '_', '_', '_'])
    for i in range(4):
        for list in start:
            num = lkg(n - k)
            # colors[num]+=1
            while colors[num] >= 4:   #Proverava da li vec ima 4 jedinice neke boje
                num = lkg(n - k)
            colors[num] += 1
            list.append(num)
    return start + empty



class Bottle:

    def __init__(self, data):
        self.data = data
        for i in range(4):   #Na osnovu sadrzaja bocice odredjuje neke njene osobine
            if data[0] == '_':
                self.top = '_'
                self.lastColor = None
                self.spaces = 4
                break
            elif data[i] == '_':
                self.top = data[i]
                self.lastColor = data[i - 1]
                self.spaces = 4 - i
                break
            else:
                self.top = data[i]
                self.lastColor = data[i]
                self.spaces = 0

        for i in range(3, -1, -1):
            if data[i] == '_':
                self.full = False
                break
            else:
                self.full = True

    def refreshBottle(self):  #Nakon presipanja iz bocice u bocicu, ponovo proverava i odredjuje osobine bocice
        data = self.data
        for i in range(4):
            if data[0] == '_':
                self.top = '_'
                self.lastColor = None
                self.spaces = 4
                break
            elif data[i] == '_':
                self.top = data[i]
                self.lastColor = data[i - 1]
                self.spaces = 4 - i
                break
            else:
                self.top = data[i]
                self.lastColor = data[i]
                self.spaces = 0

        for i in range(3, -1, -1):
            if data[i] == '_':
                self.full = False
                break
            else:
                self.full = True

    def isWinnable(self):  #Na osnovu boja u bocici proverava da li je bocica pobednicka
        if self.data[0] == self.data[1] == self.data[2] == self.data[3]:  # and self.data[0]!='_':
            return True
        else:
            return False


def isMixable(bot1, bot2):  #Proverava da li je moguce presipanje iz bot1 u bot2
    if bot2.full or bot1.spaces == 4 or bot1.isWinnable() or bot1 == bot2:  # or (bot1.top!=bot2.top and bot2.top!='_'): #or bot1.iswinnable
        return False
    if bot1.lastColor == bot2.lastColor or bot2.lastColor == None:
        return True
    if bot1.lastColor != bot2.lastColor:
        return False


def mixBottles(bot1, bot2):     #Presipanje iz bot1 u bot2
    while isMixable(bot1, bot2): #Dok je moguce mesati ponavlja se mesanje
        index1 = len(bot1.data) - bot1.data[::-1].index(bot1.lastColor) - 1
        if bot2.top == '_':
            index2 = bot2.data.index(bot2.top)
        else:
            index2 = bot2.data.index(bot2.top)
        # print(f'Menjam {index1} sa {index2}')
        # print(f'Ocu menjam {bot1.data[index1]} sa {bot2.data[index2]}')
        temp = bot1.data[index1]
        bot1.data[index1] = bot2.data[index2]
        bot2.data[index2] = temp
        bot1.refreshBottle()
        bot2.refreshBottle()


def createIDs(tree):    #Kreira recnik u kojem sifruje cvorove stabla
    treeDict = {}
    i = 0
    for node in tree:
        key = 'Node' + f'{i}'
        treeDict[key] = node
        i += 1
    return treeDict


def getNode(treeDict, id):      #Na osnovu ID cvora dohvata taj objekat
    return treeDict[id]


def getKey(treeDict, node):     #Na osnovu objekta dohvata njegovu sifru
    for key, value in treeDict.items():
        if node == value:
            return key

def findWinner(tree):      #Iz liste u kojoj su cvorovi popakovani (level order) dohvata prvog pobednika
    for node in tree:
        if node.isWin():
            winNode=node
            return winNode

class Node:

    def __init__(self):
        self.data = []
        self.father = None
        self.children = []
        self.level = 0
        self.win = False

    def isWin(self):        #Proverava da li je cvor pobedonosni
        for bottle in self.data:
            if not bottle.isWinnable():
                return False
        return True

    def addAllBottles(self, list):  #U pocetnom stanju na osnovu liste listi (bocica) formira objekte Bocica i dodaje
        for elem in list:           #kao sadrzaj cvora
            self.data.append(Bottle(elem))

    def addOneBottle(self, bott):
        self.data.append(bott)

    def addChild(self, child): #Dodaje sina za zadati cvor i odredjuje sinu neke atribute
        child.father = self
        self.children.append(child)
        child.level = child.father.level + 1

    def generateChildren(self): #Za jedan cvor izgenerise njegovu validnu decu
        sablon = copy.deepcopy(self.data)  #Pocetno stanje
        for i in range(len(sablon)):
            bot1 = copy.deepcopy(sablon[i])
            for j in range(len(sablon)):
                bot2 = copy.deepcopy(sablon[j])
                if i == j:   #ne moze da se presipa jedna ista bocica
                    continue
                else:
                    if isMixable(bot1, bot2) and not self.isWin(): #ako je moguce izmesati bocice, izmesaju se
                        mixBottles(bot1, bot2)
                        child = Node()
                        child.data = copy.deepcopy(self.data)
                        child.data[i] = copy.deepcopy(bot1)
                        child.data[j] = copy.deepcopy(bot2)
                        if self.checkNode():    #Dodatna provera da li je sve u redu sa stanjem
                            self.addChild(child)
                            self.data = copy.deepcopy(sablon)

    def checkNode(self):   #Provera da li je sve u redu sa cvorom-stanjem
        total = 0
        for bottle in self.data:
            total += bottle.spaces
        if total != k * 4:
            return False
        return True


    def generateTree(self):
        nodes = [rootNode]
        i = 0
        currentNode = nodes[i]
        foundWin = False
        while currentNode.level < p or currentNode.level == 0:
            currentNode.generateChildren()
            for child in currentNode.children:
                if not child.checkNode():
                    currentNode.children.remove(child)
            nodes = nodes + currentNode.children
            i += 1
            # if currentNode.isWin() and not foundWin:
            #     winningNode.data = copy.deepcopy(currentNode.data)
            #     winningNode.father = currentNode.father
            #     foundWin = True
            if i <= len(nodes) - 1:
                currentNode = nodes[i]
            else:
                break
        return nodes

    def printNode(self):        #Printa cvor
        tab = '   ' * self.level  #tabulacija odredjena na osnovu dubine-nivoa cvora
        if self.level == 0:
            tab = ''
        lista = []
        for bottle in self.data:
            lista.append(bottle.data)
        for i in range(3, -1, -1):
            print(tab, end='')
            for list in lista:
                print(f'| {list[i]} |    ', end='')
            print('\n', end='')
        separator = '________' * len(lista)
        print(f'{tab}{separator}')


def printWinningNode():   #printa pobednicko resenje, sa usputnim koracima, za izgenerisano pocetno stanje
    if winningNode is None:
        print('Nema uspesnog resenja za ovaj broj poteza')
    elif winningNode.data == []:
        print('Nema uspesnog resenja za ovaj broj poteza')
    else:
        lista = []
        currentNode = winningNode
        while currentNode is not None:  #Pravi listu cvorova koji su doveli do resenja
            lista.append(currentNode)
            currentNode = currentNode.father
        for i in range(len(lista) - 1, -1, -1):     #printa listu koraka unazad da bi se krenulo od pocetka
            lista[i].printNode()

sequence=[154]
fibo = [5, 9, 6, 4, 8, 7, 2, 0, 11, 5, 4]  # 5,9,6,4,8,7,2,0,11,5,4
n = int(input('Unesi ukupna broj bocica: '))
k = int(input('Unesi broj praznih bocica: '))
p = int(input('Unesi maksimalan broj koraka do cilja: '))
start = generateStart(n, k)
rootNode = Node()
rootNode.addAllBottles(start)
rootNode.printNode()
treeDict={}

tree = rootNode.generateTree()
winningNode=findWinner(tree)
moves=0
currentPlay=rootNode
while True:
    try:
        option = int(input('\nIzaberi opciju:\n'
                           '1. Ispisi celo stablo\n'
                           '2. Odigraj potez\n'
                           '3. Hint\n'
                           '4. Ispisi jedno validno resenje\n'
                           '5. Prikazi zeljeni cvor\n'
                           '0. Kraj\n'))

        if option < 0 or option > 5:
            print('Unesi ispravan broj!')

    except:
        print('Unesi broj kao opciju!')
        continue

    if option == 1:
        currentLevel=0
        treeDict = createIDs(tree)
        print(f'\n-----NIVO {currentLevel}-----')
        for key in treeDict:
            list = []
            for child in treeDict[key].children:
                if getKey(treeDict,child) is not None:
                    list.append(getKey(treeDict, child))
            if treeDict[key].level!=currentLevel:
                currentLevel+=1
                print(f'\n-----NIVO {currentLevel}-----')
            print(f'{key}-->{list}')


    elif option == 2:
        moves+=1
        if moves<=p:
            try:
                bot1=int(input('Iz bocice: '))
                bot2=int(input('U bocicu: '))
                if bot1>n or bot1<=0 or bot2<=0 or bot2>n:
                    print('Bar jedna od unetih bocica ne postoji')
                    continue
                mixBottles(currentPlay.data[bot1-1],currentPlay.data[bot2-1])
                if currentPlay.father is not None and currentPlay.data==currentPlay.father.data:
                    print('Nista se nije desilo')
                currentPlay.printNode()
            except ValueError:
                print('Nepravilno unesene bocice')
            if currentPlay.isWin():
                print('BRAVO! REEEESI IGRU!')
        else:
            print('Nemas vise poteza')

    elif option == 3:

        currentTree=currentPlay.generateTree()
        currentWinner=findWinner(currentTree)
        if currentWinner==None:
            print("Za ovaj broj poteza ne postoji pobednik!")
            continue
        while currentWinner.father is not currentPlay:
            currentWinner=currentWinner.father
            if currentWinner==None:
                print('Ovo je pobednicki cvor, nema dalje!')
                break
        if currentWinner is not None:
            currentWinner.printNode()
            currentPlay=currentWinner
        del currentTree


    elif option == 4:
        printWinningNode()


    elif option == 5:
        try:
            keyToPrint=input('Unesi ID (Node_) zeljenog cvora: ')
            if keyToPrint not in treeDict:
                print('Ovaj cvor ne postoji u stablu')
            else:
                nodeToPrint=treeDict[keyToPrint]
                tab=nodeToPrint.level*'   '
                print(f'{tab}NIVO {nodeToPrint.level}')
                nodeToPrint.printNode()
        except KeyError:
            print('Prvo je potrebno ispisati celo stablo a onda pristupiti cvoru!')


    elif option == 0:
        break
