import speedtest
import socket
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

    # Medir o ping
    ping = get_ping()

    # conectando com o workbench para fazer os inserts
    def mysql_connection(host, user, passwd, database=None):
        connection = connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        return connection

    # aqui colocar suas credencias do banco
    connection = mysql_connection('localhost', 'root', 'sptech', 'HealthTouch')

    # Exibir os resultados
    print(f"IP da rede local: {network_ip}")
    print(f"Velocidade de Download: {download_speed:.2f} Mbps")
    print(f"Velocidade de Upload: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms\r\n")

    time.sleep(5)

else:
    print("Login Inválido")