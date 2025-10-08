Políticas de Substituição de Páginas — FIFO, LRU e MRU

Disciplina: Performance em Sistemas Ciber-Físicos
Integrantes: Gastão Eduardo Santos Borges • Caio Eduardo Lamoglia • Caetano Goulart Padoin
Data: 08/10/2025

Objetivo

Implementar e explicar, em um vídeo de até 10 minutos, três políticas de substituição de páginas (FIFO, LRU e MRU). Rodar os algoritmos com 8 quadros nas sequências fornecidas e responder: “Em qual quadro a página X ficará ao final?” Também discutir qual política tende a ser melhor e justificar.

Resumo dos algoritmos

FIFO (First-In, First-Out): remove a página há mais tempo na memória. Simples e previsível; pode sofrer anomalia de Belady.

LRU (Least Recently Used): remove a menos recentemente usada; geralmente vai melhor quando há localidade temporal.

MRU (Most Recently Used): remove a mais recentemente usada; útil em padrões específicos, no geral perde para LRU.

Estrutura do repositório 
.
├─ com_comentarios/
│  └─ Subst.Paginas_comComentarios.py   
├─ sem_comentarios/
│  └─ Subst.Paginas_semComentarios.py   
└─ README.md


As duas versões têm a mesma lógica; muda apenas a presença de comentários.

Requisitos

Python 3.8+

Sem dependências externas (somente biblioteca padrão)

Como executar

Entrega principal (sem comentários):

python3 sem_comentarios/Subst.Paginas_semComentarios.py


Versão comentada:

python3 com_comentarios/Subst.Paginas_comComentarios.py


A saída mostra, para cada sequência, o quadro (1..8) em que a página-alvo termina e o estado final dos quadros.

Sequências de teste (8 quadros) e respostas

Interpretação: “qual quadro possuirá a página X?” → posições 1..8.

(a) 4,3,25,8,19,6,25,8,16,35,45,22,8,3,16,25,7 — página 7

FIFO: 5

LRU: 6

MRU: 3

(b) 4,5,7,9,46,45,14,4,64,7,65,2,1,6,8,45,14,11 — página 11

FIFO: 6

LRU: 3

MRU: 7

(c) 4,6,7,8,1,6,10,15,16,4,2,1,4,6,12,15,16,11 — página 11

FIFO: 5

LRU: 6

MRU: 8

Qual política é “melhor”?

Depende do padrão de acesso. Em cenários com localidade temporal, LRU tende a ter menos faltas por manter páginas usadas recentemente. FIFO é simples, mas pode apresentar anomalias. MRU pode funcionar quando a última página usada provavelmente não será reutilizada logo em seguida.
Conclusão do grupo: para uso geral, LRU é a mais adequada entre as três.

Como o código funciona (resumo rápido)

quadros: lista com os 8 quadros de memória.

FIFO: usa deque para controlar a ordem de entrada e substituir o mais antigo.

LRU/MRU: usam um dicionário com a última vez usada por página; a vítima é a de menor (LRU) ou maior (MRU) marca de tempo.

Ao fim de cada sequência, o programa imprime o quadro da página-alvo e o estado final dos quadros.

Vídeo (não listado)

Link do YouTube: [inserir aqui]

Sugestão de roteiro (≤ 10 min):

objetivo e integrantes (~20s)

teoria breve FIFO/LRU/MRU (~3 min)

visão do arquivo (mostrar a versão com comentários) e estruturas usadas (~3 min)

execução nas três sequências e leitura dos resultados (~2 min)

fechamento: por que LRU costuma vencer (~1–2 min)