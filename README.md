# Trabalho 2

**Grupo:** Grupo 02  
**Aluno:** Marcelo - Cartão: 587562
**Aluno:** Heitor - Cartão: 577397

---

## Bibliotecas necessárias

Nenhuma biblioteca externa.

---

## Avaliação no Tic-Tac-Toe Misere

Implementamos a poda alfa-beta com profundidade -1 (sem) em `tttm_minimax.py`, porque a árvore do jogo da velha tem no máximo 9 jogadas e calcula em tempo suficiente.

Respostas das perguntas do enunciado:

1. **O minimax sempre ganha ou empata jogando contra o randomplayer?**  
   Sim. fizemos quem chegava a 10 primeiro e deu 10:8:0 (v:e:d)

2. **O minimax sempre empata consigo mesmo?**  
   Sim, deterministicamente.

3. **O minimax não perde para você quando você usa a sua melhor estratégia?**  
   Não. Perdemos pra ele até aprender a empatar.

---

## Avaliação no Othello

### 1. Heurística Customizada (`othello_minimax_custom.py`)

Para fazer a heurística customizada, nos inspiramos [nesse artigo](https://github.com/Jules-Lion/kurwa/blob/master/Dokumentation/An%20Analysis%20of%20Heuristics%20in%20Othello.pdf) :

1. **Cantos:** Canto no Othello é estavel, então nunca vai ser reconquistada pelo outro. Demos peso +100 pra quem tem o canto. Por consequência, as casas adjacentes devem ser penalizadas (penalizamos -25 pra lateral e -50 diagonal).
2. **Mobilidade:** Calculamos os movimentos válidos do jogador. Ter mais opções de jogada que o oponente pode forçar ele a ficar sem jogadas boas ou passar a vez.
3. **Paridade de peças por fase do jogo:** No começo do jogo (mais de 40 casas vazias), ter muitas peças é ruim porque tem muitos alvos. Então botamos peso negativo pra número de peças no início. Conforme o tabuleiro vai enchendo (entre 40 e 16), o peso fica positivo, e no finalzinho (menos de 16 casas vazias) vira prioridade pegar o máximo de peças.

---

### 2. Critério de parada do agente

- Nos arquivos (`count` e `mask`) usamos profundidade 5 (`DEPTH = 5`). Roda bem abaixo dos 5 segundos.
- No agente do torneio (`tournament_agent.py`) usamos busca com **aprofundamento iterativo**, vai aumentando profundidade 1, 2, 3... até dar `TIME_LIMIT = 4`. Se o tempo acaba no meio de uma profundidade, a exceção `SearchTimeOut` para a busca e ele devolve a melhor jogada da última profundidade que terminou completa.

---

### 3. Resultado do Mini-Torneio

Com 6 partidas completas pelo servidor entre as 3 heurísticas (com profundidade 5 cada uma). Os resultados foram:

| Partida                                       | Pretas (B)       | Brancas (W)      |   Quem venceu   | Placar  |
| :-------------------------------------------- | :--------------- | :--------------- | :-------------: | :-----: |
| **Contagem X Valor posicional**               | Contagem         | Valor posicional |  **Contagem**   | 37 a 27 |
| **Valor posicional X Contagem**               | Valor posicional | Contagem         |  **Contagem**   | 26 a 38 |
| **Contagem X Heurística customizada**         | Contagem         | Customizada      | **Customizada** | 10 a 54 |
| **Heurística customizada X Contagem**         | Customizada      | Contagem         | **Customizada** | 63 a 0  |
| **Valor posicional X Heurística customizada** | Valor posicional | Customizada      | **Customizada** | 4 a 60  |
| **Heurística customizada X Valor posicional** | Customizada      | Valor posicional | **Customizada** | 41 a 23 |

**Quem foi melhor:**  
A **Heurística Customizada** ganhou. Ganhou as 4 partidas (tanto jogando de pretas quanto de brancas), e até com 63 a 0. A contagem ficou em segundo lugar ganhando da posicional nas duas vezes.

---

### 4. Implementação do Torneio (`tournament_agent.py`)

Pro torneio juntei a melhor configuração que funcionou nos testes:

- Usa a heurística customizada pra avaliar as folhas.
- Usa aprofundamento iterativo com limite de 4 segundos.
- Adicionamos uma ordenação prévia de jogadas (`order_key`): ele olha uma matriz estática simples e avalia primeiro os movimentos em casas boas (como cantos) antes dos ruins. Isso faz a poda alfa-beta cortar muito mais ramos logo no início da busca e consegue descer mais níveis de profundidade dentro dos 4 segundos.
- Contra o jogador aleatório no servidor de teste, o agente fechou a partida em **64 a 0**, ocupando o tabuleiro inteiro.
