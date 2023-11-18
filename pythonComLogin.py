import speedtest
import socket
import datetime
import time
from mysql.connector import connect

# Conectando com o Workbench para fazer os selects
conn = connect(
    host='localhost',
    user='root',
    password='sptech',
    database='HealthTouch'
)

cursor = conn.cursor()

print("Bem Vindo à Aplicação Health Touch")
email = input("Digite seu e-mail:")
senha = input("Digite sua senha:")

# puxando todos os dados do colaborador
query = "SELECT * FROM Colaborador WHERE email = %s AND senha = %s"
cursor.execute(query, (email, senha))
resultado = cursor.fetchone()

# puxando somente o nome do colaborador
query = "SELECT nome FROM Colaborador WHERE email = %s AND senha = %s"
cursor.execute(query, (email, senha))
nome = cursor.fetchone()

# puxando o cargo
query = "SELECT fkNivelAcesso FROM Colaborador WHERE email = %s AND senha = %s"
cursor.execute(query, (email, senha))
fkNivelAcesso = cursor.fetchone()

# puxando a fkEmpresa
query = "SELECT fkEmpresa FROM Colaborador WHERE email = %s AND senha = %s"
cursor.execute(query, (email, senha))
fkEmpresa = cursor.fetchone()

# completando o nome dos cargos
if fkNivelAcesso:
    fkNivelAcesso = fkNivelAcesso[0]

    if fkNivelAcesso == 1:
        cargo = "Representante Legal"
    elif fkNivelAcesso == 2:
        cargo = "Gerente de TI"
    elif fkNivelAcesso == 3:
        cargo = "Equipe de TI"

# validando login
if resultado:
    print('\r\n')
    print(f"Login bem-sucedido. Logado como {nome[0]} - {cargo}")

    # puxando todas as máquinas cadastradas
    query = "select idMaquina, SO, IP, sala, andar, nome from Maquina JOIN LocalSala on fkLocal = idLocalSala join setor on fkSetor = idSetor;"
    cursor.execute(query)
    maquinas = cursor.fetchall()

    # printando as máquinas disponíveis
    print('\r\n')
    print('Lista de máquinas disponíveis para monitoramento:\r\n')
    for maquina in maquinas:
        print("ID da Máquina:", maquina[0], "- Sistema Operacional:", maquina[1], "- Endereço IP:",
              maquina[2], "- Sala:", maquina[3], "- Andar:", maquina[4], "- Setor:", maquina[5], "\n")

    # puxando a fkMaquina
    idMaquinaSelect = input("Qual o ID da máquina que você quer monitorar?")
    query = "SELECT idMaquina FROM Maquina WHERE idMaquina = %s"
    cursor.execute(query, (idMaquinaSelect,))
    fkMaquina = cursor.fetchone()

    # Função para obter o endereço IP da rede local
    def get_network_ip():
        try:
            hostname = socket.gethostname()
            network_ip = socket.gethostbyname(hostname)
            return network_ip
        except socket.gaierror:
            return 'N/A'

    # Obter o IP da rede
    network_ip = get_network_ip()

    # Função para medir a velocidade da Internet
    def get_speed():
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Convertendo para Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convertendo para Mbps
        return download_speed, upload_speed

    # Função para medir o ping
    def get_ping():
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping
        return ping

    queryVerificarIp = '''
        select IP from rede where IP = %s;
    '''

    queryInsertIp = '''
        insert into rede(IP) values (%s);
    '''

    insert = [network_ip]

    # verificar se o IP já existe no banco de dados
    cursor.execute(queryVerificarIp, insert)
    existing_ip = cursor.fetchone()

    if not existing_ip:
        cursor.execute(queryInsertIp, insert)
        conn.commit()
        print("Nova rede cadastrada!")
    else:
        print("Esse rede já existe no banco. Nenhuma ação necessária.")

    print("\nIniciando Seu Monitoramento...\r\n")

    # puxando a fkRede
    query = "select idRede from rede where IP = %s;"
    cursor.execute(query, (str(network_ip),))  # str força string
    fkRedeRetorno = cursor.fetchall()
    if fkRedeRetorno:
        fkRede = fkRedeRetorno[0][0]

    # puxando a fkPlanoEmpresa
    query = "SELECT fkPlanoEmpresa FROM Maquina WHERE idMaquina = %s"
    cursor.execute(query, (idMaquinaSelect,))
    fkPlanoEmpresa = cursor.fetchone()

    # puxando a fkTipoMaquina
    query = "SELECT fkTipoMaquina FROM Maquina WHERE idMaquina = %s"
    cursor.execute(query, (idMaquinaSelect,))
    fkTipoMaquina = cursor.fetchone()

    # puxando a fkLocal
    query = "select fkLocal from maquina WHERE idMaquina = %s"
    cursor.execute(query, (idMaquinaSelect,))
    fkLocal = cursor.fetchone()

    # conectando com o workbench para fazer os inserts
def mysql_connection(host, user, passwd, database=None):
    connection = connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    return connection

connection = mysql_connection('localhost', 'root', 'sptech', 'HealthTouch')

cursor = connection.cursor()
while True:

    # data
    data = datetime.datetime.now()

    # Medir a velocidade da Internet
    download_speed, upload_speed = get_speed()
    download = round(download_speed, 2)
    upload = round(upload_speed, 2)

    # Medir o ping
    pingV1 = get_ping()
    ping = round(pingV1, 2)
    
    query = '''
            insert into monitoramentoRede(upload, download, ping, dataHora, fkRede, fkMaquina, fkEmpresa, fkPLanoEmpresa, fkTipoMaquina, fkLocal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''

    insert = [
        upload, download, ping, data, fkRede, fkMaquina[0], fkEmpresa[0], fkPlanoEmpresa[0], fkTipoMaquina[0], fkLocal[0]
    ]

    cursor.execute(query, insert)
    connection.commit()

    # Exibir os resultados
    print(f"IP da rede local: {network_ip}")
    print(f"Velocidade de Download: {download_speed:.2f} Mbps")
    print(f"Velocidade de Upload: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms\r\n")

    time.sleep(40)
    
else:
    print("Login Inválido")
