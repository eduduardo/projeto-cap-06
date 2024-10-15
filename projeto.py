import oracledb
import json
from datetime import datetime

ORACLE_DSN = "[USUARIO]/[SENHA]@oracle.fiap.com.br:1521/ORCL"


# Função para conectar ao banco de dados Oracle
def conectar_bd():
    try:
        connection = oracledb.connect(ORACLE_DSN)
        return connection
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def solicitar_input(mensagem, tipo):
    tipo_nome = {
        int: "inteiro",
        float: "decimal",
        str: "texto",
        "data": "data no formato YYYY-MM-DD",
        "colheitadeira": "mecânica ou manual",
    }

    while True:
        try:
            valor = input(mensagem)
            if tipo == int:
                valor = int(valor)
            elif tipo == float:
                valor = float(valor)
            elif tipo == str:
                valor = str(valor)
            elif tipo == "data":
                valor = datetime.strptime(valor, "%Y-%m-%d")
            elif tipo == "colheitadeira":
                if valor.lower() not in ["mecanica", "manual"]:
                    raise ValueError("Tipo de colheitadeira inválido")
            elif tipo == "colheitadeira_id":
                if not valor.isdigit():
                    raise ValueError("ID da colheitadeira inválido")
                if not checa_se_colheitadeira_existe(valor):
                    raise Exception("colheitadeira não encontrada")
            return valor
        except ValueError:
            print(
                f"Entrada inválida! Por favor, insira um valor do tipo {tipo_nome[tipo]}."
            )
        except Exception as e:
            print(f"Erro ao inserir valor: {e}")


# Função para inserir um usuário
def inserir_usuario(nome, email, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (:1, :2, :3)",
            (nome, email, senha),
        )
        conn.commit()
        print("Usuário inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir usuário: {e}")
    finally:
        cursor.close()
        conn.close()


# Função para inserir uma colheitadeira
def inserir_colheitadeira(nome, capacidade, tipo, eficiencia):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO colheitadeiras (nome, capacidade, tipo, eficiencia) VALUES (:1, :2, :3, :4)",
            (nome, capacidade, tipo, eficiencia),
        )
        conn.commit()
        print("colheitadeira inserida com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir colheitadeira: {e}")
    finally:
        cursor.close()
        conn.close()
        
def checa_se_colheitadeira_existe(id_colheitadeira):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM colheitadeiras WHERE id_colheitadeira = :1", (id_colheitadeira,))
        colheitadeira = cursor.fetchone()
        if colheitadeira:
            return True
        else:
            return False
    except oracledb.DatabaseError as e:
        print(f"Erro ao buscar colheitadeira: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# Função para inserir uma colheita
def inserir_colheita(
    id_colheitadeira,
    data_colheita,
    area_colhida,
    produtividade,
    umidade_solo,
    temperatura,
    observacoes,
    nome_cultura,
):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO colheitas (id_colheitadeira, data_colheita, area_colhida, produtividade, umidade_solo, temperatura, observacoes, nome_cultura) "
            "VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8)",
            (
                id_colheitadeira,
                data_colheita,
                area_colhida,
                produtividade,
                umidade_solo,
                temperatura,
                observacoes,
                nome_cultura,
            ),
        )
        conn.commit()
        print("Colheita inserida com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir colheita: {e}")
    finally:
        cursor.close()
        conn.close()


# Função para calcular o melhor momento para colheita com dados históricos
def melhor_momento_colheita(umidade_atual, temperatura_atual):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Buscar dados históricos de umidade e temperatura
        cursor.execute("SELECT umidade_solo, temperatura FROM colheitas")
        dados_historicos = cursor.fetchall()

        # Calcular a média histórica de umidade e temperatura
        total_umidade = 0
        total_temperatura = 0
        count = 0

        for umidade, temperatura in dados_historicos:
            total_umidade += umidade
            total_temperatura += temperatura
            count += 1

        media_umidade = total_umidade / count
        media_temperatura = total_temperatura / count

        # Comparar valores atuais com médias históricas
        if umidade_atual < media_umidade and temperatura_atual > media_temperatura:
            return "Agora é o melhor momento para colheita!!"
        else:
            return f"Não é um bom momento para colheita, o melhor momento é com umidade abaixo de {media_umidade} % e temperatura acima de {media_temperatura} °C"
    except oracledb.DatabaseError as e:
        print(f"Erro ao buscar dados históricos: {e}")
        return "Erro ao determinar o momento da colheita"
    finally:
        cursor.close()
        conn.close()


# Função para gerar relatório de colheitas
def gerar_relatorio():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_colheita, data_colheita, produtividade, umidade_solo, temperatura, nome_cultura FROM colheitas"
        )
        relatorio = cursor.fetchall()
        for row in relatorio:
            print(
                f"ID: {row[0]}, Data: {row[1]}, Produtividade: {row[2]}, Umidade: {row[3]}, Temperatura: {row[4]}, Cultura: {row[5]}"
            )
    except oracledb.DatabaseError as e:
        print(f"Erro ao gerar relatório: {e}")
    finally:
        cursor.close()
        conn.close()


def autenticar_usuario():
    print("\n\n\n")
    print("Autenticação de Usuário")
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")

    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = :1 AND senha = :2", (email, senha)
        )
        usuario = cursor.fetchone()
        if usuario:
            return True
        else:
            return False
    except oracledb.DatabaseError as e:
        print(f"Erro ao autenticar usuário: {e}")


# Função para salvar relatório em arquivo de texto
def salvar_relatorio_texto():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_colheita, data_colheita, produtividade, umidade_solo, temperatura, nome_cultura FROM colheitas"
        )
        relatorio = cursor.fetchall()
        with open("relatorio.txt", "w") as file:
            for row in relatorio:
                file.write(
                    f"ID: {row[0]}, Data: {row[1]}, Produtividade: {row[2]}, Umidade: {row[3]}, Temperatura: {row[4]}, Cultura: {row[5]}\n"
                )
        print("Relatório salvo em relatorio.txt")
    except oracledb.DatabaseError as e:
        print(f"Erro ao salvar relatório: {e}")
    finally:
        cursor.close()
        conn.close()

# Função para salvar relatório em arquivo JSON
def salvar_relatorio_json():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_colheita, data_colheita, produtividade, umidade_solo, temperatura, nome_cultura FROM colheitas"
        )
        relatorio = cursor.fetchall()
        relatorio_json = [
            {
                "ID": row[0],
                "Data": row[1].strftime("%Y-%m-%d"),
                "Produtividade": row[2],
                "Umidade": row[3],
                "Temperatura": row[4],
                "Cultura": row[5],
            }
            for row in relatorio
        ]
        with open("relatorio.json", "w") as file:
            json.dump(relatorio_json, file, indent=4)
        print("Relatório salvo em relatorio.json")
    except oracledb.DatabaseError as e:
        print(f"Erro ao salvar relatório: {e}")
    finally:
        cursor.close()
        conn.close()

# Função para listar colheitadeiras
def listar_colheitadeiras():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM colheitadeiras")
        colheitadeiras = cursor.fetchall()
        for colheitadeira in colheitadeiras:
            print(f"ID: {colheitadeira[0]}, Nome: {colheitadeira[1]}, Capacidade: {colheitadeira[2]}, Tipo: {colheitadeira[3]}, Eficiência: {colheitadeira[4]}")
    except oracledb.DatabaseError as e:
        print(f"Erro ao buscar colheitadeiras: {e}")
    finally:
        cursor.close()
        conn.close()


def menu():

    print("\n\n\n")
    print("Menu Principal")
    print("1 - Inserir colheitadeira")
    print("2 - Inserir Colheita")
    print("3 - Gerar Relatório de colheitas")
    print("4 - Melhor Momento para Colheita")
    print("5 - Salvar Relatório em Texto")
    print("6 - Salvar Relatório em JSON")
    print("7 - Listar colheitadeiras")
    print("8 - Sair")

    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        nome = solicitar_input("Digite o nome da colheitadeira: ", str)
        capacidade = solicitar_input("Digite a capacidade da colheitadeira: ", int)
        tipo = solicitar_input(
            "Digite o tipo da colheitadeira (mecanica/manual)", "colheitadeira"
        )
        eficiencia_porcentagem = solicitar_input("Digite a eficiência da colheitadeira (0-100): ", int)
        eficiencia = eficiencia_porcentagem / 100
        inserir_colheitadeira(nome, capacidade, tipo, eficiencia)
    elif opcao == "2":
        id_colheitadeira = solicitar_input("Digite o ID da colheitadeira: ", "colheitadeira_id")
        data_colheita = solicitar_input(
            "Digite a data da colheita (YYYY-MM-DD): ", "data"
        )
        area_colhida = solicitar_input("Digite a área colhida (em m²): ", float)
        produtividade = solicitar_input("Digite a produtividade (em toneladas): ", float)
        umidade_solo = solicitar_input("Digite a umidade do solo (em %): ", float)
        temperatura = solicitar_input("Digite a temperatura (em °C): ", float)
        observacoes = solicitar_input("Digite as observações: ", str)
        nome_cultura = solicitar_input("Digite o nome da cultura (feijao, soja, ...): ", str)
        inserir_colheita(
            id_colheitadeira,
            data_colheita,
            area_colhida,
            produtividade,
            umidade_solo,
            temperatura,
            observacoes,
            nome_cultura,
        )
    elif opcao == "3":
        gerar_relatorio()
    elif opcao == "4":
        umidade = solicitar_input("Digite a umidade do solo atual em %: ", float)
        temperatura = solicitar_input("Digite a temperatura atual em °C: ", float)
        print(melhor_momento_colheita(umidade, temperatura))
    elif opcao == "5":
        salvar_relatorio_texto()
    elif opcao == "6":
        salvar_relatorio_json()
    elif opcao == "7":
        listar_colheitadeiras()
    elif opcao == "8":
        exit()
    else:
        print("Opção inválida")


if __name__ == "__main__":
    if not autenticar_usuario():
        print("Usuário não existe ou senha inválida, tente novamente")
        exit()

    while True:
        menu()
