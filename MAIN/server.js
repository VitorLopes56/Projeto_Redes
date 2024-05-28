const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Nova conexão estabelecida');

  ws.on('message', (message) => {
    console.log(`Mensagem recebida do cliente: ${message}`);
    // Enviar mensagem para todos os clientes conectados
    wss.clients.forEach((client) => {
      client.send(message);
    });
  });

  ws.on('close', () => {
    console.log('Conexão fechada');
  });

  ws.on('error', (error) => {
    console.error(`Erro na conexão: ${error}`);
  });
});