import asyncio
import websockets

async def talk():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri, ping_interval=None, ping_timeout=None) as websocket:
        messages = ["Hello", "How are you?", "Goodbye"]
        for msg in messages:
            print(f"Client sends: {msg}")
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"Client received: {response}")
        await asyncio.sleep(2)  # wait before closing to see pings

if __name__ == "__main__":
    asyncio.run(talk())