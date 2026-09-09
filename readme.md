# Reinforcement Learning: An Introduction — Sutton & Barto

Projeto de estudo baseado no livro **[Reinforcement Learning: An Introduction — 2nd Edition](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)**, de Richard S. Sutton e Andrew G. Barto.

O objetivo deste projeto é estudar os conceitos de **Reinforcement Learning (RL)** apresentados no livro através da implementação, em Python, de alguns dos exemplos e algoritmos discutidos ao longo dos capítulos.


## Conteúdo

As implementações serão organizadas de acordo com os conceitos e exemplos estudados no livro.
Alguns dos temas abordados são:

* Multi-Armed Bandits
* Markov Decision Processes
* Dynamic Programming
* Monte Carlo Methods
* Temporal-Difference Learning
* SARSA
* Q-Learning
* Policy Gradients
* Function Approximation
* Reinforcement Learning com redes neurais

O projeto será desenvolvido gradualmente conforme os capítulos forem estudados.

Cada diretório representa, quando possível, os exemplos e experimentos relacionados a um capítulo do livro.

## Reprodutibilidade

Alguns experimentos utilizam números aleatórios. Para permitir a reprodução dos resultados, os geradores aleatórios podem ser inicializados utilizando uma `seed`.

Exemplo:

```python
import random

rng = random.Random(42)

value = rng.random()
```

Utilizando a mesma `seed` e executando as mesmas operações na mesma ordem, a sequência pseudoaleatória será reproduzida.

Isso permite testar e comparar diferentes implementações sob as mesmas condições.

## Licença

Este projeto é um projeto para fins **educacionais** e tem como objetivo estudar e implementar, de forma independente, conceitos e exemplos apresentados em *Reinforcement Learning: An Introduction*.

O código não pretende reproduzir ou distribuir o conteúdo do livro. Para a explicação completa dos conceitos, algoritmos e exemplos, consulte a obra original.

O livro **Reinforcement Learning: An Introduction** e seu conteúdo permanecem sob os direitos de seus respectivos autores e editores.