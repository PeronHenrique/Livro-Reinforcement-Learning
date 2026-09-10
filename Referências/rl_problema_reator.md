# Problema de Aprendizagem por Reforço — Operação de um Reator

## 1. Descrição do problema

Considere um sistema de produção química baseado em um reator no qual uma matéria-prima é convertida em um produto de interesse.

A cada instante de tempo, o sistema recebe uma **quantidade fixa de energia disponível**. Essa energia deve ser distribuída entre diferentes atividades operacionais:

- aquisição de matéria-prima;
- aquecimento do reator;
- ativação de sistemas auxiliares;
- transporte do produto final.

O objetivo do agente de Reinforcement Learning é determinar, a cada instante, como utilizar os recursos disponíveis para **maximizar o lucro acumulado ao longo do tempo**.

O problema é inspirado no exemplo 3.1 de bioreator apresentado em *Reinforcement Learning: An Introduction*, de Richard S. Sutton e Andrew G. Barto, mas constitui uma formulação própria para estudo.


## 2. Formulação como problema de Reinforcement Learning

O problema pode ser modelado como um **Processo de Decisão de Markov (MDP)**:

$$
M = (S, A, P, R, \gamma)
$$

onde:

- $S$ representa o conjunto de estados possíveis;
- $A$ representa o conjunto de ações possíveis;
- $P$ representa a dinâmica do sistema;
- $R$ representa a recompensa;
- $\gamma$ representa o fator de desconto.

Em cada instante $t$, o agente observa o estado $S_t$, escolhe uma ação $A_t$, o sistema evolui para um novo estado $S_{t+1}$ e o agente recebe uma recompensa $R_{t+1}$.


# 3. Estado

O estado deve representar as informações necessárias para que o agente consiga tomar uma decisão sobre a utilização da energia e a operação do processo.

Um possível vetor de estado é:

$$
S_t = [E_t, M_t, P_t, p^M_t, p^P_t, p^E_t T_t, AUX_t, C_t]
$$

onde:

| Variável | Descrição |
|---|---|
| $E_t$ | Energia disponível no instante $t$ |
| $M_t$ | Estoque de matéria-prima |
| $P_t$ | Estoque de produto |
| $p^M_t$ | Preço da matéria-prima |
| $p^P_t$ | Preço do produto |
| $p^E_t$ | Preço da energia |
| $T_t$ | Temperatura atual do reator |
| $AUX_t$ | Nível atual dos sistemas auxiliares |
| $C_t$ | Capacidade ou estado relacionado ao transporte |

A representação final do estado pode ser expandida conforme novos aspectos do processo sejam incorporados.



# 4. Ações

A ação representa as decisões tomadas pelo agente em cada instante.

Uma possibilidade é utilizar uma ação vetorial:

$$
A_t = [E^{raw}_t, E^{heat}_t, E^{aux}_t, E^{conersion}_t, E^{transport}_t]
$$

onde:

- $E^{raw}_t$ — energia destinada à aquisição de matéria-prima;
- $E^{heat}_t$ — energia destinada ao aquecimento;
- $E^{aux}_t$ — energia destinada aos sistemas auxiliares;
- $E^{conersion}_t$ — energia destinada ao processo de conversão da matéria-prima;
- $E^{transport}_t$ — energia destinada ao transporte.

A energia deve obedecer à restrição:

$$
E^{raw}_t + E^{heat}_t + E^{aux}_t + E^{conersion}_t + E^{transport}_t \leq E_t
$$

Caso toda a energia disponível deva ser utilizada:

$$
E^{raw}_t + E^{heat}_t + E^{aux}_t + E^{conersion}_t + E^{transport}_t = E_t
$$

A ação também pode ser representada por valores-alvo, como temperatura e nível dos sistemas auxiliares, enquanto um controlador de nível inferior realiza a distribuição efetiva da energia.


# 5. Aquecimento

O aquecimento influencia a velocidade da conversão da matéria-prima em produto.

De forma simplificada:

$$
r_{conversion} = f(T_t)
$$

onde $r_{conversion}$ representa a taxa de conversão.

Aumentar a temperatura pode aumentar a velocidade de conversão, mas também pode reduzir a eficiência energética do processo.

Uma representação simplificada poderia ser:

$$
\eta^T_t = f(T_t)
$$

com uma relação em que temperaturas muito elevadas apresentam menor eficiência.

A temperatura varia proporcionalmente com a diferença entre a energia aplicada e a energia perdida por radiação, a energia perdida por radiação é proporcional a temperatura:

$$
T_{t+1} = T_t + C_{heating} (E^{heat}_t - C_{rad} T_t)  
$$

O sistema possui limite da energia que pode ser usada para o aquecimento:

$$
0 \leq E^{heat}_t \leq E^{heat}_{max} 
$$


# 6. Sistemas auxiliares

Os sistemas auxiliares têm como função aumentar a eficiência da geração do produto desejado.

Podemos representar sua influência por:

$$
\eta^{aux}_t = f(AUX_t)
$$

A produção efetiva pode então depender tanto da temperatura quanto dos sistemas auxiliares.

O sistema possui restrições físicas sobre a velocidade com que determinados parâmetros podem ser alterados e os valores máximos.

Para os sistemas auxiliares:

$$
|AUX_{t+1} - AUX_t| \leq \Delta AUX_{max}
$$

$$
0 \leq E^{aux}_t \leq E^{aux}_{max} 
$$

Essas restrições tornam o problema mais próximo de um sistema físico real, no qual o agente não pode realizar mudanças instantâneas.



# 7. Estoque de matéria-prima

A matéria-prima pode ser comprada utilizando parte da energia disponível.

Se $q^{raw}_t$ representa a quantidade adquirida:

$$
M_{t+1} = M_t + q^{raw}_t - q^{conversion}_t
$$

O estoque não pode ser negativo e possui uma capacidade máxima:

$$
C_M \geq M_t \geq 0
$$

A quantidade comprada depende da energia destinada à aquisição .

Por exemplo:

$$
q^{raw}_t = {C_{raw}}{E^{raw}_t}
$$


# 8. Estoque de produto

O produto gerado pelo reator é armazenado até que seja transportado e vendido.

A dinâmica do estoque pode ser representada por:
$$
q^{conversion}_t = r_{conversion} E^{conersion}_t 
$$


$$
Q_t = \eta^T_t \eta^{Aux}_t q^{conversion}_t
$$

$$
P_{t+1} = P_t + Q_t - q^{transport}_t
$$

com:

$$
C_P \geq P_t \geq 0
$$

O transporte também possui uma capacidade limitada e consome energia.



# 9. Preços

Os preços da matéria-prima e do produto podem variar ao longo do tempo.

Assim:

$$
p^M_t \neq p^M_{t+1}
$$

$$
p^P_t \neq p^P_{t+1}
$$

$$
p^E_t \neq p^E_{t+1}
$$

Essas variações introduzem uma oportunidade de planejamento.

Por exemplo, o agente pode decidir comprar mais matéria-prima quando seu preço estiver baixo e armazená-la para utilização futura.

Da mesma forma, pode ser vantajoso armazenar o produto quando o preço de venda estiver baixo e transportá-lo quando o preço estiver mais alto.

Os preços podem ser:

- determinados por uma série histórica;
- gerados por um modelo estocástico;
- definidos por um ambiente de simulação;
- ou fornecidos externamente ao ambiente.



# 10. Energia

A quantidade de energia disponível em cada instante é limitada:

$$
E_t = E_{available}
$$

Essa energia deve ser alocada entre as diferentes atividades.

O problema apresenta, portanto, uma competição entre:

1. comprar matéria-prima;
2. aumentar a temperatura;
3. aumentar a eficiência através dos sistemas auxiliares;
4. transportar o produto.

Utilizar mais energia em uma atividade significa necessariamente ter menos energia disponível para as demais.


# 11. Recompensa

A recompensa deve representar o objetivo econômico do sistema.

Uma formulação inicial é:

$$
R_t = Revenue_t - Cost^{raw}_t - Cost^{energy}_t
$$

onde:

- $Revenue_t$ representa a receita obtida pela venda do produto;
- $Cost^{raw}_t$ representa o custo da matéria-prima;
- $Cost^{energy}_t$ representa o custo associado à energia;

e:

$$
Revenue_t = p^P_t q^{transport}_t
$$

$$
Cost^{raw}_t = p^M_t q^{raw}_t
$$

$$
Cost^{energy}_t = p^E_t E_t
$$

O objetivo do agente será maximizar a recompensa acumulada:

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$



# 12. Objetivo

O objetivo principal do agente é encontrar uma política $\pi$ que maximize o lucro esperado ao longo do tempo:

$$
\pi^* = \arg\max_{\pi} \mathbb{E}_{\pi} \left[ \sum_{t=0}^{\infty} \gamma^t R_{t+1} \right]
$$

O agente deve aprender a equilibrar **produção, eficiência, estoque, preços e utilização da energia**.

Uma estratégia que maximize a produção instantânea não necessariamente maximizará o lucro.

Por exemplo:

> Aumentar muito a temperatura pode produzir mais rapidamente, mas pode consumir mais energia e reduzir a eficiência.

Da mesma forma:

> Comprar muita matéria-prima quando o preço está alto pode ser pior do que utilizar o estoque existente e esperar uma oportunidade de compra mais favorável.

E:

> Vender muito produto quando seu preço está baixo pode ser menos vantajoso do que armazená-lo e transportá-lo posteriormente.

O agente deverá aprender decisões como:

### Produção

- Quanto produzir em cada instante?
- Qual temperatura utilizar?
- Quanto investir em sistemas auxiliares?

### Estoque

- Quando comprar matéria-prima?
- Quanto comprar?
- Quando utilizar o estoque existente?
- Quanto produto manter armazenado?

### Transporte

- Quando transportar o produto?
- Quanto transportar?
- É melhor vender imediatamente ou esperar uma condição de preço mais favorável?

### Energia

- Quanto da energia disponível deve ser destinada a cada atividade?
- É melhor produzir mais agora ou preservar recursos para uma oportunidade futura?


O problema apresenta diversos trade-offs que tornam a tarefa adequada para Reinforcement Learning.

### Temperatura × Eficiência

Temperaturas maiores podem aumentar a taxa de conversão, mas reduzir a eficiência.

### Produção × Energia

Produzir mais pode exigir maior consumo energético.

### Estoque × Preço

Manter estoque permite aproveitar variações futuras de preço, mas aumenta o custo no curto prazo.

### Sistemas auxiliares × Energia

Aumentar o uso dos sistemas auxiliares pode melhorar a eficiência da conversão, mas consome parte da energia disponível.



# 13. Ambiente

O ambiente de simulação será responsável por:

1. fornecer o estado atual;
2. receber a ação do agente;
3. verificar as restrições;
4. calcular o consumo de energia;
5. atualizar temperatura e sistemas auxiliares;
6. atualizar os estoques;
7. realizar a conversão da matéria-prima;
8. atualizar os preços;
9. calcular a receita e os custos;
10. retornar o novo estado e a recompensa.

Uma interação pode ser representada por:

```text
              ┌──────────────┐
              │    Agente    │
              └──────┬───────┘
                     │
                    A_t
                     │
                     ▼
              ┌──────────────┐
              │   Ambiente   │
              └──────┬───────┘
                     │
            ┌────────┴────────┐
            │                 │
          R_{t+1}           S_{t+1}
            │                 │
            └────────┬────────┘
                     │
                     ▼
                   Agente
```



# 14. Possíveis extensões

A primeira versão do ambiente pode utilizar funções simplificadas e determinísticas.

Posteriormente, podem ser adicionados:

- ruído nos sensores;
- atrasos no aquecimento;
- capacidade máxima do reator;
- custo de armazenamento;
- custo variável de energia;
- limites de transporte;
- demanda variável;
- diferentes fontes de energia.

Essas extensões permitem aumentar progressivamente a complexidade do problema de RL.


# 15. Primeira versão do problema

Para a primeira implementação, o ambiente pode ser simplificado para:

- uma matéria-prima;
- um produto;
- um reator;
- uma quantidade fixa de energia por instante;
- preço variável da matéria-prima;
- preço variável do produto;
- estoque de matéria-prima;
- estoque de produto;
- temperatura controlável;
- um sistema auxiliar;
- limites de variação do sistema auxiliar;

A recompensa será baseada no **lucro obtido em cada instante**.

A partir dessa versão básica, novos elementos podem ser incorporados gradualmente.