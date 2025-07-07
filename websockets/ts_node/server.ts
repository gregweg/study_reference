// server.ts
import { WebSocketServer } from 'ws';

console.log("Starting WebSocket server...");

const wss = new WebSocketServer({ port: 8080 });

console.log("WebSocket server listening on ws://localhost:8080");

wss.on('connection', (ws) => {
  console.log("Client connected");

  ws.on('message', (message) => {
    console.log("Received:", message.toString());
    ws.send(`Echo: ${message}`);
  });
  
  wss.on('error', (err) => {
    console.error("WebSocket server error:", err);
  });

  ws.on('close', () => {
    console.log("Client disconnected");
  });
});