# Trabalho 2 - Inteligência Artificial (2026/2)
**Professor:** Lucas Pessutto  
**Grupo:** T2-Grupo 02  
**Aluno:** Marcelo - Cartão: 00587562 - Turma A  

---

## Bibliotecas necessárias
Nenhuma biblioteca externa. Só usei os módulos padrão do próprio Python (`random`, `time`, `typing`). Roda liso no Python 3.9+.

---

## Avaliação no Tic-Tac-Toe Misere

Implementei a poda alfa-beta com profundidade ilimitada (`max_depth = -1`) no `tttm_minimax.py`, porque a árvore do jogo da velha tem no máximo 9 jogadas e calcula bem rápido.

Respostas das perguntas do enunciado:

1. **O minimax sempre ganha ou empata jogando contra o randomplayer?**  
   Sim. Botei pra rodar contra o `randomplayer` e ele nunca perdeu nenhuma. Quando o random faz alguma burrada logo no início (tipo jogar na ponta), o minimax pune e ganha. Se o random não errar tão feio, termina em empate.

2. **O minimax sempre empata consigo mesmo?**  
   Sim, sempre. Se você botar o minimax jogando contra ele mesmo, a primeira jogada dele é obrigatoriamente no meio `(1, 1)` e a partir daí os dois jogam perfeito, terminando sempre em empate 0 a 0.

3. **O minimax não perde para você quando você usa a sua melhor estratégia?**  
   Não perde de jeito nenhum. Tentei jogar de tudo que é jeito pelo `server.py` no terminal. Se eu jogar certinho dá empate, e se eu bobear em alguma casa ele ganha na hora.

---

## Avaliação no Othello

### 1. Heurística Customizada (`othello_minimax_custom.py`)
Para fazer a heurística customizada, misturei três ideias básicas de estratégia de Othello:

1. **Cantos e vizinhança:** Canto no Othello é peça estável: uma vez conquistado, ele nunca mais pode ser virado pelo outro jogador até o fim da partida. Por isso demos peso +100 pra quem controla o canto. Por outro lado, penalizei fortemente jogar nas casas coladas num canto vazio: botei peso -50 pra casa na diagonal e -25 pras casas vizinhas da borda. Se você jogar ali com o canto ainda livre, você praticamente entrega o canto de bandeja pro adversário.
2. **Mobilidade:** Contei quantos movimentos válidos cada jogador tem na vez. Ter mais opções de jogada que o oponente é bom porque força ele a ficar sem jogadas boas ou até passar a vez.
3. **Paridade de peças por fase do jogo:** No começo do jogo (mais de 40 casas vazias), ter muitas peças na verdade é ruim porque você vira alvo fácil. Então botei peso levemente negativo pra número de peças no início. Conforme o tabuleiro vai enchendo (meio de jogo), o peso fica positivo, e no finalzinho (menos de 16 casas vazias) vira prioridade máxima pegar o máximo de peças possível pra garantir a vitória.

**Fontes:** Dei uma olhada nas ideias do artigo clássico de Othello da Universidade de Washington (*An Analysis of Heuristics in Othello*, do Sannidhanam e Annamalai) e em guias básicos de estratégia de Reversi sobre controle de cantos e mobilidade. Peguei esses conceitos gerais e calibrei os pesos na mão testando contra as outras heurísticas.

---

### 2. Critério de parada do agente
Usei profundidade máxima fixa de 5 (`DEPTH = 5`). O algoritmo avalia os lances com folga dentro do limite de 5 segundos estipulado pelo servidor.

---

### 3. Resultado do Mini-Torneio

Rodei as 6 partidas completas pelo servidor entre as 3 heurísticas (com profundidade 5 cada uma). Os resultados foram:

| Partida | Pretas (B) | Brancas (W) | Quem venceu | Placar |
| :--- | :--- | :--- | :---: | :---: |
| **Contagem X Valor posicional** | Contagem | Valor posicional | **Contagem** | 37 a 27 |
| **Valor posicional X Contagem** | Valor posicional | Contagem | **Contagem** | 26 a 38 |
| **Contagem X Heurística customizada** | Contagem | Customizada | **Customizada** | 10 a 54 |
| **Heurística customizada X Contagem** | Customizada | Contagem | **Customizada** | 63 a 0 |
| **Valor posicional X Heurística customizada** | Valor posicional | Customizada | **Customizada** | 4 a 60 |
| **Heurística customizada X Valor posicional** | Customizada | Valor posicional | **Customizada** | 41 a 23 |

**Quem foi melhor:**  
A **Heurística Customizada** ganhou disparado. Ganhou as 4 partidas que jogou (tanto jogando de pretas quanto de brancas), com placares como 63 a 0 contra a contagem e 60 a 4 contra a posicional. A contagem ficou em segundo lugar ganhando da posicional nas duas vezes.
