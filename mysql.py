import pymysql
from datetime import datetime, timedelta

def letras_para_numero(letra):
    letra = letra.upper()
    if letra == 'Z':
        return 0
    return ord(letra) - ord('A') + 1

def numero_para_letras(numero):
    resto = numero % 26
    if resto == 0:
        return 'Z'    
    return chr(ord('A') + resto - 1)

def criptografar(par, matriz):
    x = par[0] * matriz[0][0] + par[1] * matriz [0][1]
    y = par[0] * matriz[1][0] + par[1] * matriz [1][1]
    return[x, y]

def inverter_chave(matriz):
    a, b = matriz[0]
    c, d = matriz[1]

    det = a * d - b * c
    if det == 0:
        raise ValueError("Matriz singular, não tem inversa.")
    
    inversa_det = None
    det_mod = det % 26
    for x in range (1, 26):
        if (det_mod * x) % 26 == 1:
            inversa_det = x
            break

    if not inversa_det:
        print("A chave inserida não funciona em módulo 26.")
    
    inversa = [[d, -b],
              [-c, a]]
    
    return [[x * inversa_det for x in linha] for linha in inversa]

def criptografia(palavra):
    
    global chave

    letras_impar = False
    if len(palavra) % 2 != 0:
        palavra = palavra + 'z'
        letras_impar = True

    palavra = palavra.replace(" ", "")

    valores_numericos = [letras_para_numero(i) for i in palavra]

    pares = []
    for i in range(0, len(valores_numericos), 2):
        pares.append([valores_numericos[i], valores_numericos[i + 1]])

    chave = [[4, 3],
             [1, 2]]

    criptografado = []
    for par in pares:
        criptografado.append(criptografar(par, chave))

    palavra_criptografada = [numero_para_letras(x) for par in criptografado for x in par]

    palavra_criptografada = ''.join(palavra_criptografada)
    
    return palavra_criptografada

def descriptografia(palavra_criptografada):

    chave = [[4, 3],
             [1, 2]]
    
    chave_inversa = inverter_chave(chave)

    valores_numericos_criptografados = [letras_para_numero(i) for i in palavra_criptografada]

    pares_criptografados = []
    for i in range(0, len(valores_numericos_criptografados), 2):
        pares_criptografados.append([valores_numericos_criptografados[i], valores_numericos_criptografados[i + 1]])

    descriptografado = []
    for par in pares_criptografados:
        descriptografado.append(criptografar(par, chave_inversa))

    palavra_descriptografada = [numero_para_letras(x) for par in descriptografado for x in par]
    palavra_descriptografada = ''.join(palavra_descriptografada)
    
    letra_extra = False
    if len(palavra_descriptografada) % 2 == 0:
        if palavra_descriptografada[-1] == 'Z':
            letra_extra = True
    if letra_extra:
        palavra_descriptografada = palavra_descriptografada[:-1]

    return palavra_descriptografada

def conectar_banco():
    """Conecta ao banco de dados MySQL."""
    return pymysql.connect(
        host='BD-ACD',
        user='BD170225437',
        password='Rzvvt3',
        database='BD170225437',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

def criar_tabelas(cursor):
    """Cria as tabelas Sustentabilidade e MediasSustentabilidade se não existirem."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sustentabilidade (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        data DATE,
        litros_agua INT,
        agua_classificacao VARCHAR(30),
        eletricidade_Kw INT,
        energia_classificacao VARCHAR(30),
        nao_reciclaveis FLOAT,
        nao_reciclavel_classificacao VARCHAR(30),
        reciclaveis INT,
        reciclavel_classificacao VARCHAR(30),
        publico VARCHAR(5),
        bicicleta VARCHAR(5),
        pe VARCHAR(5),
        Fossilp VARCHAR(5),
        Eletrico VARCHAR(5),
        Fossilc VARCHAR(5),
        transporte_classificacao VARCHAR(30),
        classificacao_geral VARCHAR(30)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS MediasSustentabilidade (
        id_media INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        data_inicial DATE NOT NULL,
        data_final DATE NOT NULL,
        valores_agua TEXT,
        media_agua DECIMAL(10,2),
        valores_energia TEXT,
        media_energia DECIMAL(10,2),
        valores_nao_reciclaveis TEXT,
        media_nao_reciclaveis DECIMAL(10,2),
        valores_reciclaveis TEXT,
        media_reciclaveis DECIMAL(10,2)
    )''')

def coletar_data(prompt_message="Data (DD/MM/AAAA): "):
    """Coleta e valida a data no formato DD/MM/AAAA."""
    data_valida = False
    while not data_valida:
        try:
            data_input = input(prompt_message) 
            dia, mes, ano = map(int, data_input.split('/'))
            data_obj = datetime(ano, mes, dia)
            data_para_armazenar = data_obj.strftime('%Y-%m-%d')
            data_valida = True
            return data_para_armazenar
        except ValueError:
            print("Formato inválido ou data inexistente. Use DD/MM/AAAA.")

def coletar_numero(mensagem, tipo='int'):
    """Coleta e valida a entrada numérica do usuário."""
    valido = False
    while not valido:
        try:
            valor = input(mensagem)
            if tipo == 'float':
                return float(valor)
            return int(valor)
        except ValueError:
            print("Valor inválido. Digite um número.")

def coletar_um_registro_diario():
    """Coleta todos os dados para um único registro diário de sustentabilidade."""
    print('\n--- NOVO REGISTRO DIÁRIO DE SUSTENTABILIDADE ---')
    registro_diario = {}

    registro_diario['nome'] = input('\nDigite seu nome: ')
    registro_diario['data'] = coletar_data("Data do registro (DD/MM/AAAA): ")
    
    print("\n--- Consumo Diário ---")
    registro_diario['litros_agua'] = coletar_numero('Litros de água consumidos: ')
    registro_diario['kwh_de_energia'] = coletar_numero('kWh de energia consumidos: ')
    registro_diario['nao_reciclaveis'] = coletar_numero('Resíduo não reciclável (kg): ', tipo='float')
    registro_diario['reciclaveis'] = coletar_numero('Resíduo reciclável (%): ')
    
    print('\n--- Transportes utilizados no dia (S/N): ---')
    registro_diario['Publico'] = input('Transporte público: ').lower()
    registro_diario['Bicicleta'] = input('Bicicleta: ').lower()
    registro_diario['Pe'] = input('Caminhada: ').lower()
    registro_diario['Fossilp'] = input('Carro à gasolina: ').lower()
    registro_diario['Eletrico'] = input('Carro elétrico: ').lower()
    registro_diario['Fossilc'] = input('Carona: ').lower()
        
    return registro_diario

def calcular_classificacoes(dados):
    """
    Calcula todas as classificações de sustentabilidade (água, energia, resíduos, transporte e geral).
    Pode processar dados diários ou médias de período.
    """
    # Determina se está processando dados diários ou médias de período
    if 'litros_agua' in dados and 'kwh_de_energia' in dados : # Dados diários
        consumo_agua_key = 'litros_agua'
        consumo_energia_key = 'kwh_de_energia'
        consumo_nao_reciclaveis_key = 'nao_reciclaveis'
        consumo_reciclaveis_key = 'reciclaveis'
    elif 'media_litros_agua' in dados and 'media_kwh_de_energia' in dados: # Dados de média de período
        consumo_agua_key = 'media_litros_agua'
        consumo_energia_key = 'media_kwh_de_energia'
        consumo_nao_reciclaveis_key = 'media_nao_reciclaveis'
        consumo_reciclaveis_key = 'media_reciclaveis'
    else:  
        dados['agua_classificacao'] = 'baixa'
        dados['agua_desc'] = 'Não sustentável'
        dados['energia_classificacao'] = 'baixa'
        dados['energia_desc'] = 'Não sustentável'
        dados['nao_reciclavel_classificacao'] = 'baixa'
        dados['nao_reciclavel_desc'] = 'Não sustentável'
        dados['reciclavel_classificacao'] = 'baixa'
        dados['reciclavel_desc'] = 'Não sustentável'
        dados['transporte_classificacao'] = 'baixa' 
        dados['transporte_desc'] = 'Não sustentável'
        dados['classificacao_geral'] = 'Moderado' 
        return dados

    consumo_agua = dados.get(consumo_agua_key, 201) 
    if consumo_agua <= 150:
        agua_classificacao = 'alta'
        dados['agua_classificacao'] = criptografia(agua_classificacao)
        
        agua_desc = 'Altamente'
        dados['agua_desc'] = criptografia(agua_desc)

    elif consumo_agua <= 200:
        agua_classificacao = 'moderada'
        dados['agua_classificacao'] = criptografia(agua_classificacao)

        agua_desc = 'Moderadamente'
        dados['agua_desc'] = criptografia(agua_desc)

    else:
        agua_classificacao = 'baixa'
        dados['agua_classificacao'] = criptografia(agua_classificacao)
        
        agua_desc = 'Baixamente'
        dados['agua_desc'] = criptografia(agua_desc)

    consumo_energia = dados.get(consumo_energia_key, 11) 
    if consumo_energia <= 5:
        energia_classificacao = 'alta'
        dados['energia_classificacao'] = criptografia(energia_classificacao)

        energia_desc = 'Altamente'
        dados['energia_desc'] = criptografia(energia_desc)
        
    elif consumo_energia <= 10:
        energia_classificacao = 'moderada'
        dados['energia_classificacao'] = criptografia(energia_classificacao)

        energia_desc = 'Moderadamente'
        dados['energia_desc'] = criptografia(energia_desc)

    else:
        energia_classificacao = 'baixa'
        dados['energia_classificacao'] = criptografia(energia_classificacao)

        energia_desc = 'Baixamente'
        dados['energia_desc'] = criptografia(energia_desc)

    consumo_nao_reciclaveis = dados.get(consumo_nao_reciclaveis_key, 2.6) 
    if consumo_nao_reciclaveis <= 1.5:
        nao_reciclavel_classificacao = 'alta'
        dados['nao_reciclavel_classificacao'] = criptografia(nao_reciclavel_classificacao)

        nao_reciclavel_desc = 'Altamente'
        dados['nao_reciclavel_desc'] = criptografia(nao_reciclavel_desc)

    elif consumo_nao_reciclaveis <= 2.5:
        nao_reciclavel_classificacao = 'moderada'
        dados['nao_reciclavel_classificacao'] = criptografia(nao_reciclavel_classificacao)

        nao_reciclavel_desc = 'Moderadamente'
        dados['nao_reciclavel_desc'] = criptografia(nao_reciclavel_desc)

    else:
        nao_reciclavel_classificacao = 'baixa'
        dados['nao_reciclavel_classificacao'] = criptografia(nao_reciclavel_classificacao)

        nao_reciclavel_desc = 'Baixamente'
        dados['nao_reciclavel_desc'] = criptografia(nao_reciclavel_desc)

    percentual_reciclaveis = dados.get(consumo_reciclaveis_key, 0) 
    if percentual_reciclaveis >= 50:
        reciclavel_classificacao = 'alta'
        dados['reciclavel_classificacao'] = criptografia(reciclavel_classificacao)

        reciclavel_desc = 'Altamente'
        dados['reciclavel_desc'] = criptografia(reciclavel_desc)

    elif percentual_reciclaveis >= 20:
        reciclavel_classificacao = 'moderada'
        dados['reciclavel_classificacao'] = criptografia(reciclavel_classificacao)

        reciclavel_desc = 'Moderadamente'
        dados['reciclavel_desc'] = criptografia(reciclavel_desc)
    
    else:
        reciclavel_classificacao = 'baixa'
        dados['reciclavel_classificacao'] = criptografia(reciclavel_classificacao)

        reciclavel_desc = 'Baixamente'
        dados['reciclavel_desc'] = criptografia(reciclavel_desc)

    sustentaveis = sum([dados.get('Publico', 'n') == 's', 
                        dados.get('Bicicleta', 'n') == 's', 
                        dados.get('Pe', 'n') == 's', 
                        dados.get('Eletrico', 'n') == 's'])
    nao_sustentaveis = sum([dados.get('Fossilp', 'n') == 's', 
                            dados.get('Fossilc', 'n') == 's'])

    if nao_sustentaveis == 0 and sustentaveis > 0:
        transporte_classificacao = 'alta'
        dados['transporte_classificacao'] = criptografia(transporte_classificacao)

        transporte_desc = 'Altamente'
        dados['transporte_desc'] = criptografia(transporte_desc)

    elif sustentaveis > nao_sustentaveis:
        transporte_classificacao = 'moderada'
        dados['transporte_classificacao'] = criptografia(transporte_classificacao)

        transporte_desc = 'Moderadamente'
        dados['transporte_desc'] = criptografia(transporte_desc)

    else:
        transporte_classificacao = 'baixa'
        dados['transporte_classificacao'] = criptografia(transporte_classificacao)

        transporte_desc = 'Baixamente'
        dados['transporte_desc'] = criptografia(transporte_desc)

    classificacoes = [
        dados['agua_classificacao'],
        dados['energia_classificacao'],
        dados['nao_reciclavel_classificacao'],
        dados['reciclavel_classificacao'],
        dados['transporte_classificacao']
    ]
    altas = classificacoes.count('NYEV')
    baixas = classificacoes.count('KDDEDA')

    if baixas == 5:
        classificacao_geral = 'Baixamente'
        dados['classificacao_geral'] = criptografia(classificacao_geral)

    elif altas == 5 and baixas == 0:
        classificacao_geral = 'Altamente'
        dados['classificacao_geral'] = criptografia(classificacao_geral)

    else:
        classificacao_geral = 'Moderadamente'
        dados['classificacao_geral'] = criptografia(classificacao_geral)
        
    return dados

def inserir_dados(cursor, dados):
    """
    Insere os dados de um único dia (já classificados) na tabela Sustentabilidade.
    """
    sql = '''
        INSERT INTO Sustentabilidade (
            nome, data, 
            litros_agua, agua_classificacao, 
            eletricidade_Kw, energia_classificacao,
            nao_reciclaveis, nao_reciclavel_classificacao, 
            reciclaveis, reciclavel_classificacao,
            publico, bicicleta, pe, Fossilp, Eletrico, Fossilc, 
            transporte_classificacao, classificacao_geral
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    valores_para_inserir = (
        dados.get('nome', 'Desconhecido'), 
        dados.get('data'), 
        dados.get('litros_agua', 0), 
        dados.get('agua_classificacao', 'N/A'),
        dados.get('kwh_de_energia', 0), 
        dados.get('energia_classificacao', 'N/A'),
        dados.get('nao_reciclaveis', 0.0), 
        dados.get('nao_reciclavel_classificacao', 'N/A'),
        dados.get('reciclaveis', 0), 
        dados.get('reciclavel_classificacao', 'N/A'),
        'sim' if dados.get('Publico', 'n') == 's' else 'nao',
        'sim' if dados.get('Bicicleta', 'n') == 's' else 'nao',
        'sim' if dados.get('Pe', 'n') == 's' else 'nao',
        'sim' if dados.get('Fossilp', 'n') == 's' else 'nao',
        'sim' if dados.get('Eletrico', 'n') == 's' else 'nao',
        'sim' if dados.get('Fossilc', 'n') == 's' else 'nao',
        dados.get('transporte_classificacao', 'N/A'),
        dados.get('classificacao_geral', 'N/A')
    )
    
    try:
        cursor.execute(sql, valores_para_inserir)
    except Exception as e:
        print(f"Erro ao inserir dados diários em Sustentabilidade: {e}")

def calcular_e_salvar_media_geral_usuario(cursor):
    """
    Calcula a média geral de consumo de um usuário, exibe e salva/atualiza na tabela MediasSustentabilidade.
    """
    nome_usuario = input("Digite o nome do usuário para calcular a média geral: ")
    if not nome_usuario:
        print("Nome do usuário não pode ser vazio.")
        return

    try:
        sql_select = """
            SELECT data, litros_agua, eletricidade_Kw, nao_reciclaveis, reciclaveis,
                    Publico, Bicicleta, Pe, Fossilp, Eletrico, Fossilc
            FROM Sustentabilidade 
            WHERE nome = %s ORDER BY data ASC
        """
        cursor.execute(sql_select, (nome_usuario,))
        registros = cursor.fetchall()

        if not registros:
            print(f"\nNenhum registro encontrado para o usuário {nome_usuario}. Não é possível calcular a média.")
            return

        num_dias = len(registros)
        datas = [r[0] for r in registros] 
        data_inicial_obj = min(datas)
        data_final_obj = max(datas)
        data_inicial_str = data_inicial_obj.strftime('%Y-%m-%d')
        data_final_str = data_final_obj.strftime('%Y-%m-%d')

        total_litros_agua = sum(r[1] for r in registros)
        total_kwh_de_energia = sum(r[2] for r in registros)
        total_nao_reciclaveis = sum(r[3] for r in registros)
        total_reciclaveis = sum(r[4] for r in registros)

        media_litros_agua = total_litros_agua / num_dias
        media_kwh_de_energia = total_kwh_de_energia / num_dias
        media_nao_reciclaveis = total_nao_reciclaveis / num_dias
        media_reciclaveis = total_reciclaveis / num_dias 

        valores_agua_str = ",".join([str(r[1]) for r in registros])
        valores_energia_str = ",".join([str(r[2]) for r in registros])
        valores_nao_reciclaveis_str = ",".join([str(r[3]) for r in registros])
        valores_reciclaveis_str = ",".join([str(r[4]) for r in registros])

        dados_para_classificacao_periodo = {
            'media_litros_agua': media_litros_agua,
            'media_kwh_de_energia': media_kwh_de_energia,
            'media_nao_reciclaveis': media_nao_reciclaveis,
            'media_reciclaveis': media_reciclaveis,
            'Publico': registros[0][5], 'Bicicleta': registros[0][6], 'Pe': registros[0][7],
            'Fossilp': registros[0][8], 'Eletrico': registros[0][9], 'Fossilc': registros[0][10]
        }
        resumo_classificado = calcular_classificacoes(dados_para_classificacao_periodo)
        
        resumo_periodo_para_mostrar = {
            'nome': nome_usuario,
            'data_inicial': data_inicial_str,
            'data_final': data_final_str,
            'num_dias': num_dias,
            'media_litros_agua': media_litros_agua,
            'agua_desc': resumo_classificado.get('agua_desc'),
            'media_kwh_de_energia': media_kwh_de_energia,
            'energia_desc': resumo_classificado.get('energia_desc'),
            'media_nao_reciclaveis': media_nao_reciclaveis,
            'nao_reciclavel_desc': resumo_classificado.get('nao_reciclavel_desc'),
            'media_reciclaveis': media_reciclaveis,
            'reciclavel_desc': resumo_classificado.get('reciclavel_desc'),
            'transporte_desc': resumo_classificado.get('transporte_desc'),
            'classificacao_geral': resumo_classificado.get('classificacao_geral')
        }
        mostrar_resultados(None, resumo_periodo=resumo_periodo_para_mostrar)

        cursor.execute("SELECT id_media FROM MediasSustentabilidade WHERE nome = %s", (nome_usuario,))
        media_existente = cursor.fetchone()

        db_payload_insert = (
            nome_usuario, data_inicial_str, data_final_str,
            valores_agua_str, round(media_litros_agua, 2),
            valores_energia_str, round(media_kwh_de_energia, 2),
            valores_nao_reciclaveis_str, round(media_nao_reciclaveis, 2),
            valores_reciclaveis_str, round(media_reciclaveis, 2)
        )

        if media_existente:
            sql_update = """
                UPDATE MediasSustentabilidade SET 
                data_inicial = %s, data_final = %s, 
                valores_agua = %s, media_agua = %s, 
                valores_energia = %s, media_energia = %s, 
                valores_nao_reciclaveis = %s, media_nao_reciclaveis = %s, 
                valores_reciclaveis = %s, media_reciclaveis = %s
                WHERE nome = %s
            """
            update_payload = (
                data_inicial_str, data_final_str,
                valores_agua_str, round(media_litros_agua, 2),
                valores_energia_str, round(media_kwh_de_energia, 2),
                valores_nao_reciclaveis_str, round(media_nao_reciclaveis, 2),
                valores_reciclaveis_str, round(media_reciclaveis, 2),
                nome_usuario
            )
            cursor.execute(sql_update, update_payload)
            print(f"\nMédias gerais para {nome_usuario} atualizadas com sucesso na tabela MediasSustentabilidade.")
        else:
            sql_insert = """
                INSERT INTO MediasSustentabilidade (
                    nome, data_inicial, data_final,
                    valores_agua, media_agua,
                    valores_energia, media_energia,
                    valores_nao_reciclaveis, media_nao_reciclaveis,
                    valores_reciclaveis, media_reciclaveis
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, db_payload_insert)
            print(f"\nMédias gerais para {nome_usuario} salvas com sucesso na tabela MediasSustentabilidade.")
        
    except Exception as e:
        print(f"Erro ao calcular e salvar média geral: {e}")

def exibir_registros_usuario(cursor):
    """Exibe todos os registros diários de um usuário específico, ordenados por data."""
    nome_usuario = input("Digite o nome do usuário para exibir os registros: ")
    if not nome_usuario:
        print("Nome do usuário não pode ser vazio.")
        return
    
    try:
        cursor.execute("SELECT * FROM Sustentabilidade WHERE nome = %s ORDER BY data ASC", (nome_usuario,))
        registros = cursor.fetchall()

        if not registros:
            print(f"\nNenhum registro encontrado para o usuário {nome_usuario}.")
            return

        print(f"\n--- Registros Diários para {nome_usuario} ---")
        for record in registros:
            record_id = record[0]
            data_db = record[2]
            data_formatada = data_db.strftime('%d/%m/%Y') if isinstance(data_db, datetime) else str(data_db) 

            consumo_agua = descriptografia(record[4])
            consumo_energia = descriptografia(record[6])
            lixo_nao_reciclavel = descriptografia(record[8])
            lixo_reciclavel = descriptografia (record[10])
            transporte = descriptografia(record[17])
            classificacao_geral_dia = descriptografia(record[18])
            print("---------------------------------")
            print(f"Data: {data_formatada} (ID: {record_id})")
            print(f"Consumo de Água: {record[3]} L ({consumo_agua})")
            print(f"Consumo de Energia: {record[5]} kWh ({consumo_energia})")
            print(f"Lixo Não Reciclável: {record[7]:.2f} kg ({lixo_nao_reciclavel})") 
            print(f"Lixo Reciclável: {record[9]} % ({lixo_reciclavel})")
            print(f"Transporte: {transporte}") 
            print(f"Classificação Geral do Dia: {classificacao_geral_dia}")
            
        print("---------------------------------")
        print(f"\n{len(registros)} registro(s) encontrado(s) para {nome_usuario}.")

    except Exception as e:
        print(f"Erro ao exibir registros: {e}")

def alterar_registro_diario_existente(conexao, cursor):
    """
    Permite ao usuário alterar um registro diário existente no banco de dados.
    """
    print("\n--- ALTERAR REGISTRO DIÁRIO EXISTENTE ---")
    nome_usuario = input("Digite o nome do usuário do registro a ser alterado: ")
    if not nome_usuario:
        print("Nome do usuário não pode ser vazio. Operação cancelada.")
        return

    data_registro_str = coletar_data("Digite a DATA do registro a ser alterado (DD/MM/AAAA): ")

    try:
        # 1. Verificar se o registro existe
        sql_select = "SELECT * FROM Sustentabilidade WHERE nome = %s AND data = %s"
        cursor.execute(sql_select, (nome_usuario, data_registro_str))
        registro_existente = cursor.fetchone()

        if not registro_existente:
            print(f"\nNenhum registro encontrado para '{nome_usuario}' na data '{data_registro_str}'.")
            return

        print(f"\nRegistro atual para {nome_usuario} em {data_registro_str}:")
        print(f"  Água: {registro_existente[3]} L")
        print(f"  Energia: {registro_existente[5]} kWh")
        print(f"  Não Recicláveis: {registro_existente[7]:.2f} kg")
        print(f"  Recicláveis: {registro_existente[9]} %")
        print(f"  Transporte Público: {registro_existente[11]}")
        print(f"  Bicicleta: {registro_existente[12]}")
        print(f"  Caminhada: {registro_existente[13]}")
        print(f"  Carro à Gasolina: {registro_existente[14]}")
        print(f"  Carro Elétrico: {registro_existente[15]}")
        print(f"  Carona: {registro_existente[16]}")
        
        # 2. Coletar as novas informações para o registro
        print("\n--- Digite as NOVAS informações para este registro ---")
        novos_dados = {}
        novos_dados['nome'] = nome_usuario # Mantém o nome
        novos_dados['data'] = data_registro_str # Mantém a data

        novos_dados['litros_agua'] = coletar_numero('Novos litros de água consumidos: ')
        novos_dados['kwh_de_energia'] = coletar_numero('Novos kWh de energia consumidos: ')
        novos_dados['nao_reciclaveis'] = coletar_numero('Novo resíduo não reciclável (kg): ', tipo='float')
        novos_dados['reciclaveis'] = coletar_numero('Novo resíduo reciclável (%): ')
        
        print('\n--- Novos transportes utilizados no dia (S/N): ---')
        aux = 0
        while aux == 0:
            novos_dados['Publico'] = input('Transporte público: ').lower()
            
            if novos_dados['Publico'] == 's' or novos_dados['Publico'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')

        while aux == 0:
            novos_dados['Bicicleta'] = input('Bicicleta: ').lower()

            if novos_dados['Bicicleta'] == 's' or novos_dados['Bicicleta'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')
                
        while aux == 0:
            novos_dados['Pe'] = input('Caminhada: ').lower()

            if novos_dados['Pe'] == 's' or novos_dados['Pe'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')
        
        while aux == 0:
            novos_dados['Fossilp'] = input('Carro à gasolina: ').lower()

            if novos_dados['Fossilp'] == 's' or novos_dados['Fossilp'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')

        while aux == 0:
            novos_dados['Eletrico'] = input('Carro elétrico: ').lower()

            if novos_dados['Eletrico'] == 's' or novos_dados['Eletrico'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')

        while aux == 0:
            novos_dados['Fossilc'] = input('Carona: ').lower()

            if novos_dados['Fossilc'] == 's' or novos_dados['Fossilc'] == 'n':
                break
            
            else:
                print('Resposta inválida! Por favor utilize somente S ou N como resposta.\n')

        # 3. Recalcular classificações com os novos dados
        registro_classificado_atualizado = calcular_classificacoes(novos_dados.copy())

        # 4. Construir e executar o comando UPDATE
        sql_update = """
            UPDATE Sustentabilidade SET
                litros_agua = %s, agua_classificacao = %s,
                eletricidade_Kw = %s, energia_classificacao = %s,
                nao_reciclaveis = %s, nao_reciclavel_classificacao = %s,
                reciclaveis = %s, reciclavel_classificacao = %s,
                publico = %s, bicicleta = %s, pe = %s,
                Fossilp = %s, Eletrico = %s, Fossilc = %s,
                transporte_classificacao = %s, classificacao_geral = %s
            WHERE nome = %s AND data = %s
        """
        valores_para_atualizar = (
            registro_classificado_atualizado.get('litros_agua', 0),
            registro_classificado_atualizado.get('agua_classificacao', 'N/A'),
            registro_classificado_atualizado.get('kwh_de_energia', 0),
            registro_classificado_atualizado.get('energia_classificacao', 'N/A'),
            registro_classificado_atualizado.get('nao_reciclaveis', 0.0),
            registro_classificado_atualizado.get('nao_reciclavel_classificacao', 'N/A'),
            registro_classificado_atualizado.get('reciclaveis', 0),
            registro_classificado_atualizado.get('reciclavel_classificacao', 'N/A'),
            'sim' if registro_classificado_atualizado.get('Publico', 'n') == 's' else 'nao',
            'sim' if registro_classificado_atualizado.get('Bicicleta', 'n') == 's' else 'nao',
            'sim' if registro_classificado_atualizado.get('Pe', 'n') == 's' else 'nao',
            'sim' if registro_classificado_atualizado.get('Fossilp', 'n') == 's' else 'nao',
            'sim' if registro_classificado_atualizado.get('Eletrico', 'n') == 's' else 'nao',
            'sim' if registro_classificado_atualizado.get('Fossilc', 'n') == 's' else 'nao',
            registro_classificado_atualizado.get('transporte_classificacao', 'N/A'),
            registro_classificado_atualizado.get('classificacao_geral', 'N/A'),
            nome_usuario,
            data_registro_str
        )

        cursor.execute(sql_update, valores_para_atualizar)
        conexao.commit()
        print(f"\nRegistro de '{nome_usuario}' na data '{data_registro_str}' alterado com SUCESSO!")
        print("\n--- Novo Resultado do Registro Diário ---")
        mostrar_resultados(registro_classificado_atualizado)

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao alterar o registro: {e}")

def excluir_registros_usuario(conexao, cursor):
    """
    Exclui todos os registros de um usuário nas tabelas 'Sustentabilidade' e 'MediasSustentabilidade'.
    """
    nome_usuario = input("Digite o nome do usuário que deseja EXCLUIR: ")
    if not nome_usuario:
        print("Nome do usuário não pode ser vazio.")
        return

    confirmacao = input(f"Tem certeza que deseja excluir TODOS os registros de '{nome_usuario}'? Esta ação é irreversível! (S/N): ").lower()
    if confirmacao != 's':
        print("Operação de exclusão cancelada.")
        return

    try:
        # Excluir da tabela 'Sustentabilidade'
        cursor.execute("DELETE FROM Sustentabilidade WHERE nome = %s", (nome_usuario,))
        registros_excluidos_sustentabilidade = cursor.rowcount

        # Excluir da tabela 'MediasSustentabilidade'
        cursor.execute("DELETE FROM MediasSustentabilidade WHERE nome = %s", (nome_usuario,))
        registros_excluidos_medias = cursor.rowcount

        conexao.commit()
        print(f"\nOperação concluída com sucesso para o usuário '{nome_usuario}'.")
        print(f"- {registros_excluidos_sustentabilidade} registro(s) excluído(s) da tabela 'Sustentabilidade'.")
        print(f"- {registros_excluidos_medias} registro(s) excluído(s) da tabela 'MediasSustentabilidade'.")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao excluir registros do usuário '{nome_usuario}': {e}")

def mostrar_resultados(registro_classificado=None, resumo_periodo=None):
    """
    Exibe os resultados de um registro diário classificado ou um resumo do período.
    """
    if registro_classificado:
        print("\n--- Resultados do Registro Diário ---")
        data_registro = registro_classificado.get('data')
        if isinstance(data_registro, datetime):
            data_formatada = data_registro.strftime('%d/%m/%Y')
        else:
            try:
                data_formatada = datetime.strptime(str(data_registro), '%Y-%m-%d').strftime('%d/%m/%Y')
            except (ValueError, TypeError):
                data_formatada = str(data_registro) if data_registro else 'N/A'

        agua_classificacao = descriptografia(registro_classificado.get('agua_classificacao', 'N/A'))
        energia_classificacao = descriptografia(registro_classificado.get('energia_classificacao', 'N/A'))
        nao_reciclavel_classificacao = descriptografia(registro_classificado.get('nao_reciclavel_classificacao', 'N/A'))
        reciclavel_classificacao = descriptografia(registro_classificado.get('reciclavel_classificacao', 'N/A'))
        transporte_classificacao = descriptografia(registro_classificado.get('transporte_classificacao', 'N/A'))
        classificacao_geral = descriptografia(registro_classificado.get('classificacao_geral', 'N/A'))

        print(f"Data: {data_formatada}")
        print(f"Consumo de Água: {registro_classificado.get('litros_agua', 'N/A')}L ({agua_classificacao})")
        print(f"Consumo de Energia: {registro_classificado.get('kwh_de_energia', 'N/A')}kWh ({energia_classificacao})")
        print(f"Lixo Não Reciclável: {registro_classificado.get('nao_reciclaveis', 'N/A')}kg ({nao_reciclavel_classificacao})")
        print(f"Lixo Reciclável: {registro_classificado.get('reciclaveis', 'N/A')}% ({reciclavel_classificacao})")
        print(f"Transporte: {transporte_classificacao}")
        print(f"Classificação Geral do Dia: {classificacao_geral}")
        print("---------------------------------")

    if resumo_periodo:
        print("\n--- Resumo do Período ---")
        print(f"Usuário: {resumo_periodo.get('nome', 'N/A')}")

        data_inicial_str = resumo_periodo.get('data_inicial', 'N/A')
        if isinstance(data_inicial_str, str) and data_inicial_str != 'N/A':
            try:
                data_inicial_formatada = datetime.strptime(data_inicial_str, '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                data_inicial_formatada = data_inicial_str 
        elif isinstance(data_inicial_str, datetime):
            data_inicial_formatada = data_inicial_str.strftime('%d/%m/%Y')
        else:
            data_inicial_formatada = 'N/A'

        data_final_str = resumo_periodo.get('data_final', 'N/A')
        if isinstance(data_final_str, str) and data_final_str != 'N/A':
            try:
                data_final_formatada = datetime.strptime(data_final_str, '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                data_final_formatada = data_final_str 
        elif isinstance(data_final_str, datetime):
            data_final_formatada = data_final_str.strftime('%d/%m/%Y')
        else:
            data_final_formatada = 'N/A'
            
        print(f"Período: {data_inicial_formatada} a {data_final_formatada}")
        print(f"Número de dias no período: {resumo_periodo.get('num_dias', 'N/A')}")
        
        agua_desc = resumo_periodo.get('agua_desc', 'N/A')
        agua_desc = descriptografia(agua_desc)

        energia_desc = resumo_periodo.get('energia_desc', 'N/A')
        energia_desc = descriptografia(energia_desc)

        nao_reciclavel_desc = resumo_periodo.get('nao_reciclavel_desc', 'N/A')
        nao_reciclavel_desc = descriptografia(nao_reciclavel_desc)

        reciclavel_desc = resumo_periodo.get('reciclavel_desc', 'N/A')
        reciclavel_desc = descriptografia(reciclavel_desc)

        transporte_desc = resumo_periodo.get('transporte_desc', 'N/A')
        transporte_desc = descriptografia(transporte_desc)

        classificacao_geral_periodo = resumo_periodo.get('classificacao_geral', 'N/A')
        classificacao_geral_periodo = descriptografia(classificacao_geral_periodo)

        media_agua = resumo_periodo.get('media_litros_agua', 0)
        media_energia = resumo_periodo.get('media_kwh_de_energia', 0)
        media_nao_reciclaveis = resumo_periodo.get('media_nao_reciclaveis', 0)
        media_reciclaveis = resumo_periodo.get('media_reciclaveis', 0)

        print(f"Média de Consumo de Água: {media_agua if isinstance(media_agua, (int, float)) else 0:.2f} L ({agua_desc})")
        print(f"Média de Consumo de Energia: {media_energia if isinstance(media_energia, (int, float)) else 0:.2f} kWh ({energia_desc})")
        print(f"Média de Lixo Não Reciclável: {media_nao_reciclaveis if isinstance(media_nao_reciclaveis, (int, float)) else 0:.2f} kg ({nao_reciclavel_desc})")
        print(f"Média de Lixo Reciclável: {media_reciclaveis if isinstance(media_reciclaveis, (int, float)) else 0:.2f} % ({reciclavel_desc})")
        print(f"Classificação de Transporte no Período: {transporte_desc}")
        print(f"Classificação Geral do Período: {classificacao_geral_periodo}")
        print("---------------------------------")

def mostrar_menu():
    """Exibe o menu principal e retorna a escolha válida do usuário."""
    print("\n========= MENU PRINCIPAL =========")
    print("1. Adicionar novo(s) registro(s) diário(s)")
    print("2. Alterar registro diário existente")
    print("3. Excluir registro(s) diário(s) de um usuário")
    print("4. Exibir todos os registros diários de um usuário")
    print("5. Calcular e exibir média geral de um usuário")
    print("6. Sair")
    print("==================================")

    while escolha != 6:
        try:
            escolha = int(input("Digite sua opção: "))
            if 1 <= escolha <= 5:
                return escolha
            elif escolha == 6:
                print("\nSaindo do programa...")
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except ValueError:
            print("Opção inválida. Por favor, tente novamente.")

def main():
    """Função principal do programa que gerencia o fluxo de execução."""
    conexao = None
    cursor = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        criar_tabelas(cursor)

        menu_principal_ativo = True
        while menu_principal_ativo:
            escolha = mostrar_menu()

            if escolha == 1:
                print("\n--- Adicionar Novo(s) Registro(s) ---")
                adicionando_registros = True
                while adicionando_registros:
                    registro_diario = coletar_um_registro_diario()
                    if registro_diario: 
                        registro_classificado = calcular_classificacoes(registro_diario.copy()) 
                        inserir_dados(cursor, registro_classificado)
                        conexao.commit() 
                        print("\n1 registro diário adicionado com sucesso!") 
                        mostrar_resultados(registro_classificado) 
                    
                    continuar_adicao = ''
                    while continuar_adicao not in ['s', 'n']:
                        continuar_adicao = input("\nDeseja adicionar outro registro nesta sessão? (S/N): ").lower()
                        if continuar_adicao not in ['s', 'n']:
                            print("Opção inválida. Por favor, digite S ou N.")
                    
                    if continuar_adicao == 'n':
                        adicionando_registros = False
            
            elif escolha == 2:
                alterar_registro_diario_existente(conexao, cursor) 
            elif escolha == 3:
                excluir_registros_usuario(conexao, cursor)
            elif escolha == 4:
                exibir_registros_usuario(cursor)
            elif escolha == 5:
                calcular_e_salvar_media_geral_usuario(cursor)
                if conexao and cursor: 
                    conexao.commit() 

    except Exception as e:
        print(f"\nOcorreu um erro geral no processamento principal: {e}")
        if conexao:
            try:
                conexao.rollback()
                print("Rollback realizado devido ao erro.")
            except Exception as rb_err:
                print(f"Erro durante o rollback: {rb_err}")

    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as cur_err:
                print(f"Erro ao fechar o cursor: {cur_err}")
        if conexao:
            try:
                conexao.close()
                print("\nConexão com o banco de dados encerrada.")
            except Exception as con_err:
                print(f"Erro ao fechar a conexão: {con_err}")
        

if __name__ == "__main__":
    main()
