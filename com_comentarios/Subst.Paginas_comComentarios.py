# Simulador de políticas de substituição de páginas: FIFO, LRU e MRU
# - Código simples, direto, apenas com biblioteca padrão.
# - Variáveis e comentários em português, como solicitado.
#
# Ideia geral:
#   - Mantemos um vetor 'quadros' com o conteúdo dos 8 quadros de memória.
#   - Para cada referência de página na sequência:
#       * Se a página já estiver nos quadros (acerto/HIT), atualizamos metadados quando necessário.
#       * Se não estiver (falta/MISS), inserimos ou substituímos conforme a política.
#
# Políticas:
#   - FIFO: remove a página que está há mais tempo na memória (a "mais antiga").
#           Implementação: uma fila (deque) de índices dos quadros.
#   - LRU : remove a menos recentemente usada.
#           Implementação: dicionário {pagina: tempo_da_ultima_vez_usada}.
#   - MRU : remove a mais recentemente usada.
#           Implementação: igual ao LRU, porém escolhe a vítima com MAIOR tempo recente.
#
# Ao final, imprimimos:
#   - Em qual quadro (1..8) ficou a página-alvo.
#   - O estado final dos quadros para cada política.

from collections import deque

# Quantidade de quadros (fixa em 8 conforme enunciado)
QUANTIDADE_QUADROS = 8

def posicao_pagina(quadros, pagina):
    """
    Procura a página no vetor de quadros.
    Retorna o índice (0..n-1) se encontrou; caso contrário, -1.
    """
    for i, p in enumerate(quadros):
        if p == pagina:
            return i
    return -1

def simular_fifo(sequencia, qtd_quadros):
    """
    Simula a política FIFO:
    - Se a página não está nos quadros (MISS) e há espaço, insere no próximo livre.
    - Se não há espaço, remove o quadro mais antigo (frente da fila) e coloca a nova página nele.
    """
    quadros = [None] * qtd_quadros
    fila_indices = deque()  # guarda a ordem de entrada (índices dos quadros)
    proximo_livre = 0       # aponta para o próximo quadro vazio

    for pagina in sequencia:
        # Verifica se já está na memória (HIT)
        if posicao_pagina(quadros, pagina) != -1:
            # FIFO não precisa atualizar nada em caso de HIT
            continue

        # MISS
        if proximo_livre < qtd_quadros:
            # Ainda há espaço: ocupa o próximo quadro livre
            quadros[proximo_livre] = pagina
            fila_indices.append(proximo_livre)
            proximo_livre += 1
        else:
            # Memória cheia: remove o mais antigo (frente da fila)
            indice_vitima = fila_indices.popleft()
            quadros[indice_vitima] = pagina
            # O índice usado volta para o fim da fila (agora é o mais "novo")
            fila_indices.append(indice_vitima)

    return quadros

def simular_lru(sequencia, qtd_quadros):
    """
    Simula a política LRU:
    - Mantém, para cada página carregada, o 'tempo' (posição na sequência) da última utilização.
    - A vítima é a página com MENOR 'ultima_vez_usada' (ou seja, a que está há mais tempo sem uso).
    """
    quadros = [None] * qtd_quadros
    ultima_vez_usada = {}   # mapeia página -> tempo da última referência
    proximo_livre = 0
    tempo = 0               # contador simples de tempo (índice da referência)

    for pagina in sequencia:
        pos = posicao_pagina(quadros, pagina)
        if pos != -1:
            # HIT: apenas atualiza a recência
            ultima_vez_usada[pagina] = tempo
        else:
            # MISS
            if proximo_livre < qtd_quadros:
                # Ainda há espaço nos quadros
                quadros[proximo_livre] = pagina
                ultima_vez_usada[pagina] = tempo
                proximo_livre += 1
            else:
                # Memória cheia: escolhe a vítima menos recente
                indice_vitima = -1
                pagina_vitima = None
                menor_tempo = 10**9  # número grande só para iniciar a busca

                # Percorre os quadros para achar quem tem a menor 'ultima_vez_usada'
                for i, p in enumerate(quadros):
                    t = ultima_vez_usada.get(p, -1)
                    if t < menor_tempo:
                        menor_tempo = t
                        pagina_vitima = p
                        indice_vitima = i

                # Substitui a vítima pela nova página
                quadros[indice_vitima] = pagina
                # Remove metadado da vítima (opcional, mas deixa o dicionário limpo)
                if pagina_vitima in ultima_vez_usada:
                    del ultima_vez_usada[pagina_vitima]
                # Registra a última vez usada da página recém-carregada
                ultima_vez_usada[pagina] = tempo

        tempo += 1  # avança o tempo a cada referência

    return quadros

def simular_mru(sequencia, qtd_quadros):
    """
    Simula a política MRU:
    - Mantém 'ultima_vez_usada' similar ao LRU.
    - A vítima é a página com MAIOR 'ultima_vez_usada' (a mais recentemente usada).
    """
    quadros = [None] * qtd_quadros
    ultima_vez_usada = {}   # mapeia página -> tempo da última referência
    proximo_livre = 0
    tempo = 0

    for pagina in sequencia:
        pos = posicao_pagina(quadros, pagina)
        if pos != -1:
            # HIT: atualiza recência
            ultima_vez_usada[pagina] = tempo
        else:
            # MISS
            if proximo_livre < qtd_quadros:
                quadros[proximo_livre] = pagina
                ultima_vez_usada[pagina] = tempo
                proximo_livre += 1
            else:
                # Memória cheia: escolhe a vítima mais recente
                indice_vitima = -1
                pagina_vitima = None
                maior_tempo = -1  # começa baixo para achar o maior

                # Percorre os quadros para achar quem tem a maior 'ultima_vez_usada'
                for i, p in enumerate(quadros):
                    t = ultima_vez_usada.get(p, -1)
                    if t > maior_tempo:
                        maior_tempo = t
                        pagina_vitima = p
                        indice_vitima = i

                # Substitui a vítima pela nova página
                quadros[indice_vitima] = pagina
                # Limpa metadados da vítima (opcional)
                if pagina_vitima in ultima_vez_usada:
                    del ultima_vez_usada[pagina_vitima]
                # Registra a recência da nova página
                ultima_vez_usada[pagina] = tempo

        tempo += 1  # avança o tempo

    return quadros

def posicao_humana(quadros, pagina):
    """
    Converte o índice interno (0..n-1) para numeração humana (1..n).
    Se a página não estiver nos quadros, retorna 'N/A'.
    """
    idx = posicao_pagina(quadros, pagina)
    return "N/A" if idx == -1 else idx + 1

def testar_sequencia(rotulo, sequencia, pagina_alvo):
    """
    Roda a mesma sequência nas três políticas, imprime:
      - Em qual quadro (1..8) ficou a página-alvo.
      - O conteúdo final dos quadros.
    """
    print(f"Sequência {rotulo} (página alvo = {pagina_alvo}):")

    quadros_fifo = simular_fifo(sequencia, QUANTIDADE_QUADROS)
    quadros_lru  = simular_lru(sequencia,  QUANTIDADE_QUADROS)
    quadros_mru  = simular_mru(sequencia,  QUANTIDADE_QUADROS)

    print(f"  FIFO -> quadro da página {pagina_alvo}: {posicao_humana(quadros_fifo, pagina_alvo)}  | quadros: {quadros_fifo}")
    print(f"  LRU  -> quadro da página {pagina_alvo}: {posicao_humana(quadros_lru,  pagina_alvo)}  | quadros: {quadros_lru}")
    print(f"  MRU  -> quadro da página {pagina_alvo}: {posicao_humana(quadros_mru,  pagina_alvo)}  | quadros: {quadros_mru}")
    print()

def main():
    """
    Sequências do enunciado + página-alvo para cada uma:
      (a) alvo = 7
      (b) alvo = 11
      (c) alvo = 11
    """
    seq_a = [4,3,25,8,19,6,25,8,16,35,45,22,8,3,16,25,7]
    seq_b = [4,5,7,9,46,45,14,4,64,7,65,2,1,6,8,45,14,11]
    seq_c = [4,6,7,8,1,6,10,15,16,4,2,1,4,6,12,15,16,11]

    testar_sequencia("a", seq_a, 7)
    testar_sequencia("b", seq_b, 11)
    testar_sequencia("c", seq_c, 11)

if __name__ == "__main__":
    main()
