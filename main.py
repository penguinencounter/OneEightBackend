import asyncio
import websockets
import json
import game
from rng import new_generator

games = {}

gen_code = new_generator(10)


# action
#  new_game (name)
#
def require_has(a: dict, b: str):
    if not b in a.keys(): raise KeyError(f"Bad input: key required: {b}")


def parse(inp: dict):
    print(f'parse {inp}')
    if (type(inp) != dict):
        raise KeyError(f"Bad input: wrong type {type(inp)}, expected {dict}")
    require_has(inp, "action")
    if inp["action"] == "new_game":
        require_has(inp, "name")
        game_id = gen_code(games.keys())
        uname = inp["name"]
        player = game.Player(uname)
        games[game_id] = game.Game(game_id, player)
        print(f'{uname} created a new game: {game_id}')
        return {"game_id": game_id, "token": player.token}


VERSION = 1


def get_send_func(websocket):
    c = websocket

    async def ssend(data):
        if type(data) == dict:
            await c.send(json.dumps(data))
        else:
            await c.send(str(data))

    return ssend


async def echo(websocket):
    send = get_send_func(websocket)
    await send({"type": "hello", "version": VERSION})
    async for message in websocket:
        try:
            payload = json.loads(message)
            await send(parse(payload))
        except json.decoder.JSONDecodeError:
            await send("err: Failed to parse")
        except KeyError as e:
            await send(f"err: {e}")


async def main():
    async with websockets.serve(echo, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever


asyncio.run(main())
