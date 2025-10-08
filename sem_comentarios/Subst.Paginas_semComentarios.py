from collections import deque

QUANTIDADE_QUADROS = 8

def posicao_pagina(quadros, pagina):
    for i, p in enumerate(quadros):
        if p == pagina:
            return i
    return -1

def simular_fifo(sequencia, qtd_quadros):
    quadros = [None] * qtd_quadros
    fila_indices = deque()
    proximo_livre = 0
    for pagina in sequencia:
        if posicao_pagina(quadros, pagina) != -1:
            continue
        if proximo_livre < qtd_quadros:
            quadros[proximo_livre] = pagina
            fila_indices.append(proximo_livre)
            proximo_livre += 1
        else:
            indice_vitima = fila_indices.popleft()
            quadros[indice_vitima] = pagina
            fila_indices.append(indice_vitima)
    return quadros

def simular_lru(sequencia, qtd_quadros):
    quadros = [None] * qtd_quadros
    ultima_vez_usada = {}
    proximo_livre = 0
    tempo = 0
    for pagina in sequencia:
        pos = posicao_pagina(quadros, pagina)
        if pos != -1:
            ultima_vez_usada[pagina] = tempo
        else:
            if proximo_livre < qtd_quadros:
                quadros[proximo_livre] = pagina
                ultima_vez_usada[pagina] = tempo
                proximo_livre += 1
            else:
                indice_vitima = -1
                pagina_vitima = None
                menor_tempo = 10**9
                for i, p in enumerate(quadros):
                    t = ultima_vez_usada.get(p, -1)
                    if t < menor_tempo:
                        menor_tempo = t
                        pagina_vitima = p
                        indice_vitima = i
                quadros[indice_vitima] = pagina
                if pagina_vitima in ultima_vez_usada:
                    del ultima_vez_usada[pagina_vitima]
                ultima_vez_usada[pagina] = tempo
        tempo += 1
    return quadros

def simular_mru(sequencia, qtd_quadros):
    quadros = [None] * qtd_quadros
    ultima_vez_usada = {}
    proximo_livre = 0
    tempo = 0
    for pagina in sequencia:
        pos = posicao_pagina(quadros, pagina)
        if pos != -1:
            ultima_vez_usada[pagina] = tempo
        else:
            if proximo_livre < qtd_quadros:
                quadros[proximo_livre] = pagina
                ultima_vez_usada[pagina] = tempo
                proximo_livre += 1
            else:
                indice_vitima = -1
                pagina_vitima = None
                maior_tempo = -1
                for i, p in enumerate(quadros):
                    t = ultima_vez_usada.get(p, -1)
                    if t > maior_tempo:
                        maior_tempo = t
                        pagina_vitima = p
                        indice_vitima = i
                quadros[indice_vitima] = pagina
                if pagina_vitima in ultima_vez_usada:
                    del ultima_vez_usada[pagina_vitima]
                ultima_vez_usada[pagina] = tempo
        tempo += 1
    return quadros

def posicao_humana(quadros, pagina):
    idx = posicao_pagina(quadros, pagina)
    return "N/A" if idx == -1 else idx + 1

def testar_sequencia(rotulo, sequencia, pagina_alvo):
    print(f"Sequência {rotulo} (página alvo = {pagina_alvo}):")
    quadros_fifo = simular_fifo(sequencia, QUANTIDADE_QUADROS)
    quadros_lru  = simular_lru(sequencia,  QUANTIDADE_QUADROS)
    quadros_mru  = simular_mru(sequencia,  QUANTIDADE_QUADROS)
    print(f"  FIFO -> quadro da página {pagina_alvo}: {posicao_humana(quadros_fifo, pagina_alvo)}  | quadros: {quadros_fifo}")
    print(f"  LRU  -> quadro da página {pagina_alvo}: {posicao_humana(quadros_lru,  pagina_alvo)}  | quadros: {quadros_lru}")
    print(f"  MRU  -> quadro da página {pagina_alvo}: {posicao_humana(quadros_mru,  pagina_alvo)}  | quadros: {quadros_mru}")
    print()

def main():
    seq_a = [4,3,25,8,19,6,25,8,16,35,45,22,8,3,16,25,7]
    seq_b = [4,5,7,9,46,45,14,4,64,7,65,2,1,6,8,45,14,11]
    seq_c = [4,6,7,8,1,6,10,15,16,4,2,1,4,6,12,15,16,11]
    testar_sequencia("a", seq_a, 7)
    testar_sequencia("b", seq_b, 11)
    testar_sequencia("c", seq_c, 11)

if __name__ == "__main__":
    main()
