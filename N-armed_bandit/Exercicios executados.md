### N-armed bandit

Você tem a opção de realizar N ações. Cada ação possui uma recompensa pré-determinada, com algum nível de ruído. Você não sabe qual a recompensa de nenhuma das ações.

O objetivo é obter a maior recompensa total ao longo de várias ações. A cada ação a recompensa não é alterada.


>Exemplo:  
>Caso a recompensa da ação *k* seja 1, ao escolher a ação *k* você poderá receber as seguintes recompensas: <code>{1.1, 1.2, 0.5, 0.8, 1.5, 0.9}</code>
>
>A partir destes resultados é possivel inferir que a recompensa média dessa ação é 1, quanto maior o número da amostra maior será a certeza a respeito da recompensa esperada. 

Assim o algoritmo implementado deve determinar a recompensa esperada para cada ação e escolher a ação que maximiza o valor ao longo prazo.  

É necessário balancear a exploração das opções com a maximação da melhor ação. A fim de explorar as opções de forma adequada, sem deixar de escolher a melhor opção.

Para esse exercicio será implementado uma versão do problema N-armed bandit, onde <code>N = 10</code> e explorado a diferença entre os algoritmos ε-greedy com diferentes ε, tomando como base a solução descrita na seção 2.2 a 2.7 do livro.

Foram implementados:
* Epsilon-Greed Action Selection
* Upper-Confidence-Bound Action Selection
* Gradient Bandits
* Average Value Estimation
* Weighted Average Value Estimation
* Initial Value Estimation 