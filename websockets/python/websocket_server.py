import asyncio
import websockets

PING_INTERVAL = 10  # seconds
PING_TIMEOUT = 5

async def echo(websocket):
    async def ping():
        while True:
            try:
                await websocket.ping()
                await asyncio.sleep(PING_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Ping failed: {e}")
                await websocket.close()
                break

    ping_task = asyncio.create_task(ping())

    try:
        async for message in websocket:
            print(f"Server received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e.code} - {e.reason}")
    finally:
        ping_task.cancel()
        await ping_task

async def main():
    async with websockets.serve(echo, "localhost", 8765, ping_interval=None):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())