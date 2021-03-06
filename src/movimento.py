
class Mover:
    rankRows = {"1": 7,"2": 6,"3": 5,"4": 4,"5": 3,"6": 2,"7": 1,"8": 0}
    rowsRanks = {v: k for k, v in rankRows.items()}
    filesCols = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,"g": 6,"h": 7}
    colsFiles = {v: k for k, v in filesCols.items()}

    def __init__(self, inicio: tuple, fim: tuple, tabuleiro: list) -> None:
        self.inicioRow, self.inicioCol = inicio
        self.fimRow, self.fimCol = fim
        self.pecaMovida = tabuleiro[self.inicioRow][self.inicioCol]
        self.pecaCapturada = tabuleiro[self.fimRow][self.fimCol]

    def getRankFiles(self, row: int, col: int) -> str:
        return self.colsFiles[col] + self.rowsRanks[row]

    def getFilesNumber(self, row: int) -> int:
        return self.filesCols[row]

    def getRankNumber(self, row: int) -> int:
        return self.rankRows[row]

    def getChessNotation(self) -> str:
        return self.getRankFiles(self.inicioRow, self.inicioCol) + "" + self.getRankFiles(self.fimRow, self.fimCol)

    def validaMovimento(self, peca: str, cor: str, posicaoAtual: tuple, tabuleiro: list, moveLogNotation: list) -> list:
        if peca == 'P':
            return self.movPeao(cor, posicaoAtual, tabuleiro, moveLogNotation)
        elif peca == 'R':
            return self.movTorre(cor, posicaoAtual, tabuleiro)
        elif peca == 'N':
            return self.movCavalo(cor, posicaoAtual, tabuleiro)
        elif peca == 'B':
            return self.movBispo(cor, posicaoAtual, tabuleiro)
        elif peca == 'K':
            return self.movRei(cor, posicaoAtual, tabuleiro, moveLogNotation)
        elif peca == 'Q':
            return self.movRainha(cor, posicaoAtual, tabuleiro)

    def peaoPassado(self, cor: str, posicaoAtual: tuple, tabuleiro: list, moveLogNotation: list) -> list:
        movPossiveis = [[],[]]
        inverte = 1
        posInicial = 1
        if cor == 'w':
            inverte *= -1
            posInicial = 6

        if posicaoAtual[1] < 7: 
            lateralDireita = tabuleiro[(posicaoAtual[0])][(posicaoAtual[1] + 1)]
            if lateralDireita[0] != cor and lateralDireita[1] == 'P':
                if (int(moveLogNotation[-1][1]) - 1) == posInicial:
                    if self.getRankNumber(moveLogNotation[-1][3]) == posicaoAtual[0] and self.getFilesNumber(moveLogNotation[-1][2]) == (posicaoAtual[1] + 1):
                        movPossiveis[0] = ((posicaoAtual[0] + (inverte*1)), (posicaoAtual[1] + 1))

        lateralEsquerda = tabuleiro[(posicaoAtual[0])][(posicaoAtual[1] - 1)]
        if lateralEsquerda[0] != cor and lateralEsquerda[1] == 'P':
            if (int(moveLogNotation[-1][1]) - 1) == posInicial:
                if self.getRankNumber(moveLogNotation[-1][3]) == posicaoAtual[0] and self.getFilesNumber(moveLogNotation[-1][2]) == (posicaoAtual[1] - 1):
                    movPossiveis[1] = ((posicaoAtual[0] + (inverte*1)), (posicaoAtual[1] - 1))

        return movPossiveis

    def movPeao(self, cor: str, posicaoAtual: tuple, tabuleiro: list, moveLogNotation: list) -> list:
        movPossiveis = []
        inverte = 1
        posInicial = 1
        if cor == 'w':
            inverte *= -1
            posInicial = 6

        diagonalEsquerda = tabuleiro[(posicaoAtual[0] + (inverte*1))][(posicaoAtual[1] - 1)]
        if (posicaoAtual[1] + 1) < 8:
            diagonalDireita = tabuleiro[(posicaoAtual[0] + (inverte*1))][(posicaoAtual[1] + 1)]
            if diagonalDireita != '--' and diagonalDireita[0] != cor:
                movPossiveis.append(((posicaoAtual[0] + (inverte*1)), (posicaoAtual[1] + 1)))
        
        peaoPassadoDireita = self.peaoPassado(cor, posicaoAtual, tabuleiro, moveLogNotation)
        if peaoPassadoDireita[0] != []:
            movPossiveis.append(peaoPassadoDireita[0])
        if peaoPassadoDireita[1] != []:
            movPossiveis.append(peaoPassadoDireita[1])
        
        if diagonalEsquerda != '--' and diagonalEsquerda[0] != cor:
            movPossiveis.append(((posicaoAtual[0] + (inverte*1)), (posicaoAtual[1] - 1)))

        qtdeMov = 1
        if posicaoAtual[0] == posInicial:
            qtdeMov += 1
        for mov in range(1, (qtdeMov + 1)):
            if tabuleiro[(posicaoAtual[0] + (inverte*mov))][posicaoAtual[1]] == '--':
                movPossiveis.append(((posicaoAtual[0] + (inverte*mov)), posicaoAtual[1]))
            if mov == 1 and tabuleiro[(posicaoAtual[0] + (inverte*mov))][posicaoAtual[1]] != '--':
                break

        return movPossiveis

    def loopMovimentoLinhaReta(self, vertical: bool, inicio: int, fim: int, passo: int, posicaoAtual: tuple, tabuleiro: list, cor: str) -> list:
        movPossiveis = []
        if vertical:
            for casa in range(inicio, fim, passo):
                if tabuleiro[casa][posicaoAtual[1]] == '--':
                    movPossiveis.append((casa, posicaoAtual[1]))
                elif tabuleiro[casa][posicaoAtual[1]][0] != cor:
                    movPossiveis.append((casa, posicaoAtual[1]))
                    break
                else:
                    break
        else:
            for casa in range(inicio, fim, passo):
                if tabuleiro[posicaoAtual[0]][casa] == '--':
                    movPossiveis.append((posicaoAtual[0], casa))
                elif tabuleiro[posicaoAtual[0]][casa][0] != cor:
                    movPossiveis.append((posicaoAtual[0], casa))
                    break
                else:
                    break

        return movPossiveis

    def movTorre(self, cor: str, posicaoAtual: tuple, tabuleiro: list) -> list:
        movPossiveis = []
        menor = -1
        maior = 8
        movPossiveis = movPossiveis + self.loopMovimentoLinhaReta(True, (posicaoAtual[0]+1), maior, 1, posicaoAtual, tabuleiro, cor)
        movPossiveis = movPossiveis + self.loopMovimentoLinhaReta(True, (posicaoAtual[0]-1), menor, -1, posicaoAtual, tabuleiro, cor)
        movPossiveis = movPossiveis + self.loopMovimentoLinhaReta(False, (posicaoAtual[1]+1), maior, 1, posicaoAtual, tabuleiro, cor)
        movPossiveis = movPossiveis + self.loopMovimentoLinhaReta(False, (posicaoAtual[1]-1), menor, -1, posicaoAtual, tabuleiro, cor)

        return movPossiveis
        
    def loopMovimentoLinhaDiagonal(self, sentidoRow: int, sentidoCol: int, cor: str, posicaoAtual: tuple, tabuleiro: list) -> list:
        movPossiveis = []
        for casa in range(1, 8):
            row = posicaoAtual[0] + (casa * sentidoRow)
            col = posicaoAtual[1] + (casa * sentidoCol)
            if row < 0 or row > 7 or col < 0 or col > 7 :
                break
            elif tabuleiro[row][col] == '--':
                movPossiveis.append((row, col))
            elif tabuleiro[row][col][0] != cor:
                movPossiveis.append((row, col))
                break
            else:
                break
        return movPossiveis

    def movBispo(self, cor: str, posicaoAtual: tuple, tabuleiro: list) -> list:
        movPossiveis = []
    
        movPossiveis = self.loopMovimentoLinhaDiagonal(1, 1, cor, posicaoAtual, tabuleiro)
        
        movPossiveis = movPossiveis + self.loopMovimentoLinhaDiagonal(-1, 1, cor, posicaoAtual, tabuleiro)
        movPossiveis = movPossiveis + self.loopMovimentoLinhaDiagonal(1, -1, cor, posicaoAtual, tabuleiro)
        movPossiveis = movPossiveis + self.loopMovimentoLinhaDiagonal(-1, -1, cor, posicaoAtual, tabuleiro)
    
        return movPossiveis

    def movRainha(self, cor, posicaoAtual, tabuleiro) -> list:
        movTorre = self.movTorre(cor, posicaoAtual, tabuleiro)
        movBispo = self.movBispo(cor, posicaoAtual, tabuleiro)
        movPossiveis = movTorre + movBispo

        return movPossiveis

    def castle(self, cor: str, posicaoAtual: tuple, tabuleiro: list, moveLogNotation: list) -> list:
        movPossiveis = [(), ()]
        rowInicial = 0
        rowInicialNotation = 8
        if cor == 'w':
            rowInicial = 7
            rowInicialNotation = 1

        if any("e"+str(rowInicialNotation) in mov for mov in moveLogNotation):
            return movPossiveis

        if tabuleiro[rowInicial][5] == '--' and tabuleiro[rowInicial][6] == '--' and not any("h"+str(rowInicialNotation) in mov for mov in moveLogNotation):
            movPossiveis[0] = (posicaoAtual[0], (posicaoAtual[1] + 2))

        if tabuleiro[rowInicial][1] == '--' and tabuleiro[rowInicial][2] == '--' and tabuleiro[rowInicial][3] == '--' and not any("a"+str(rowInicialNotation) in mov for mov in moveLogNotation):
            movPossiveis[1] = (posicaoAtual[0], (posicaoAtual[1] - 2))

        return movPossiveis

    def movRei(self, cor: str, posicaoAtual: tuple, tabuleiro: list, moveLogNotation: list) -> list:
        movPossiveis = []
        row = posicaoAtual[0]
        col = posicaoAtual[1]

        for c in range(1, 3):
            for i in range(1, 3):
                rowCasa = 1
                colCasa = 1
                if i // 2 == 0:
                    rowCasa = rowCasa * -1
                if c // 2 == 0:
                    colCasa = colCasa * -1
                if (row + rowCasa) < 8 and (row + rowCasa) > -1 and (col + colCasa) < 8 and (col + colCasa) > -1:
                    if tabuleiro[(row + rowCasa)][(col + colCasa)] == '--' or tabuleiro[(row + rowCasa)][(col + colCasa)][0] != cor:
                        movPossiveis.append(((row + rowCasa), (col + colCasa)))
                if c == i:
                    if row < 8 and row > -1 and (col + colCasa) < 8 and (col + colCasa) > -1:
                        if tabuleiro[row][(col + colCasa)] == '--' or tabuleiro[row][(col + colCasa)][0] != cor:
                            movPossiveis.append((row, (col + colCasa)))
                else:
                    if (row + rowCasa) < 8 and (row + rowCasa) > -1 and col < 8 and col > -1:
                        if tabuleiro[(row + rowCasa)][col] == '--' or tabuleiro[(row + rowCasa)][col][0] != cor:
                            movPossiveis.append(((row + rowCasa), col))

        castleMov = self.castle(cor, posicaoAtual, tabuleiro, moveLogNotation)
        if castleMov[0] != ():
            movPossiveis.append(castleMov[0])
        if castleMov[1] != ():
            movPossiveis.append(castleMov[1])

        return movPossiveis
    
    def movCavalo(self, cor: str, posicaoAtual: tuple, tabuleiro: list) -> list:
        movPossiveis = []
        rowSentido = 1
        colSentido = 1
        for c in range(0, 4):
            row = posicaoAtual[0]
            col = posicaoAtual[1]
            if c % 2 == 0:
                row = row + (2 * rowSentido)
                colDireita = col + 1
                colEsquerda = col - 1
                rowSentido = -1
                if row > -1 and row < 8:
                    if colDireita < 8:
                        if tabuleiro[row][colDireita] == '--' or tabuleiro[row][colDireita][0] != cor:
                            movPossiveis.append((row, colDireita))
                    if colEsquerda > -1:
                        if tabuleiro[row][colEsquerda] == '--' or tabuleiro[row][colEsquerda][0] != cor:
                            movPossiveis.append((row, colEsquerda))
            else:
                col = col + (2 * colSentido)
                rowDireita = row + 1
                rowEsquerda = row - 1
                colSentido = -1
                if col > -1 and col < 8:
                    if rowDireita < 8:
                        if tabuleiro[rowDireita][col] == '--' or tabuleiro[rowDireita][col][0] != cor:
                            movPossiveis.append((rowDireita, col))
                    if rowEsquerda > -1:
                        if tabuleiro[rowEsquerda][col] == '--' or tabuleiro[rowEsquerda][col][0] != cor:
                            movPossiveis.append((rowEsquerda, col))

        return movPossiveis
