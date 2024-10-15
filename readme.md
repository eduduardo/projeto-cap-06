# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://github.com/lfusca/templateFiap/raw/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Cap 6 - Python e além

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/edu-ramos/">Eduardo Ramos</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- Lucas
### Coordenador(a)
- André

## 📜 Descrição

Este projeto tem como objetivo gerenciar dados de colheitas no setor de agronegócio. Ele permite a inserção de dados de colhedoras e colheitas, além de gerar relatórios e determinar o melhor momento para colheita com base em dados históricos.



## Funcionalidades
- Inserção de usuários
- Inserção de colhedoras
- Inserção de colheitas
- Geração de relatórios de colheitas
- Determinação do melhor momento para colheita
- Salvamento de relatórios em formato texto e JSON

## Inovação
O projeto utiliza dados históricos para calcular o melhor momento para colheita, otimizando a produtividade e eficiência no campo.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- `projeto.py`: Script principal com as funcionalidades do projeto.
- `README.md`: Este arquivo de documentação.
- `banco-de-dados.sql`: Este arquivo tem toda a estrutura e alguns dados de teste para o projeto.

## 🔧 Como executar o código

### Passo a Passo

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Configure a conexão com o banco de dados Oracle no arquivo `projeto.py`.
```python
ORACLE_DSN = "[USUARIO]/[SENHA]@oracle.fiap.com.br:1521/ORCL"
```


3. Execute o script SQL para criar a base de dados:
    ```sh
    sqlplus usuario/senha@oracle.fiap.com.br:1521/ORCL @banco-de-dados.sql
    ```

4. Instale as dependências do Python:
    ```sh
    pip install oracledb
    ```

5. Execute o script `projeto.py`:
    ```sh
    python src/projeto.py
    ```


## 🗃 Histórico de lançamentos

* 0.1.0 * - 14/10/2024

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

