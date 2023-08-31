import csv
import os
import pandas as pd
import openai

openai.api_key = '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'

def menu():
    """
    Menu para navegação do usuario. (1 - 6)
    """
    print('='*98)
    print(f"{'PROJETO VERÃO':^98}")
    print('='*98)
    print('''   
        1 - CADASTRAR USUARIO
        2 - IMC/BASAl
        3 - DIETA
        4 - TREINO
        5 - ROTINA 
        6 - TUDO
    ''')

    menu = int(input('DIGITE O NUMERO DA OPÇÃO:  '))

    if menu == 1:
        cadastrar_usuarios()
    elif menu == 2:
        saude_geral('clientes.csv')
    elif menu == 3:
        user_info = user_ID_info('clientes.csv')
        dieta(user_info)
    elif menu == 4:
        user_info = user_ID_info('clientes.csv')
        treino(user_info)
    elif menu == 5:
        user_info = user_ID_info('clientes.csv')
        rotina(user_info)
    elif menu == 6:
        user_info = user_ID_info('clientes.csv')
        dieta(user_info)
        treino(user_info)
        rotina(user_info)



def transform(nome, idade, peso, altura, sexo, atividade):
    """
    Calcula o metabolismo basal, de acorodo com o sexo do usuario 
    e retorna com 2 casa decimais
    """
    metabolismo_basal = 0
    
    if sexo == 'M':
        metabolismo_basal = 88.362 + (13.397 * peso) + (4.799 * altura * 100) - (5.677 * idade)
    else:
        metabolismo_basal = 447.593 + (9.247 * peso) + (3.098 * altura * 100) - (4.330 * idade)

    
    return f'{metabolismo_basal:.2f}'



def imc(nome, idade, peso, altura, sexo, atividade):
    """
    calcula o imc de um usuario e retorna com 2 casa decimais
    """

    imc = peso / (altura*altura)
    return f'{imc:.2f}'



def cadastrar_usuarios():
    """
    Cadastra informações de usuários em um arquivo CSV.

    Essa função coleta informações do usuario e salva em clientes.csv 
    Se o arquivo não existir, ele será criado e um cabeçalho será inserido.
    O usuário pode inserir vários registros consecutivos.
    """
    userID = 0

    
    niveis_atividade = {
        1: 'SEDENTARIO',
        2: 'lEVE',
        3: 'MODERADO',
        4: 'INTESO',
        5: 'MUITO INTENSO'
    }

    
    csv_file = 'clientes.csv'

    
    file_exists = os.path.isfile(csv_file)

    
    with open(csv_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        
        if not file_exists:
            csvwriter.writerow(['userID', 'nome', 'idade', 'peso', 'altura', 'atividade', 'sexo'])

        while True:
            print('=' * 60)
            userID += 1 if file_exists else +1  # Incrementa o userID a partir do último valor existente ou começa em 1
            nome = str(input('Digite seu nome: ')).strip().title()

            while True:
                try:
                    idade = int(input('Digite sua idade: '))
                    break
                except ValueError:
                    print('Por favor, digite um número válido para a idade.')

            while True:
                try:
                    peso = float(input('Digite seu peso (kg): '))
                    break
                except ValueError:
                    print('Por favor, digite um número válido para o peso.')

            while True:
                try:
                    
                    altura = float(input('Digite sua altura (m): ').replace(',','.'))
                    break
                except ValueError:
                    print('Por favor, digite um número válido para a altura.')

            while True:
                sexo = str(input('Sexo: (f/m) : ')).upper()
                if sexo not in ['F', 'M']:
                    sexo = str(input('Sexo inválido, digite novamente: ')).upper()
                else:
                    break
            while True:
                try:
                    print('='*25)
                    print('''
    1: \033[38;5;196mSEDENTARIO\033[0m
    2: \033[38;5;202mlEVE\033[0m
    3: \033[38;5;226mMODERADO\033[0m
    4: \033[38;5;118mINTESO\033[0m
    5: \033[38;5;46mMUITO INTENSO\033[0m
                        ''')
                    print('='*25)
                    nivel = int(input('Digite seu nível de atividade: '))
                    atividade = niveis_atividade.get(nivel)
                    if atividade is None:
                        print('Nível de atividade inválido.')
                    else:
                        csvwriter.writerow([userID, nome, idade, peso, altura, atividade, sexo])
                        break  # Sai do loop interno quando o nível de atividade é válido
                except ValueError:
                    print('Por favor, digite um número válido para o nível de atividade.')
            continuar = input('Deseja inserir outro usuário? (s/n) ')
            if continuar.lower() != 's':
                print('Programa encerrado.')
                break
            
            
            
def saude_geral(arquivo_csv):
    """
    Exibe informações de saúde geral para os usuários presentes em um arquivo CSV.

    Args:
        arquivo_csv (str): O caminho para o arquivo CSV contendo informações dos usuários.

    """
    print("="*115)
    print (f"{'CALCULO DO IMC E GASTO BASAL':^95}")
    print("="*115)


    df = pd.read_csv(arquivo_csv, delimiter=',')
    df.columns = df.columns.str.strip()


    users = []
    for _, row in df.iterrows():
        user_dict = {
            'userID': row['userID'],
            'nome': row['nome'],
            'idade': row['idade'],
            'peso': row['peso'],
            'altura': row['altura'],
            'atividade': row['atividade'], 
            'sexo': row['sexo'] 
        }
        users.append(user_dict)

    # Imprime cabeçalho da tabela
    print(f"{'userID':<7}|{'Nome':<15}|{'Idade':<10}|{'Peso (kg)':<10}|{'Altura (m) ':<10}|{'Atividade':<15}|\033[91m{'Basal':<10}{'|''IMC':>14}\033[0m")
    print("="*115)  # Linha de separação

    for user in users:
        userID = user['userID']
        nome = user['nome']
        idade = user['idade']
        peso = user['peso']
        altura = user['altura']
        sexo = user['sexo']
        atividade = user['atividade']
        result = transform(nome, idade, peso, altura, sexo, atividade)
        imc_user = imc(nome, idade, peso, altura, sexo, atividade)

        print(f"{userID:<7}|{nome:<15}|{idade:<10}|{peso:<10}|{altura:<10} |{atividade:<15}|{result:<20}|{imc_user:<20}")

    print("="*115)
    


def user_ID_info(arquivo_csv):
    """
    Pega informaçoes de um usuario(userID) apartir do .CSV 
    A função retorna um diconario com o cabeçalho e as informaçoes do seu usuario(userID) respctivamente.

    Args:
        arquivo_csv (str): arquivo csv

    Returns:
        dict: Um dicionário contendo as informações do usuário (userID, nome, idade, peso, altura, atividade, sexo).
            Retorna None se o userID não for encontrado.
    """
    saude_geral(arquivo_csv)
    print('QUAl cliente voce gostaria de fazer uma dieta')
    userID = int(input('Digite o userID do cliente: '))

    
    arquivo_csv = "clientes.csv"  
    df = pd.read_csv(arquivo_csv, delimiter=',')
    df.columns = df.columns.str.strip()

   
    target_user_id = userID  # Substitua pelo userID desejado

    
    user_row = df[df['userID'] == target_user_id]

    if not user_row.empty:
        user_info = {
            'userID': user_row['userID'].values[0],
            'nome': user_row['nome'].values[0],
            'idade': user_row['idade'].values[0],
            'peso': user_row['peso'].values[0],
            'altura': user_row['altura'].values[0],
            'atividade': user_row['atividade'].values[0],
            'sexo': user_row['sexo'].values[0],
        }
        print("Informações do usuário encontradas:")
        return user_info
    else:
        print(f"UserID {target_user_id} não encontrado no DataFrame.")




def dieta(user_info):
    """
    Gera uma dieta personalizado com base nas informações do usuário e envia para save_to_txt.

    Args:
        user_info (dict): Um dicionário contendo as informações do usuário (userID, Nome, Idade, Peso (kg), Altura (m), Atividade, Basal, IMC).

    Returns:
        texto gerado pelo chat gpt (dieta).
    """
    prompt = f"Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}\napenas me de 7 refeiçoes bem detalhadas com base nisso em tópicos"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    dieta_text = response.choices[0].message['content'].strip()
    save_to_txt(dieta_text, 'Dieta')
    


def treino(user_info):
    """
    Gera um treino personalizado com base nas informações do usuário e envia para save_to_txt.

    Args:
        user_info (dict): Um dicionário contendo as informações do usuário (userID, Nome, Idade, Peso (kg), Altura (m), Atividade, Basal, IMC).

    Returns:
        texto gerado pelo chat gpt (treino).
    """
    prompt = f"Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}\npenas me de 3 treinos hipertroficos bem detalhados completo em tópicos, sem explicação"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    treino_text = response.choices[0].message['content'].strip()
    save_to_txt(treino_text, 'Treino')



def rotina(user_info):
    """
    Gera uma rotina personalizada com base nas informações do usuário e envia para save_to_txt

    Args:
        user_info (dict): Um dicionário contendo as informações do usuário (userID, Nome, Idade, Peso (kg) ,Altura (m), Atividade,).

    Returns:
        texto gerado pelo chat gpt (rotina).
    """
   
    prompt = f"Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}\napenas me de uma rotina de bons Habitos (24H) detalhada com base nisso em topicos, sem explicaçao"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    rotina_text = response.choices[0].message['content'].strip()
    save_to_txt(rotina_text, 'Rotina')



def save_to_txt(content, filename):
    """
    Salva o conteúdo em um arquivo de texto.

    Args:
        content (str): O conteúdo que será salvo no arquivo.
        filename (str): O nome para o arquivo .
    """
    filename = filename + '.txt'
    with open(filename, "w") as file:
        file.write(content)
    print(f"Arquivo '{filename}' salvo com sucesso.")


