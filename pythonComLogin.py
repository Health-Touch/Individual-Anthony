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

print("\nIniciando Seu Monitoramento...\r\n")

while True:
    # Função para obter o endereço IP da rede local
    def get_network_ip():
        try:
            hostname = socket.gethostname()
            network_ip = socket.gethostbyname(hostname)
            return network_ip
        except socket.gaierror:
            return 'N/A'

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

    # Obter o IP da rede
    network_ip = get_network_ip()

    # Medir a velocidade da Internet
    download_speed, upload_speed = get_speed()
    download = round(download_speed,2)
    upload = round(upload_speed,2)

    # Medir o ping
    pingV1 = get_ping()
    ping = round(pingV1,2)

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
    
    queryVerificarIp = '''
        select IP from rede where IP = %s;
    '''

    queryInsertIp = '''
        insert into rede(IP) values (%s);
    '''

    insert = [network_ip]

    cursor = connection.cursor()

    # verificar se o IP já existe no banco de dados
    cursor.execute(queryVerificarIp, insert)
    existing_ip = cursor.fetchone()

    if not existing_ip:
        cursor.execute(queryInsertIp, insert)
        connection.commit()
        print("Nova rede cadastrada!")
    else:
        print("Esse rede já existe no banco. Nenhuma ação necessária.")

    # puxando a fkRede
    query = "select idRede from rede where IP = %s;"
    cursor.execute(query, (str(network_ip),)) #str força string
    fkRedeRetorno = cursor.fetchall()
    if fkRedeRetorno:
        fkRede = fkRedeRetorno[0][0]
        
    # data
    data = datetime.datetime.now()

    query = '''
            insert into monitoramentoRede(upload, download, ping, dataHora, fkRede, fkMaquina, fkEmpresa, fkPLanoEmpresa, fkTipoMaquina, fkLocal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''
    
    insert = (upload, download, ping, data, fkRede, 1, 1, 1, 1, 1)

    cursor = connection.cursor()
    cursor.execute(query, insert)
    connection.commit()

    # Exibir os resultados
    print(f"IP da rede local: {network_ip}")
    print(f"Velocidade de Download: {download_speed:.2f} Mbps")
    print(f"Velocidade de Upload: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms\r\n")

    time.sleep(5)
