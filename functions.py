from time import sleep
import csv
import os
import pandas as pd
import openai
from fpdf import FPDF

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
                                        6 - TUDO (Dieta, Treino, Rotina)
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
                print('='*25)
                choice()
            
            
            
def saude_geral(arquivo_csv):
    """
    Exibe informações de saúde geral para os usuários presentes em um arquivo CSV.

    Args:
        arquivo_csv (str): O caminho para o arquivo CSV contendo informações dos usuários.

    """
    print('\033[34m')
    print("="*101)
    print('\033[0m')
    print(f"\033[1m{'CALCULO DO IMC E GASTO BASAL':^95}\033[m")
    print('\033[34m')
    print("="*101)
    print('\033[0m')


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
    print('\033[1m')
    print(f"{'userID':<7}|{'Nome':<15}|{'Idade':<10}|{'Peso (kg)':<10}|{'Altura (m) ':<10}|{'Atividade':<15}|\033[91m{'Basal':<10}{'|''IMC':>14}\033[0m")
    print("-"*101)  # Linha de separação

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

    print("="*101)

    


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
    comentario = str(input('Digite suas restrições alimentares:  '))
    prompt = f"""Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}
    \napenas me de 5 refeiçoes bem detalhadas (24h) em tópicos. Condições = ({comentario})"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an excellent nutritionist."},
            {"role": "user", "content": prompt},
        ]
    )

    dieta_text = response.choices[0].message['content'].strip()
    save_to_txt(user_info ,dieta_text, 'Dieta')
    save_to_pdf(user_info ,dieta_text, 'Dieta')
    


def treino(user_info):
    """
    Gera um treino personalizado com base nas informações do usuário e envia para save_to_txt.

    Args:
        user_info (dict): Um dicionário contendo as informações do usuário (userID, Nome, Idade, Peso (kg), Altura (m), Atividade, Basal, IMC).

    Returns:
        texto gerado pelo chat gpt (treino).
    """
    objetivo = str(input('Digite seu objetivo de treino, em poucas palavras :  '))
    restri_fisica = str(input('Se possuir, digite alguma restrição física  :  '))
    prompt = f"""Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}
    \napenas me de 3 treinos com o objetivo = ({objetivo}) bem detalhados completo em tópicos, restrição={restri_fisica}"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an excellent nutritionist"},
            {"role": "user", "content": prompt},
        ]
    )

    treino_text = response.choices[0].message['content'].strip()
    save_to_txt(user_info,treino_text, 'Treino')
    save_to_pdf(user_info,treino_text, 'Treino')



def rotina(user_info):
    """
    Gera uma rotina personalizada com base nas informações do usuário e envia para save_to_txt

    Args:
        user_info (dict): Um dicionário contendo as informações do usuário (userID, Nome, Idade, Peso (kg) ,Altura (m), Atividade,).

    Returns:
        texto gerado pelo chat gpt (rotina).
    """
    restricoes = str(input('Se houver, digite sua restrição:  '))
    prompt = f"Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}\napenas me de uma rotina de bons Habitos (24H) detalhada com base nisso em topicos, restriçoes = {restricoes}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an excellent nutritionist."},
            {"role": "user", "content": prompt},
        ]
    )

    rotina_text = response.choices[0].message['content'].strip()
    save_to_txt(user_info,rotina_text, 'Rotina')
    save_to_pdf(user_info,rotina_text, 'Rotina')





def save_to_txt(user_info, content, filename):
    """
    Salva o conteúdo em um arquivo de texto dentro de uma pasta com o nome do usuário.

    Args:
        user_info (dict): Informações do usuário, incluindo o nome.
        content (str): O conteúdo que será salvo no arquivo.
        filename (str): O nome base para o arquivo.
    """
    user_folder = user_info['nome']
    os.makedirs(user_folder, exist_ok=True) 
    filename = os.path.join(user_folder, f"{filename}_{user_info['nome']}.txt")
    
    with open(filename, "w") as file:
        file.write(content)
    print(f"Arquivo '{filename}' salvo com sucesso.")
    choice()



def save_to_pdf(user_info,content, filename):
    user_folder = user_info['nome']
    os.makedirs(user_folder, exist_ok=True)  
    filename = os.path.join(user_folder, f"{filename}_{user_info['nome']}.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename +'_'+ user_info['nome']+'.pdf') 
    print(f"Arquivo '{filename}' salvo com sucesso.") 
    choice()
    


def choice():
    sleep(1.5)
    print('='*25)

    print(f"{'ESCOLHA UMA OPÇÃO':^25}")
    print('='*25)
    print('''
0 -  FINALIZAR PROGRAMA
1 -  VOLTAR PARA O MENU
    ''')
    user_choice = input(':')

                
    if user_choice in "01":
        if user_choice == '1':
            menu()
        elif user_choice == '0':
            print('Programa encerrado.')
            exit()
    else:
        print('\033[38;5;196m-'*25)
        print('DIGITE UM VALOR VALIDO')
        print('\033[38;5;196m-\033[0m'*25)
        sleep(1.5)
        choice()
        