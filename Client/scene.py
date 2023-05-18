from stacked_sprite import *
from random import uniform
from entity import Entity
import json
import socketio

P = 'player'
K = 'kitty'  # entity
A, B, C, D, E, F, G, H = 'van', 'tank', 'blue_tree', 'car', 'grass', 'crate', 'cup', 'pancake'
S = 'sphere' # transform object

MAP = [
    [0, E, 0, E, B, 0, E, 0, 0, E, 0, E, 0, E,0],
    [E, C, C, C, 0, C, C, 0, E, 0, C, C, C, 0,0],
    [0, C, 0, 0, 0, 0, E, C, 0, C, 0, H, K, C,C],
    [C, 0, 0, E, C, 0, 0, C, C, 0, 0, 0, 0, C,C],
    [C, E, 0, 0, P, E, 0, E, 0, 0, F, E, 0, C,C],
    [C, 0, 0, A, E, D, E, S, 0, F, 0, 0, C, 0,C],
    [0, C, E, 0, 0, 0, E, 0, E, 0, 0, B, C, E,C],
    [0, C, C, 0, E, 0, C, C, 0, G, E, C, 0, 0,C],
    [E, 0, 0, C, C, C, C, 0, C, C, C, 0, E, 0,C],
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2

sio = socketio.Client()
sio.connect('https://mmorpgserver.onrender.com/')
print('my sid is', sio.sid)
app.player.id=sio.sid
print('app.player.id', app.player.id)
sio.emit('player joining', json.dumps({"id":app.player.id}))

@sio.on('getState')
def on_getting_state():
        print("getting state",app.player.offset,app.player.angle)
        playerdata = {
            "offsetx": app.player.offset[0],
            "offsety": app.player.offset[1],
            "angle": app.player.angle,
            "id":app.player.id
                }
        sio.emit('returning state', json.dumps(playerdata))
@sio.on('updateState')
def on_update_state(data):
        tempplayers=json.loads(data)
        for pl in app.players:
            del pl
        app.players=[]
        for player in tempplayers:
            print(player['id'],app.player.id,"ids")
            if player['id']==app.player.id:
                continue
            newplayer=AnotherPlayer(app)
            newplayer.offset=vec2(player['x'],player['y'])
            newplayer.angle=player['angle']
            print(newplayer)
            app.players.append(newplayer)
            print(app.players,"app.players")


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.load_scene()

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name == 'kitty':
                    print(pos,"pos")
                    Entity(self.app, name=name, pos=pos)
                elif name == 'blue_tree':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'grass':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(),
                                  collision=False)
                elif name == 'sphere':
                    obj = StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                    self.transform_objects.append(obj)
                elif name:
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())

    def get_closest_object_to_player(self):
        closest = sorted(self.app.transparent_objects, key=lambda e: e.dist_to_player)
        closest[0].alpha_trigger = True
        closest[1].alpha_trigger = True

    def transform(self):
        for obj in self.transform_objects:
            obj.rot = 30 * self.app.time

    def update(self):
        self.get_closest_object_to_player()
        self.transform()
