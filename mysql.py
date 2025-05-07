import pymysql
from datetime import datetime, timedelta

def conectar_banco():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Yuri.1325',
        database='banco_de_dados',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

def criar_tabelas(cursor):
    """Função para criar as tabelas se não existirem"""
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

def coletar_dados():
    """Coleta todos os dados do usuário"""
    dados = {}
    print('\n--- NOVO REGISTRO DE SUSTENTABILIDADE ---')
    
    dados['nome'] = input('\nDigite seu nome: ')
    dados['data'] = coletar_data()
    
    # Coleta de dados numéricos com validação
    dados['litros_agua'] = coletar_numero('Litros de água consumidos: ')
    dados['kwh_de_energia'] = coletar_numero('kWh de energia consumidos: ')
    dados['nao_reciclaveis'] = coletar_numero('Resíduo não reciclável (kg): ', tipo='float')
    dados['reciclaveis'] = coletar_numero('Resíduo reciclável (%): ')
    
    # Coleta de dados de transporte
    print('\nTransportes utilizados (S/N):')
    dados['Publico'] = input('Transporte público: ').lower()
    dados['Bicicleta'] = input('Bicicleta: ').lower()
    dados['Pe'] = input('Caminhada: ').lower()
    dados['Fossilp'] = input('Carro à gasolina: ').lower()
    dados['Eletrico'] = input('Carro elétrico: ').lower()
    dados['Fossilc'] = input('Carona: ').lower()
    
    return dados

def coletar_data():
    """Coleta e valida a data"""
    data_valida = False
    while not data_valida:
        try:
            data_input = input('Data (DD/MM/AAAA): ')
            dia, mes, ano = map(int, data_input.split('/'))
            data = f'{ano}-{mes:02d}-{dia:02d}'
            datetime.strptime(data, '%Y-%m-%d')
            data_valida = True
            return data
        except ValueError:
            print("Formato inválido. Use DD/MM/AAAA.")

def coletar_numero(mensagem, tipo='int'):
    """Coleta e valida números"""
    valido = False
    while not valido:
        try:
            valor = input(mensagem)
            if tipo == 'float':
                return float(valor)
            return int(valor)
        except ValueError:
            print("Valor inválido. Digite um número.")

def calcular_classificacoes(dados):
    """Calcula todas as classificações de sustentabilidade"""
    # Classificação de Água
    if dados['litros_agua'] <= 150:
        dados['agua_classificacao'] = 'alta'
        dados['agua_desc'] = 'Sustentável'
    elif dados['litros_agua'] <= 200:
        dados['agua_classificacao'] = 'moderada'
        dados['agua_desc'] = 'Moderado'
    else:
        dados['agua_classificacao'] = 'baixa'
        dados['agua_desc'] = 'Não sustentável'

    # Classificação de Energia
    if dados['kwh_de_energia'] <= 5:
        dados['energia_classificacao'] = 'alta'
        dados['energia_desc'] = 'Sustentável'
    elif dados['kwh_de_energia'] <= 10:
        dados['energia_classificacao'] = 'moderada'
        dados['energia_desc'] = 'Moderado'
    else:
        dados['energia_classificacao'] = 'baixa'
        dados['energia_desc'] = 'Não sustentável'

    # Classificação de Resíduos Não Recicláveis
    if dados['nao_reciclaveis'] <= 1.5:
        dados['nao_reciclavel_classificacao'] = 'alta'
        dados['nao_reciclavel_desc'] = 'Sustentável'
    elif dados['nao_reciclaveis'] <= 2.5:
        dados['nao_reciclavel_classificacao'] = 'moderada'
        dados['nao_reciclavel_desc'] = 'Moderado'
    else:
        dados['nao_reciclavel_classificacao'] = 'baixa'
        dados['nao_reciclavel_desc'] = 'Não sustentável'

    # Classificação de Resíduos Recicláveis
    if dados['reciclaveis'] >= 50:
        dados['reciclavel_classificacao'] = 'alta'
        dados['reciclavel_desc'] = 'Sustentável'
    elif dados['reciclaveis'] >= 20:
        dados['reciclavel_classificacao'] = 'moderada'
        dados['reciclavel_desc'] = 'Moderado'
    else:
        dados['reciclavel_classificacao'] = 'baixa'
        dados['reciclavel_desc'] = 'Não sustentável'

    # Classificação de Transporte
    sustentaveis = sum([dados['Publico'] == 's', dados['Bicicleta'] == 's', 
                       dados['Pe'] == 's', dados['Eletrico'] == 's'])
    nao_sustentaveis = sum([dados['Fossilp'] == 's', dados['Fossilc'] == 's'])

    if nao_sustentaveis == 0 and sustentaveis > 0:
        dados['transporte_classificacao'] = 'alta'
        dados['transporte_desc'] = 'Sustentável'
    elif sustentaveis > nao_sustentaveis:
        dados['transporte_classificacao'] = 'moderada'
        dados['transporte_desc'] = 'Moderado'
    else:
        dados['transporte_classificacao'] = 'baixa'
        dados['transporte_desc'] = 'Não sustentável'

    # Classificação Geral
    classificacoes = [
        dados['agua_classificacao'],
        dados['energia_classificacao'],
        dados['nao_reciclavel_classificacao'],
        dados['reciclavel_classificacao'],
        dados['transporte_classificacao']
    ]

    altas = classificacoes.count('alta')
    baixas = classificacoes.count('baixa')

    if baixas >= 3:
        dados['classificacao_geral'] = 'Não sustentável'
    elif altas >= 3 and baixas == 0:
        dados['classificacao_geral'] = 'Sustentável'
    else:
        dados['classificacao_geral'] = 'Moderado'

    return dados

def inserir_dados(cursor, dados):
    """Insere os dados na tabela Sustentabilidade"""
    cursor.execute('''
        INSERT INTO Sustentabilidade (
            nome, data, litros_agua, agua_classificacao, eletricidade_Kw, energia_classificacao,
            nao_reciclaveis, nao_reciclavel_classificacao, reciclaveis, reciclavel_classificacao,
            publico, bicicleta, pe, Fossilp, Eletrico, Fossilc, transporte_classificacao, classificacao_geral
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        dados['nome'], dados['data'],
        dados['litros_agua'], dados['agua_classificacao'],
        dados['kwh_de_energia'], dados['energia_classificacao'],
        dados['nao_reciclaveis'], dados['nao_reciclavel_classificacao'],
        dados['reciclaveis'], dados['reciclavel_classificacao'],
        'sim' if dados['Publico'] == 's' else 'nao',
        'sim' if dados['Bicicleta'] == 's' else 'nao',
        'sim' if dados['Pe'] == 's' else 'nao',
        'sim' if dados['Fossilp'] == 's' else 'nao',
        'sim' if dados['Eletrico'] == 's' else 'nao',
        'sim' if dados['Fossilc'] == 's' else 'nao',
        dados['transporte_classificacao'],
        dados['classificacao_geral']
    ))

def calcular_medias(cursor, nome, data):
    """Calcula e insere as médias dos últimos 7 dias"""
    data_hoje = datetime.strptime(data, '%Y-%m-%d').date()
    data_inicial = data_hoje - timedelta(days=7)

    cursor.execute('''
        SELECT 
            GROUP_CONCAT(litros_agua SEPARATOR ', '),
            AVG(litros_agua),
            GROUP_CONCAT(eletricidade_Kw SEPARATOR ', '),
            AVG(eletricidade_Kw),
            GROUP_CONCAT(nao_reciclaveis SEPARATOR ', '),
            AVG(nao_reciclaveis),
            GROUP_CONCAT(reciclaveis SEPARATOR ', '),
            AVG(reciclaveis)
        FROM Sustentabilidade 
        WHERE nome = %s AND data BETWEEN %s AND %s
    ''', (nome, data_inicial, data_hoje))
    
    resultado = cursor.fetchone()
    
    if resultado and all(resultado):
        (valores_agua, media_agua, 
         valores_energia, media_energia, 
         valores_nao_reciclaveis, media_nao_reciclaveis, 
         valores_reciclaveis, media_reciclaveis) = resultado
        
        cursor.execute('''
            INSERT INTO MediasSustentabilidade (
                nome, data_inicial, data_final,
                valores_agua, media_agua,
                valores_energia, media_energia,
                valores_nao_reciclaveis, media_nao_reciclaveis,
                valores_reciclaveis, media_reciclaveis
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            nome, data_inicial, data_hoje,
            valores_agua, round(float(media_agua), 2) if media_agua else 0,
            valores_energia, round(float(media_energia), 2) if media_energia else 0,
            valores_nao_reciclaveis, round(float(media_nao_reciclaveis), 2) if media_nao_reciclaveis else 0,
            valores_reciclaveis, round(float(media_reciclaveis), 2) if media_reciclaveis else 0
        ))

def mostrar_resultados(dados):
    """Exibe os resultados para o usuário"""
    print('\n--- RESULTADOS ---')
    print(f"Água: {dados['litros_agua']}L - {dados['agua_desc']}")
    print(f"Energia: {dados['kwh_de_energia']}kWh - {dados['energia_desc']}")
    print(f"Resíduos não recicláveis: {dados['nao_reciclaveis']:.1f}kg - {dados['nao_reciclavel_desc']}")
    print(f"Resíduos recicláveis: {dados['reciclaveis']}% - {dados['reciclavel_desc']}")
    print(f"Transporte: {dados['transporte_desc']}")
    print(f"\nCLASSIFICAÇÃO GERAL: {dados['classificacao_geral']}")

def main():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    criar_tabelas(cursor)

    continuar = 's'
    while continuar == 's':
        dados = coletar_dados()
        dados = calcular_classificacoes(dados)
        
        try:
            inserir_dados(cursor, dados)
            calcular_medias(cursor, dados['nome'], dados['data'])
            conexao.commit()
            mostrar_resultados(dados)
        except Exception as e:
            print(f"\nErro ao salvar dados: {e}")
            conexao.rollback()

        continuar = input('\nDeseja inserir outro registro? (S/N): ').lower()
        while continuar not in ['s', 'n']:
            print("Por favor, digite S ou N")
            continuar = input('Deseja inserir outro registro? (S/N): ').lower()

    cursor.close()
    conexao.close()
    print("\nPrograma encerrado.")

if __name__ == "__main__":
    main()
