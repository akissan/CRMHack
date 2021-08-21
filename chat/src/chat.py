from falcon.errors import WebSocketDisconnected
import falcon
import collections
import asyncio


class ChatList:

    def __init__(self):
        # TODO initialize the chat lists with repository of the chats
        pass

    async def on_get(self, req, resp):
        # get the list of the chats
        pass

    async def on_websocket(self, ws):
        # create connection to push all the chats created
        pass


class Chat:

    async def on_get(self, req, resp, account):
        # get all the messages
        pass

    async def on_post(self, req, resp, account):
        # add message to the chat (used to add from the bitrix API)
        pass

    async def on_websocket(self, ws, account):

        try:
            await ws.accept(subprotocol='wamp')
        except WebSocketDisconnected:
            return

        messages = collections.deque()

        async def sink():
            while True:
                try:
                    message = await ws.receive_text()
                except falcon.WebSocketDisconnected:
                    break

                messages.append(message)

        sink_task = falcon.create_task(sink())

        while not sink_task.done():
            while ws.ready and not messages and not sink_task.done():
                await asyncio.sleep(0)

            try:
                # await ws.send_text(messages.popleft())
                # TODO send messages
                pass
            except falcon.WebSocketDisconnected:
                break

        sink_task.cancel()
        try:
            await sink_task
        except asyncio.CancelledError:
            pass
