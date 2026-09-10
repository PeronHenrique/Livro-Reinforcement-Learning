# Reinforcement Learning

Projeto de estudo dedicado ao aprendizado de Reinforcement Learning (RL) por meio da implementação prática de conceitos, algoritmos e exemplos encontrados em diferentes livros e materiais de referência sobre o tema.

O objetivo principal é aprender e aprofundar os conceitos de Reinforcement Learning através da prática, recriando e experimentando diferentes abordagens apresentadas nas referências utilizadas durante o estudo.

As implementações são desenvolvidas de forma independente e podem incluir adaptações, experimentos e variações dos exemplos originais.

Ao final esperasse aplicar as tecnicas e conhecimentos obtidos a alguns projetos pessoais.

# Conteúdo

O projeto será desenvolvido gradualmente conforme os diferentes conceitos de Reinforcement Learning forem estudados.

Entre os temas explorados (e as suas principais referências) estão:

* Multi-Armed Bandits (Suton & Barto)

A organização do projeto busca manter os exemplos e experimentos relacionados aos conceitos estudados, independentemente da fonte utilizada.

Projetos pessoais:

* Jogo 1010 (Criar agente capaz de jogar o jogo)
* Problema do Reator (Adaptado do exemplo 3.1 de Suton & Barto) 

# Referências

Durante o desenvolvimento do projeto serão utilizados diferentes livros e materiais de referência.

* Livro **[Reinforcement Learning: An Introduction — 2nd Edition](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)**, de Richard S. Sutton e Andrew G. Barto.


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

Este projeto é um projeto para fins **educacionais**.

O código não pretende reproduzir ou distribuir o conteúdo do livro. Para a explicação completa dos conceitos, algoritmos e exemplos, consulte a obra original.

Os livros,textos e materiais utilizados e seus conteúdos permanecem sob os direitos de seus respectivos autores e editores.