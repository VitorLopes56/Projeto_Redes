import socket
import threading
import os
import struct
import time
import select
#Vitor Gabriel Lopes Souza /  Bruno Constatino
# função do protocolo TCP
def tcp_client():
    host = 'localhost'
    port = 12345

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        message = input("Digite a mensagem para enviar ao servidor: ")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print('Mensagem recebida do servidor:', data.decode())
    except Exception as e:
        print("Erro:", e)
    finally:
        client_socket.close()
        

# função do protocolo UDP
def udp_client():
    host = 'localhost'
    port = 12345

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = input("Digite a mensagem para enviar ao servidor: ")
        client_socket.sendto(message.encode(), (host, port))

    except Exception as e:
        print("Erro:", e)
    finally:
        client_socket.close()
        

# função chat
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print(data.decode())
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            break


def chat_client():
    host = 'localhost'
    port = 12345

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        while True:
            message = input()
            if message.lower() == 'sair':
                break
            client_socket.sendall(message.encode())
    except Exception as e:
        print("Erro:", e)
    finally:
        client_socket.close()
        

# função ICMP
def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def icmp_ping(host):
    try:
        icmp = socket.getprotobyname("icmp")
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        my_socket.settimeout(1)
        my_id = os.getpid() & 0xFFFF
        dest_addr = socket.gethostbyname(host)
        
        def send_one_ping(my_socket, dest_addr, my_id):
            my_checksum = 0
            header = struct.pack("bbHHh", 8, 0, my_checksum, my_id, 1)
            data = struct.pack("d", time.time())
            my_checksum = checksum(header + data)
            header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), my_id, 1)
            packet = header + data
            my_socket.sendto(packet, (dest_addr, 1))
        
        def receive_one_ping(my_socket, my_id, timeout):
            time_left = timeout
            while True:
                start_select = time.time()
                what_ready = select.select([my_socket], [], [], time_left)
                how_long_in_select = (time.time() - start_select)
                if what_ready[0] == []:  # Timeout
                    return

                time_received = time.time()
                rec_packet, addr = my_socket.recvfrom(1024)
                icmp_header = rec_packet[20:28]
                type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)
                if packet_id == my_id:
                    bytes_in_double = struct.calcsize("d")
                    time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
                    return time_received - time_sent, addr[0]

                time_left = time_left - how_long_in_select
                if time_left <= 0:
                    return

        send_one_ping(my_socket, dest_addr, my_id)
        delay = receive_one_ping(my_socket, my_id, 1)
        my_socket.close()
        
        if delay is None:
            print(f"Falha ao pingar {host}.")
        else:
            print(f"Resposta de {host} em {delay[0]*1000:.2f} ms.")
    
    except Exception as e:
        print("Erro:", e)


def traceroute(host):
    try:
        icmp = socket.getprotobyname("icmp")
        udp = socket.getprotobyname("udp")
        ttl = 1
        max_hops = 30
        port = 33434

        dest_addr = socket.gethostbyname(host)
        
        while True:
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
            recv_socket.settimeout(2)
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            recv_socket.bind(("", port))
            
            start_time = time.time()
            send_socket.sendto(b"", (dest_addr, port))
            
            curr_addr = None
            curr_name = None
            try:
                data, curr_addr = recv_socket.recvfrom(512)
                end_time = time.time()
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error:
                pass
            finally:
                send_socket.close()
                recv_socket.close()
            
            if curr_addr is not None:
                curr_host = f"{curr_name} ({curr_addr})"
            else:
                curr_host = "*"
                
            print(f"{ttl}\t{curr_host}\t{(end_time - start_time) * 1000:.2f} ms")
            
            ttl += 1
            if curr_addr == dest_addr or ttl > max_hops:
                break
    
    except Exception as e:
        print("Erro:", e)


def menu():
    print("Escolha o protocolo de comunicação:")
    print("1. TCP")
    print("2. UDP")
    print("3. Chat")
    print("4. ICMP Ping")
    print("5. Traceroute")
    print("6. Encerrar")
    return input("Digite o número da opção desejada: ")

def inicia():
    opcao = menu()

    if opcao == '1':
        tcp_client()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '2':
        udp_client()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '3':
        chat_client()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '4':
        host = input("Digite o endereço IP para pingar: ")
        icmp_ping(host)
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '5':
        host = input("Digite o endereço IP ou hostname para traceroute: ")
        traceroute(host)
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '6':
        exit()
    else:
        print("\nOpção inválida. Por favor, escolha uma opção válida.\n")
        print("\n===============================================================================\n")
        inicia()
        
inicia()
