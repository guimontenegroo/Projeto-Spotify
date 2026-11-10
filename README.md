# Spotify POO — Simulador em Python

## Sobre o projeto

Este projeto foi desenvolvido como atividade acadêmica da disciplina de **Programação Orientada a Objetos (POO)**.

O objetivo é simular algumas funcionalidades do Spotify utilizando Python, aplicando conceitos de orientação a objetos, como herança, encapsulamento, métodos, classes e organização de código.

O sistema começou com uma interface pelo terminal e posteriormente recebeu uma interface gráfica desenvolvida com Tkinter.

Na quinta etapa do desenvolvimento, o foco foi a refatoração do código, separando as classes de negócio, os serviços e os componentes da interface para facilitar a manutenção e o entendimento do projeto.

## Funcionalidades

- Criação e gerenciamento de perfis de usuários.
- Catálogo de músicas com informações de título, artista, gênero e duração.
- Simulação da reprodução de músicas.
- Criação e exclusão de playlists.
- Adição e remoção de músicas nas playlists.
- Avaliação de músicas com notas de 1 a 5.
- Comentários nas avaliações.
- Cálculo da média das avaliações.
- Simulação de propagandas durante a reprodução de playlists.
- Armazenamento de informações em arquivos JSON.
- Interface gráfica com tema escuro.

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Tkinter:** desenvolvimento da interface gráfica.
- **JSON:** armazenamento e recuperação dos dados.
- **Programação Orientada a Objetos:** organização das classes e funcionalidades.

## Estrutura do projeto

```text
Spotify/
│
├── main.py
├── interface.py
├── interface_perfis.py
├── interface_catalogo.py
├── interface_playlists.py
│
├── usuario.py
├── musica.py
├── avaliacao.py
├── playlist.py
├── propaganda.py
├── faixa_audio.py
│
├── servicos.py
├── catalogo.py
├── projeto.py
└── dados.json
```

## Organização das classes

### Classes de negócio

Representam os principais elementos do sistema.

- `Usuario`: gerencia informações dos perfis e suas playlists.
- `Musica`: armazena informações das músicas e suas avaliações.
- `Playlist`: organiza as músicas e simula sua reprodução.
- `Avaliacao`: valida notas e armazena comentários.
- `Propaganda`: representa anúncios reproduzidos pelo sistema.
- `FaixaAudio`: classe-base utilizada por músicas e propagandas.

### Serviços

O arquivo `servicos.py` concentra as operações relacionadas ao armazenamento e à recuperação dos dados do sistema.

O arquivo `catalogo.py` reúne as definições do catálogo inicial de músicas e das propagandas padrão.

Essa organização permite separar os dados e comportamentos dos objetos das operações de gerenciamento da aplicação.

### Interface gráfica

A interface foi organizada em módulos com responsabilidades específicas:

- `interface.py`: estrutura principal da aplicação.
- `interface_perfis.py`: telas e operações de perfis.
- `interface_catalogo.py`: catálogo, reprodução e avaliações.
- `interface_playlists.py`: gerenciamento das playlists.

## Como executar

1. Instale o Python no computador.
2. Baixe ou clone este repositório.
3. Abra a pasta do projeto no VS Code ou em outro editor.
4. Execute o arquivo `interface.py` para abrir a interface gráfica.

```bash
python interface.py
```

Para utilizar a versão pelo terminal:

```bash
python main.py
```

O projeto utiliza bibliotecas da própria instalação padrão do Python, incluindo Tkinter e JSON.

## Persistência dos dados

O sistema utiliza o arquivo `dados.json` para armazenar informações dos usuários, playlists, músicas e avaliações.

Os métodos `to_dict()` e `from_dict()` permitem converter os objetos em dicionários e reconstruí-los a partir das informações salvas.

## Refatoração — Quinta semana

Nesta etapa, o projeto passou por uma reorganização estrutural, seguindo as orientações apresentadas em aula.

As principais mudanças foram:

- Separação das classes de negócio em arquivos individuais.
- Organização das operações de serviço.
- Divisão da interface gráfica em módulos.
- Atualização das importações entre arquivos.
- Redução da concentração de código em arquivos extensos.
- Preservação das funcionalidades desenvolvidas nas etapas anteriores.

O objetivo foi melhorar a legibilidade, a organização e a manutenção do código, além de facilitar o entendimento de seu funcionamento.

## Objetivo acadêmico

O projeto tem finalidade educacional e busca demonstrar a aplicação prática dos conceitos estudados na disciplina de Programação Orientada a Objetos.

A reprodução de músicas é simulada, não sendo realizado streaming de áudio real.

## Status do projeto

**Em desenvolvimento acadêmico.**

A etapa atual está concentrada na organização do código e na consolidação dos conceitos de programação orientada a objetos.
