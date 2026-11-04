# Trabalho 2: Busca com Adversários
**Disciplina:** INF01048 – Inteligência Artificial (Turma A)  
**Professor:** Lucas Rafael Costella Pessutto  
**Grupo:** T2-Grupo 02  

### Integrantes:
- **Nome:** Marcelo  
  **Cartão de Matrícula:** 00587562  
  **Turma:** A  

---

## 1. Bibliotecas e Requisitos
A implementação utiliza estritamente módulos da biblioteca padrão do Python (`random`, `time`, `typing`).
- Não é necessária a instalação de nenhuma biblioteca externa adicional para a execução dos agentes e do servidor.
- Ambiente de execução testado: Python 3.9+ / Python 3.11 no Windows e Linux.

---

## 2. Avaliação no Jogo da Velha Invertido (Tic-Tac-Toe Misere)
O agente para o Tic-Tac-Toe Misere foi implementado no módulo `tttm_minimax.py`, invocando o algoritmo minimax com poda alfa-beta com profundidade ilimitada (`max_depth = -1`), utilizando a função de utilidade terminal:
- $+1.0$ em caso de vitória do jogador;
- $-1.0$ em caso de derrota (quando o jogador alinha 3 peças e perde segundo as regras misere);
- $0.0$ em caso de empate.

### Respostas às Questões do Enunciado:
1. **O minimax sempre ganha ou empata jogando contra o randomplayer?**  
   **Sim.** Em todas as simulações executadas contra o jogador aleatório, o agente nunca perdeu nenhuma partida, obtendo sempre vitórias ou empates forçados.
2. **O minimax sempre empata consigo mesmo?**  
   **Sim.** Em jogo perfeito no Tic-Tac-Toe Misere com o primeiro jogador abrindo no centro `(1, 1)`, a partida termina inevitavelmente em empate ($0 \times 0$).
3. **O minimax não perde para você quando você usa a sua melhor estratégia?**  
   **Sim.** Como o espaço de estados do jogo da velha é pequeno (profundidade máxima 9) e o algoritmo explora a árvore completa com poda alfa-beta até os nós terminais, o agente joga de forma estritamente ótima, impossibilitando qualquer derrota contra um jogador humano.

---

## 3. Avaliação no Othello (Reversi)

### 3.1 Heurística Customizada (`othello_minimax_custom.py`)
A função de avaliação customizada (`evaluate_custom`) combina quatro componentes estratégicos consagrados na literatura de Othello:

1. **Controle de Cantos e Regiões Adjacentes (Corners & Danger Zones):**
   - Os 4 cantos `(0,0), (0,7), (7,0), (7,7)` são posições estáveis imutáveis e recebem peso alto ($+100$).
   - As casas vizinhas imediatas (zonas X e C) recebem penalidade severa ($-50$ e $-25$) enquanto o respectivo canto estiver vazio, pois concedem a quina ao oponente. Caso o canto já pertença ao jogador, essas posições deixam de ser penalizadas.
2. **Matriz de Valores Posicionais (`BASE`):**
   - Atribui pesos táticos para bordas e centro do tabuleiro.
3. **Mobilidade Relativa (`mobility`):**
   - Calculada como a diferença percentual de movimentos legais disponíveis:  
     $$\text{mobilidade} = 100 \times \frac{\text{movimentos}_{\text{jogador}} - \text{movimentos}_{\text{oponente}}}{\text{movimentos}_{\text{jogador}} + \text{movimentos}_{\text{oponente}}}$$
   - Restringir as opções do adversário força jogadas fracas ou passagem de vez.
4. **Ponderação Dinâmica de Paridade de Peças conforme a Fase do Jogo:**
   - **Abertura/Início (mais de 40 casas vazias):** Peso de diferença de peças negativo ($-0.5$), incentivando manter poucas peças expostas.
   - **Meio de jogo (entre 16 e 40 casas vazias):** Peso moderado ($0.5$).
   - **Fim de jogo (16 ou menos casas vazias):** Peso alto ($4.0$), priorizando maximizar a quantidade final de peças para a vitória.

**Fontes consultadas:**
- Artigos clássicos de estratégias de Othello (Sannidhanam & Annamalai, *An Analysis of Heuristics in Othello*, Stanford University). A heurística combina a ideia de fases dinâmicas do jogo e mobilidade relativa com a ponderação clássica de cantos.

### 3.2 Critério de Parada do Agente
- **Profundidade Fixa:** Nas heurísticas de Contagem e Máscara Posicional, foi utilizada profundidade fixa de 5 níveis (`DEPTH = 5`), garantindo respostas em fração de segundo.
- **Aprofundamento Iterativo (Iterative Deepening Search - IDS):** No agente de torneio (`tournament_agent.py`), a busca itera de $d=1, 2, \dots$ com controle de tempo (`TIME_LIMIT = 4` segundos). O tempo limite de 4 segundos garante uma margem de segurança segura em relação ao limite estipulado pelo servidor (5 segundos), interrompendo a busca graciosamente caso o tempo se esgote através da exceção `SearchTimeOut`.

### 3.3 Resultados do Mini-Torneio entre as Heurísticas
Foram executadas as 6 partidas regulamentares entre os algoritmos com as três heurísticas implementadas:

| Confronto | Jogador Pretas (B) | Jogador Brancas (W) | Vencedor | Placar Final |
| :--- | :--- | :--- | :---: | :---: |
| **Contagem X Valor posicional** | Contagem | Valor posicional | **Contagem** | **37 a 27** |
| **Valor posicional X Contagem** | Valor posicional | Contagem | **Contagem** | **26 a 38** |
| **Contagem X Heurística customizada** | Contagem | Heurística customizada | **Customizada** | **10 a 54** |
| **Heurística customizada X Contagem** | Heurística customizada | Contagem | **Customizada** | **63 a 0** |
| **Valor posicional X Heurística customizada** | Valor posicional | Heurística customizada | **Customizada** | **4 a 60** |
| **Heurística customizada X Valor posicional** | Heurística customizada | Valor posicional | **Customizada** | **41 a 23** |

#### Conclusão da Avaliação:
A **Heurística Customizada** foi a mais bem-sucedida de forma incontestável:
- **100% de aproveitamento** (venceu todas as 4 partidas em que participou, tanto de Pretas quanto de Brancas).
- Conquistou vitórias expressivas, incluindo placares de **63 a 0** contra a heurística de Contagem e **60 a 4** contra a Máscara Posicional.

---

## 4. Agente do Torneio (`tournament_agent.py`)
A implementação escolhida para o torneio incorpora as seguintes melhorias:
1. **Heurística Customizada Multicritério:** Utiliza a função `evaluate_custom` como avaliador de folhas.
2. **Busca com Aprofundamento Iterativo (IDS):** Começa em profundidade 1 e avança sucessivamente enquanto houver tempo restante, retornando sempre a melhor jogada do nível completamente explorado anterior caso ocorra timeout.
3. **Ordenação Prévia de Movimentos (`order_key`):** Utiliza uma matriz de prioridades das posições (cantos primeiro, evitando casas de risco) para ordenar os sucessores na raiz e nos nós da busca, aumentando drasticamente o número de cortes pela poda alfa-beta e permitindo alcançar profundidades maiores no mesmo intervalo de tempo.
4. **Controle de Tempo Seguro:** `TIME_LIMIT = 4.0` segundos, mantendo o consumo de memória estritamente baixo e sem criação de threads/processos em segundo plano.
