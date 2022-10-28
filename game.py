import websockets
from rng import new_generator

pid_c = 0
tokegen = new_generator(128)
class Player:
    def __init__(self, name: str):
        global pid_c
        self.name = name
        self.id = pid_c
        self.token = tokegen()
        pid_c += 1
        print(f'new player {self.id} "{self.name}" token {self.token[:16]}...')

class Game:
    def __init__(self, id: str, host: Player):
        self.id = id
        self.host = host
        

    def add_user(self, name: str, sock):
        if name in self.sockets.keys():
            raise KeyError("player already in game")
    
            