# Operação de um Reator - Formulação como Problema de RL

Considere um sistema de produção química baseado em um reator no qual uma matéria prima é convertida em um produto de interesse.

Dada a necessidade de gestão de estoques e uma contratação de energia,
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

> Comprar muita matéria prima quando o preço está alto pode ser pior do que utilizar o estoque existente e esperar uma oportunidade de compra mais favorável.

> Vender muito produto quando seu preço está baixo pode ser menos vantajoso do que armazená-lo e transportá-lo posteriormente.

O problema apresenta diversos trade-offs que tornam a tarefa adequada para Reinforcement Learning.

- Estoque × Preço: Manter estoque permite aproveitar variações futuras de preço, mas aumenta o custo no curto prazo.
- Temperatura × Eficiência: Temperaturas maiores podem aumentar a taxa de conversão, mas reduzir a eficiência.
- Sistemas auxiliares × Energia: Aumentar o uso dos sistemas auxiliares pode melhorar a eficiência da conversão, mas consome parte da energia disponível.

## 1. Formulação como problema de Reinforcement Learning

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

## 2. Representação do Estado

O estado deve representar as informações necessárias para que o agente consiga tomar uma decisão sobre a operação do processo e a utilização da energia.
O vetor de estado é:

$$
S_t = [E^{contr}_t, M^{raw}_t, M^{react}_t, M^{prod}_t, p^{raw}_t, p^{prod}_t, p^E_t, T^{react}_t, AUX_t]
$$

onde:

- $E^{contr}_t$  — Energia disponível no instante $t$
- $M^{raw}_t$  — Estoque de matéria prima
- $M^{react}_t$  — matéria prima no reator
- $M^{prod}_t$  — Estoque de produto
- $p^{raw}_t$  — Preço da matéria prima
- $p^{prod}_t$  — Preço do produto
- $p^E_t$  — Preço da energia
- $T^{react}_t$  — Temperatura atual do reator
- $AUX_t$  — Nível atual dos sistemas auxiliares

## 3. Representação da Ação

A ação representa as decisões tomadas pelo agente em cada instante.
O vetor de ação é:

$$
A_t = [q^{raw}_t, q^{react}_t, E^{heat}_t, E^{aux}_t, q^{sell}_t]
$$

onde:

- $q^{raw}_t$ — Quantidade de matéria prima para comprar;
- $q^{react}_t$ — Quantidade de matéria prima para ser colocada no reator;
- $E^{heat}_t$ — Energia destinada ao aquecimento do reator;
- $E^{aux}_t$ — Energia destinada aos sistemas auxiliares;
- $q^{sell}_t$ — Quantidade de produto a ser vendido.


## 4. Dinâmica do Sistema

### 4.1. Energia

A energia usada no instante t é calculada como:

$$
E_t = E^{heat}_t + E^{aux}_t 
$$

E deve seguir as restrições:

$$
E^{heat}_t \leq E^{heat}_{max}
$$

$$
E^{aux}_t \leq E^{aux}_{max}
$$


Caso a energia alocada através da ação seja superior ao maximo permitido, o total aplicado aos sistemas é o valor máximo.

Ainda uma penalidade é aplicada na recompensa, pela uso de energia acima da energia $E^{contr}_t$.

### 4.2. Aquecimento

O aquecimento influencia a velocidade da conversão da matéria prima em produto.

De forma simplificada: 

$$
r_{prod} = f(T^{react}_t)
$$

Onde $r_{prod}$ representa a taxa de conversão da matéria prima no conversor, uma taxa de $1$ significa que toda a matéria prima no reator será convertida.

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


### 4.3. Sistemas Auxiliares

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
    E^{aux}_t & |\Delta E^{aux}_t| \leq \Delta E^{aux}_{max}\\
    AUX_{t-1} \pm \Delta E^{aux}_{max} & |\Delta E^{aux}_t| > \Delta E^{aux}_{max}
  \end{cases}
$$

O sistema possui limite da energia que pode ser usada:

$$
0 \leq E^{aux}_t \leq E^{aux}_{max} 
$$

### 4.4. Estoque de matéria prima

A matéria prima pode ser comprada e armazenada para uso futuro ou usada completamamente.

Se $q^{raw}_t$ representa a quantidade adquirida:

$$
M^{raw}_{t+1} = M^{raw}_t + q^{raw}_t - q^{react}_t
$$

O estoque não pode ser negativo e possui uma capacidade máxima:

$$
0 \leq M^{raw}_t \leq C^{raw}
$$


### 4.5. Reator e Produção

O reator é onde a matéria prima é convertida em produto.
O reator possui capacidade máxima e assim como o estoque:

$$
0 \leq M^{react}_t \leq C^{react}
$$

A produção depende da temperatura do reator, que define $r^{prod}_t$, assim:

$$
q^{prod}_t = max(1, r^{prod}_t)
$$

Se $r^{prod}_t \geq 1$, então toda matéria  prima será convertida, a taxa de conversão depende da eficiência do reator.

Se a matéria  prima permanece no reator por mais de 3 etapas da simulação, então ela é "descartada", simulando uma matéria prima ruim. 

Na simulação sempre é utilizada a matéria prima mais antiga primeiro, seja f(x) uma função que retorna a quantidade de matéria  prima que deve ser descartada, então:

$$
q^{waist}_t = f(M^{react}_t) 
$$


A eficiência é influenciada pelos serviços auxiliares e pela temperatura do reator, que definen $\eta_t$, assim a quantidade de matéria  prima usada é dada por:

$$
q^{used}_t = \frac {q^{prod}_t} {\eta_t} 
$$

Se $\eta_t$ for menor que 1 então a quantidade de produto produzido é menor que a de matéria  prima usada, e vice-versa.

Portanto a quantidade de matéria  prima restante no reator após o instante $t$ é:

$$
M^{react}_{t+1} = M^{react}_t + q^{react}_t - q^{waist}_t - q^{used}_t 
$$ 

### 4.6. Estoque de produto

O produto gerado pelo reator é armazenado até que seja transportado e vendido.
A dinâmica do estoque pode ser representada por:

$$
M^{prod}_{t+1} = M^{prod}_t + q^{prod}_t - q^{sell}_t
$$

O estoque não pode ser negativo e possui uma capacidade máxima:

$$
0 \leq M^{prod}_t \leq C^{prod}
$$

### 4.7. Preços

Os preços da matéria prima do produto e da energia podem variar ao longo do tempo.

Os preços são determinados através de uma fórmula onde alguns componentes da forma $A sin(\alpha * step + \theta)$.
Usando diferentes parâmetros para cada conjunto de preços. 

Dessa forma os preços são continuos mas apresentam variações aparentemente aleatórias, sem dependência entre si. 

### 4.8. Execução de um Passo da Simulação 


A cada instante $t$, o agente recebe o estado atual do sistema e seleciona uma ação $A_t$, que determina os níveis de energia a serem aplicados ao aquecimento e aos sistemas auxiliares.

A execução de um passo da simulação segue a seguinte sequência:

- Recebimento da ação $A_t$.
- Atualização dos preços.
- Aplicação das restrições de energia dos sistemas auxiliares e de aquecimento.
- A energia efetivamente destinada ao aquecimento é utilizada para atualizar a temperatura do reator.
- O nível dos sistemas auxiliares é atualizado respeitando o limite máximo de variação entre dois instantes.
- Determinação da eficiência total do processo $\eta_t$ e da taxa de conversão $r^{react}_t$ 
- Compra da matéria prima.
- Transferência da matéria  prima ao reator. 
- Atualização do estoque de matéria prima.
- Conversão da matéria prima no reator considerando a taxa de produção e eficiência.
- Descarte de matéria prima.
- Atualização do estoque do reator.
- Atualização do estoque de produto.
- Atualização do estoque de produto
- Cálculo da recompensa.

Após todas as atualizações, o ambiente retorna:

$$
(S_{t+1}, R_{t+1})
$$

onde:

- $S_{t+1}$ - novo estado do sistema;
- $R_{t+1}$ - recompensa obtida no instante;

O processo é então repetido no instante $t+1$.

## 5. Recompensa

A recompensa deve representar o objetivo econômico do sistema.
A formulação usada é:

$$
R_t = p^{prod}_t q^{prod}_t - p^{raw}_t q^{raw}_t - Cost^{energy}_t
$$

A recompensa reflete a receita recebida da venda, o custo da matéria  prima e da energia usada para operação. 

O custo da energia sofre penalização no caso do agente solicitar mais que a quantidade contratada:

$$
Cost^{energy}_t = p^E_t min(E_t, E^{contr}_t) + 2p^E_t max(0, E_t - E^{disp}_t)
$$