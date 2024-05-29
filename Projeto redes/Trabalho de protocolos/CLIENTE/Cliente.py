import socket
import threading
#Vitor Gabriel Lopes Souza /  Bruno Constatino
#função TCP
def tcp_server():
    host = 'localhost'
    port = 12345

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print("Servidor TCP esperando por conexões...")
        while True:
            client_socket, client_address = server_socket.accept()
            print("Conexão recebida de:", client_address)
            data = client_socket.recv(1024)
            print('Mensagem recebida do cliente:', data.decode())
            client_socket.sendall("Mensagem recebida com sucesso!".encode()) 
            client_socket.close()
            break
    
    except Exception as e:
        print("Erro:", e)
    
    finally:
        server_socket.close()
        
    return
        
    


#função UDP
def udp_server():
    host = 'localhost'
    port = 12345

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))
        print("Servidor UDP esperando por mensagens...")
        while True:
            data, client_address = server_socket.recvfrom(1024)
            print("Mensagem recebida do cliente:", data.decode())
            break
    except Exception as e:
        print("Erro:", e)
    finally:
        server_socket.close()
        



#função chat

# Função para lidar com a comunicação do cliente
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode())
                # Aqui você pode adicionar lógica para processar a mensagem do cliente, se necessário
                # Neste exemplo, estamos apenas enviando uma mensagem de volta para o cliente
                response = "Mensagem recebida com sucesso!"
                client_socket.send(response.encode())
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            break

# Função principal do servidor de chat
def chat_server():
    host = 'localhost'
    port = 12345

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)  # Permitindo apenas uma conexão de cliente
        print("Servidor de Chat esperando por conexões...")
        client_socket, client_address = server_socket.accept()
        print("Conexão recebida de:", client_address)
        
        # Iniciando a thread para lidar com a comunicação do cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        
        # Agora o servidor pode enviar mensagens para o cliente
        while True:
            message_to_send = input()
            client_socket.send(message_to_send.encode())
            
    except Exception as e:
        print("Erro:", e)
    finally:
        server_socket.close()


        


def menu():
    print("Escolha a funcionalidade do servidor:")
    print("1. TCP")
    print("2. UDP")
    print("3. Chat")
    print("4. ICMP")
    print("5. Traceroute")
    print("6. Encerrar")
    return input("Digite o número da opção desejada: ")


def inicia():
    opcao = menu()

    if opcao == '1':
        tcp_server()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '2':
        udp_server()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '3':
        chat_server()
        print("\n===============================================================================\n")
        inicia()
    elif opcao == '6':
        exit()
    else:
        print("\nOpção inválida. Por favor, escolha uma opção válida.\n")
        print("\n===============================================================================\n")
        inicia()
        

inicia()