import random, copy, sys, pygame
from pygame.locals import*

ancho = 7
altura = 6
assert ancho >= 4 and altura >= 4
dificultad = 2
fichat = 60
fps = 30
windowwidth = 800
windowheight = 700
xmargin = int((windowwidth - ancho * fichat)/2)
ymargin = int((windowheight - altura * fichat)/2)
blue = (100, 149, 237)
usuario = "usuario"
computadora = "computadora"
none = None
morado = "morado"
verde = "verde"

def main():
    global clock, window, morados, verdes, fichamoradaimg, fichaverdeimg, tableroimg, ganasteimg, ganasterect, perdisteimg, empateimg, instruccionesimg, instruccionesrect
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption("Connect 4!")

    morados = pygame.Rect(int(fichat / 2), windowheight - int(3 * fichat / 2), fichat, fichat)
    verdes = pygame.Rect(windowwidth - int(3 * fichat / 2), windowheight - int(3 * fichat/ 2), fichat, fichat)
    fichamoradaimg = pygame.image.load('ficha_morada.png')
    fichamoradaimg = pygame.transform.smoothscale(fichamoradaimg, (fichat, fichat))
    fichaverdeimg = pygame.image.load('ficha_verde.png')
    fichaverdeimg = pygame.transform.smoothscale(fichaverdeimg, (fichat, fichat))
    tableroimg = pygame.image.load('tablero.png')
    tableroimg = pygame.transform.smoothscale(tableroimg, (fichat, fichat))
    ganasteimg = pygame.image.load('ganaste.png')
    perdisteimg = pygame.image.load('perdiste.png')
    empateimg = pygame.image.load('empate.png')
    ganasterect = ganasteimg.get_rect()
    ganasterect.center = (int(windowwidth / 2), int(windowheight / 2))
    instruccionesimg = pygame.image.load('instrucciones.png')
    instruccionesimg = pygame.transform.smoothscale(instruccionesimg, (150, 120))
    instruccionesrect = instruccionesimg.get_rect()
    instruccionesrect.left = morados.right + 10
    instruccionesrect.centery = morados.centery - 10
    juego= True

    while True:
        run(juego)
        juego = False


def run(juego):
    if juego:
        turno = computadora
        mostrarinstrucciones = True
    else:
        if random.randint(0, 1) == 0:
            turno = computadora
        else:
            turno = usuario
        mostrarinstrucciones = False
    tablero = nuevotablero()
    while True:
        if turno == usuario:
            turnousuario(tablero, mostrarinstrucciones)
            if mostrarinstrucciones:
                mostrarinstrucciones = False
            if ganador(tablero, morado):
                imagen = ganasteimg
                break
            turno = computadora
        else:
            columna = turnocomputadora(tablero)
            animarcomputadora(tablero, columna)
            hacerjugada(tablero, verde, columna)
            if ganador(tablero, verde):
                imagen = perdisteimg
                break
            turno = usuario
        if tablerolleno(tablero):
            imagen = empateimg
            break
    while True:
        formartablero(tablero)
        window.blit(imagen, ganasterect)
        pygame.display.update()
        clock.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def hacerjugada(tabla, jugador, columna):
    menor = menorespaciolibre(tabla,columna)
    if menor != -1:
        tabla[columna][menor] = jugador


def nuevotablero():
    tabla = []
    for x in range(ancho):
        tabla.append([none] * altura)
    return tabla


def formartablero(tabla, fichaextra=None):
    window.fill(blue)
    espaciorect = pygame.Rect(0, 0, fichat, fichat)
    for x in range(ancho):
        for y in range(altura):
            espaciorect.topleft = (xmargin + (x * fichat), ymargin + (y * fichat))
            if tabla[x][y] == morado:
                window.blit(fichamoradaimg, espaciorect)
            elif tabla[x][y] == verde:
                window.blit(fichaverdeimg, espaciorect)
    if fichaextra != None:
        if fichaextra['color'] == morado:
            window.blit(fichamoradaimg, (fichaextra['x'], fichaextra['y'], fichat, fichat))
        elif fichaextra['color'] == verde:
            window.blit(fichaverdeimg, (fichaextra['x'], fichaextra['y'], fichat, fichat))
    for x in range(ancho):
        for y in range(altura):
            espaciorect.topleft = (xmargin + (x * fichat), ymargin + (y * fichat))
            window.blit(tableroimg, espaciorect)
    window.blit(fichamoradaimg, morados)
    window.blit(fichaverdeimg, verdes)


def turnousuario(tabla, primermovimiento):
    moverficha = False
    fichax, fichay = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not moverficha and morados.collidepoint(event.pos):
                moverficha = True
                fichax, fichay = event.pos
            elif event.type == MOUSEMOTION and moverficha:
                fichax, fichay = event.pos
            elif event.type == MOUSEBUTTONUP and moverficha :
                if fichay < 190 and 210 < fichax < 590:
                    columna = int((fichax - xmargin) / fichat)
                    if movimientovalido(tabla,columna):
                        animarficha(tabla, columna, morado)
                        tabla[columna][menorespaciolibre(tabla,columna)] = morado
                        formartablero(tabla)
                        pygame.display.update()
                        return
                fichax, fichay = None, None
                moverficha = False
        if fichax != None and fichay != None:
            formartablero(tabla, {'x':fichax - int(fichat / 2),'y': fichay - int(fichat / 2), 'color': morado})
        else:
            formartablero(tabla)
        if primermovimiento:
            window.blit(instruccionesimg, instruccionesrect)
        pygame.display.update()
        clock.tick()


def animarficha(tabla, columna, color):
    x = xmargin + columna * fichat
    y = ymargin - fichat
    velocidad = 0.5
    menor = menorespaciolibre(tabla, columna)
    while True:
        y += int(velocidad)
        velocidad += 0.5
        if int((y - ymargin) / fichat) >= menor:
            return
        formartablero(tabla, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        clock.tick()


def tablerolleno(tabla):
    for x in range(ancho):
        for y in range(altura):
            if tabla[x][y] == none:
                return False
    return True


def animarcomputadora(tabla, columna):
    x = verdes.left
    y = verdes.top
    rapidez = 0.5
    while y > (ymargin - fichat):
        y -= int(rapidez)
        rapidez += 0.5
        formartablero(tabla, {'x': x, 'y': y, 'color': verde})
        pygame.display.update()
        clock.tick()
    y = ymargin - fichat
    rapidez = 0.5
    while x > (xmargin + columna * fichat):
        x -= int(rapidez)
        rapidez += 0.5
        formartablero(tabla, {'x': x, 'y': y, 'color': verde})
        pygame.display.update()
        clock.tick()
    animarficha(tabla, columna, verde)


def turnocomputadora(tabla):
    posibles = posiblesmovimientos(tabla, verde, dificultad)
    eficiencia = -1
    for i in range(ancho):
        if posibles[i] > eficiencia and movimientovalido(tabla, i):
            eficiencia = posibles[i]
    mejores = []
    for i in range(len(posibles)):
        if posibles[i] == eficiencia and movimientovalido(tabla, i):
            mejores.append(i)
    return random.choice(mejores)


def menorespaciolibre(tabla, columna):
    for y in range(altura-1, -1, -1):
        if tabla[columna][y] == none:
            return y
    return -1


def movimientovalido(tabla, columna):
    if columna < 0 or columna >= ancho or tabla[columna][0] != None:
        return False
    return True


def posiblesmovimientos(tabla, espacio, prever):
    if prever == 0 or tablerolleno(tabla):
        return [0] * ancho
    if espacio == morado:
        oponente = verde
    else:
        oponente = morado
    posibles = [0] * ancho
    for primermovimiento in range(ancho):
        copiatablero = copy.deepcopy(tabla)
        if not movimientovalido(copiatablero, primermovimiento):
            continue
        hacerjugada(copiatablero, espacio, primermovimiento)
        if ganador(copiatablero, espacio):
            posibles[primermovimiento] = 1
            break
        else:
            if tablerolleno(copiatablero):
                posibles[primermovimiento] = 0
            else:
                for contramov in range(ancho):
                    copiatablero2 = copy.deepcopy(copiatablero)
                    if not movimientovalido(copiatablero2, contramov):
                        continue
                    hacerjugada(copiatablero2, oponente, contramov)
                    if ganador(copiatablero2, oponente):
                        posibles[primermovimiento] = -1
                        break
                    else:
                        resultados = posiblesmovimientos(copiatablero2, espacio, prever - 1)
                        posibles[primermovimiento] += ((sum(resultados) / ancho) / altura)
    return posibles


def ganador(tabla, espacio):
    for x in range(ancho - 3):
        for y in range(altura):
            if tabla[x][y] == espacio and tabla[x + 1][y] == espacio and tabla[x + 2][y] == espacio and tabla[x + 3][y] == espacio:
                return True
    for x in range(ancho):
        for y in range(altura - 3):
            if tabla[x][y] == espacio and tabla[x][y + 1] == espacio and tabla[x][y + 2] == espacio and tabla[x][y + 3] == espacio:
                return True
    for x in range(ancho - 3):
        for y in range(3, altura):
            if tabla[x][y] == espacio and tabla[x + 1][y - 1] == espacio and tabla[x + 2][y - 2] == espacio and tabla[x + 3][y - 3] == espacio:
                return True
    for x in range(ancho - 3):
        for y in range(altura - 3):
            if tabla[x][y] == espacio and tabla[x + 1][y + 1] == espacio and tabla[x + 2][y + 2] == espacio and tabla[x + 3][y + 3] == espacio:
                return True
    return False


if __name__ == '__main__':
    main()
