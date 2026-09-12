# Operação de um Reator - Formulação como Problema de RL

Considere um sistema de produção química baseado em um reator no qual uma matéria-prima é convertida em um produto de interesse.

Dada a necessidade de gestão de estoques e a disponibilidade de uma quantidade fixa de energia,
a cada instante de tempo o operador deve decidir:

- Quantidade de matéria prima a ser comprada;
- Quantidade de matéria prima a ser colocada no reator;
- Quantidade de produto a ser vendido;
- Energia a ser aplicada no aquecimento do reator;
- Energia destinada para a ativação de sistemas auxiliares.

O problema é inspirado no exemplo 3.1 de bioreator apresentado em *Reinforcement Learning: An Introduction*, de Richard S. Sutton e Andrew G. Barto, mas constitui uma formulação própria para estudo.

O objetivo principal do agente é encontrar uma política $\pi$ que maximize o lucro esperado ao longo do tempo:

$$
\pi^* = \arg\max_{\pi} \mathbb{E}_{\pi} \left[ \sum_{t=0}^{\infty} \gamma^t R_{t+1} \right]
$$

O agente deve aprender a equilibrar produção, eficiência, estoque, preços e utilização da energia.
Uma estratégia que maximize a produção instantânea não necessariamente maximizará o lucro.

Por exemplo:

> Aumentar muito a temperatura pode produzir mais rapidamente, mas pode consumir mais energia e reduzir a eficiência.

> Comprar muita matéria-prima quando o preço está alto pode ser pior do que utilizar o estoque existente e esperar uma oportunidade de compra mais favorável.

> Vender muito produto quando seu preço está baixo pode ser menos vantajoso do que armazená-lo e transportá-lo posteriormente.

O problema apresenta diversos trade-offs que tornam a tarefa adequada para Reinforcement Learning.

* Estoque × Preço: Manter estoque permite aproveitar variações futuras de preço, mas aumenta o custo no curto prazo.
* Temperatura × Eficiência: Temperaturas maiores podem aumentar a taxa de conversão, mas reduzir a eficiência.
* Sistemas auxiliares × Energia: Aumentar o uso dos sistemas auxiliares pode melhorar a eficiência da conversão, mas consome parte da energia disponível.

## 2. Formulação como problema de Reinforcement Learning

O problema pode ser modelado como um Processo de Decisão de Markov (MDP) contínuo:

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

## 3. Representação do Estado

O estado deve representar as informações necessárias para que o agente consiga tomar uma decisão sobre a operação do processo e a utilização da energia.
O vetor de estado é:

$$
S_t = [E^{disp}_t, M^{raw}_t, M^{react}_t, M^{prod}_t, p^{raw}_t, p^{prod}_t, p^E_t, T^{react}_t, AUX_t]
$$

onde:

| Variável | Descrição |
|---|---|
| $E^{disp}_t$ | Energia disponível no instante $t$ |
| $M^{raw}_t$ | Estoque de matéria-prima |
| $M^{react}_t$ | Matéria-prima no reator |
| $M^{prod}_t$ | Estoque de produto |
| $p^{raw}_t$ | Preço da matéria-prima |
| $p^{prod}_t$ | Preço do produto |
| $p^E_t$ | Preço da energia |
| $T^{react}_t$ | Temperatura atual do reator |
| $AUX_t$ | Nível atual dos sistemas auxiliares |

## 4. Representação da Ação

A ação representa as decisões tomadas pelo agente em cada instante.
O vetor de ação é:

$$
A_t = [q^{raw}_t, q^{react}_t, E^{heat}_t, E^{aux}_t, q^{sell}_t]
$$

onde:

- $q^{raw}_t$ — Quantidade de matéria-prima para comprar;
- $q^{react}_t$ — Quantidade de matéria-prima para ser colocada no reator;
- $E^{heat}_t$ — Energia destinada ao aquecimento do reator;
- $E^{aux}_t$ — Energia destinada aos sistemas auxiliares;
- $q^{sell}_t$ — Quantidade de produto a ser vendido.


## 5. Dinâmica do Sistema

### 5.1. Energia

A energia deve obedecer à restrição:

$$
E_t = E^{heat}_t + E^{aux}_t \leq E^{disp}_t
$$

Caso a energia recebida através da ação seja superior ao total, o total aplicado aos sistemas é proporcional ao solicitado, respeitando a $E^{disp}_t$.
Ainda uma penalidade é aplicada na recompensa, pela contratação de energia em excesso.

### 5.2. Aquecimento

O aquecimento influencia a velocidade da conversão da matéria-prima em produto.

De forma simplificada: 

$$
r_{conv} = f(T^{react}_t)
$$

Onde $r_{conv}$ representa a taxa de conversão da matéria prima no conversor, uma taxa de $1$ significa que toda a matéria prima no reator será convertida.
Aumentar a temperatura aumenta a velocidade de conversão, mas também reduz a eficiência do processo. Onde $f(T_t)$ é tal que temperaturas elevadas apresentam menor eficiência:

$$
\eta^T_t = f(T_t)
$$


A temperatura varia proporcionalmente com a diferença entre a energia aplicada e a energia perdida por radiação. A energia perdida por radiação é proporcional a temperatura:

$$
T_{t+1} = T_t + C_{heating} (E^{heat}_t - C_{rad} T_t)  
$$

O sistema possui limite da energia que pode ser usada para o aquecimento:

$$
0 \leq E^{heat}_t \leq E^{heat}_{max} 
$$


### 5.3. Sistemas Auxiliares

Os sistemas auxiliares têm como função aumentar a eficiência da geração do produto desejado. Onde $f(AUX_t)$ é maior que $1$ a partir de um determinado nível de utilização:

$$
\eta^{aux}_t = f(AUX_t)
$$

A produção efetiva depende tanto da temperatura quanto dos sistemas auxiliares: $\eta_t = \eta^{aux}_t \times \eta^T_t$

Os sistemas auxiliares possuem restrições físicas sobre a velocidade com que determinados parâmetros podem ser alterados e os valores máximos.

Para os sistemas auxiliares:

$$
\Delta E^{aux}_t = E^{aux}_t - E^{aux}_{t-1}
$$

$$
AUX_{t} = 
  \begin{cases}
    E^{aux}_t & |Delta E^{aux}_t| \leq Delta E^{aux}_{max}\\
    AUX_{t-1} +- Delta E^{aux}_{max} & |Delta E^{aux}_t| \geq Delta E^{aux}_{max}
  \end{cases}
$$


### 4.. Estoque de matéria-prima

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


### 4.. Estoque de produto

O produto gerado pelo reator é armazenado até que seja transportado e vendido.

A dinâmica do estoque pode ser representada por:

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



### 5.. Preços

Os preços da matéria-prima do produto e da energia podem variar ao longo do tempo.

Os preços são determinados através de uma fórmula onde alguns componentes da forma $A sin(\alpha \* step + \theta)$. 
Usando diferentes parâmetros para cada conjunto de preços. 
Dessa forma os preços são continuos mas apresentam variações aparentemente aleatórias, sem dependência entre si. 

## 6. Recompensa

A recompensa deve representar o objetivo econômico do sistema.

Uma formulação inicial é:

$$
R_t = p^{prod}_t q^{prod}_t - p^{raw}_t q^{raw}_t - Cost^{energy}_t
$$

onde o custo da energia sofre penalização no caso da ação solicitar mais que a quantidade disponivel:

$$
Cost^{energy}_t = p^E_t min(E_t, E^{disp}_t) + 2p^E_t max(0, E_t - E^{disp}_t)
$$






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
