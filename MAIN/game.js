const socket = new WebSocket('ws://localhost:8080');

socket.onopen = () => {
  console.log('Conexão estabelecida com o servidor');
};

socket.onmessage = (event) => {
  console.log(`Mensagem recebida do servidor: ${event.data}`);
  // Atualize o chat com a mensagem recebida
  const messageList = document.getElementById('messages');
  const message = document.createElement('li');
  message.textContent = event.data;
  messageList.appendChild(message);
};

socket.onclose = () => {
  console.log('Conexão fechada com o servidor');
};

socket.onerror = (error) => {
  console.error(`Erro na conexão com o servidor: ${error}`);
};

// Enviar mensagem do chat ao servidor
document.getElementById('send').addEventListener('click', () => {
  const message = document.getElementById('message').value;
  socket.send(message);
  document.getElementById('message').value = '';
});