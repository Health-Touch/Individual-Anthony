import speedtest
import socket
import datetime
import time
from mysql.connector import connect

print("Bem Vindo à Aplicação Health Touch")

# Conectando com o workbench para fazer os inserts
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
    SELECT IP FROM rede WHERE IP = %s;
'''

queryInsertIp = '''
    INSERT INTO rede(IP) VALUES (%s);
'''

insert = [network_ip]

# Verificar se o IP já existe no banco de dados
cursor.execute(queryVerificarIp, insert)
existing_ip = cursor.fetchone()

if not existing_ip:
    cursor.execute(queryInsertIp, insert)
    connection.commit()
    print("Nova rede cadastrada!")
else:
    print("Essa rede já existe no banco. Nenhuma ação necessária.")

print("\nIniciando Seu Monitoramento...\r\n")

# Puxando a fkRede
query = "SELECT idRede FROM rede WHERE IP = %s;"
cursor.execute(query, (str(network_ip),))  # str força string
fkRedeRetorno = cursor.fetchall()
if fkRedeRetorno:
    fkRede = fkRedeRetorno[0][0]

while True:

    # Data
    data = datetime.datetime.now()

    # Medir a velocidade da Internet
    download_speed, upload_speed = get_speed()
    download = round(download_speed, 2)
    upload = round(upload_speed, 2)

    # Medir o ping
    pingV1 = get_ping()
    ping = round(pingV1, 2)
    
    query = '''
        INSERT INTO monitoramentoRede(upload, download, ping, dataHora, fkRede, fkMaquina, fkEmpresa, fkPLanoEmpresa, fkTipoMaquina, fkLocal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    insert = [
        upload, download, ping, data, fkRede, 1, 1, 1, 1, 1
    ]

    cursor.execute(query, insert)
    connection.commit()

    # Exibir os resultados
    print(f"IP da rede local: {network_ip}")
    print(f"Velocidade de Download: {download_speed:.2f} Mbps")
    print(f"Velocidade de Upload: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms\r\n")

    teste = 0
    if teste == 1:
        break

    time.sleep(40)
    
else:
    print("Login Inválido")
