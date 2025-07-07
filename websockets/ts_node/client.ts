import WebSocket from 'ws';

const ws = new WebSocket('ws://localhost:8080');

const messages = ['Hello', 'How are you?', 'Goodbye'];
let sentCount = 0;

ws.on('open', () => {
  console.log("WebSocket client connected");

  // Send the first message
  ws.send(messages[sentCount]);
});

ws.on('message', (data) => {
  console.log(`Client received: ${data}`);

  sentCount++;

  if (sentCount < messages.length) {
    // Send the next message
    ws.send(messages[sentCount]);
  } else {
    console.log("All messages sent, closing connection...");
    ws.close(); //Close the connection after final message
  }
});

ws.on('close', () => {
  console.log("Client disconnected from server");
});