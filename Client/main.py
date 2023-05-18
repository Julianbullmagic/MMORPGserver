import sys
from settings import *
from cache import Cache
from player import Player
from anotherplayer import AnotherPlayer
from scene import Scene
import json
import sys
import socketio
from entity import Entity
from entity import AnotherPlayerEntity

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES,pg.RESIZABLE)
        pg.display.set_caption('MMORPG')
        self.clock = pg.time.Clock()
        self.time = 0
        self.players = []
        self.playernames = []
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        # groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.transparent_objects = []
        # game objects
        self.cache = Cache()
        self.player = Player(self)
        self.scene = Scene(self)


    def update(self):
        self.scene.update()
        self.main_group.update()
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.main_group.draw(self.screen)
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.KEYDOWN:
                self.player.single_fire(event=e)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.check_events()
            self.get_time()
            self.update()
            self.draw()

app = App()

sio = socketio.Client()
sio.connect('https://mmorpgserver.onrender.com/')
print('my sid is', sio.sid)
app.player.id=sys.argv[1]
print('app.player.id', app.player.id)
sio.emit('player joining', json.dumps({"name":sys.argv[1]}))

@sio.on('getState')
def on_getting_state():
        # print("getting state",app.player.offset,app.player.angle)
        playerdata = {
            "offsetx": app.player.offset[0],
            "offsety": app.player.offset[1],
            "angle": app.player.angle,
            "id":app.player.id
                }
        sio.emit('returning state', json.dumps(playerdata))
@sio.on('updateState')
def on_update_state(data):
        print("updating state")
        tempplayers=json.loads(data)
        print(tempplayers,"temp players")
        print(app.players)
        for player in tempplayers:
            if player['id']==app.player.id:
                continue
            if player['id'] not in app.playernames:
                app.playernames.append(player['id'])
                pos = vec2(player['x'],player['y'])
                newplayer=AnotherPlayerEntity(app, name='kitty', pos=pos, playername=player['id'])
                app.players.append(newplayer)
            for play in app.players:
                if play.playername==player['id']:
                    # play.lastpos=play.pos
                    play.pos=vec2(player['x'],player['y'])
                    print(play.pos[0],play.pos[1],"pos")
                    # play.incrementx=play.lastpos[0]-play.pos[0]
                    # play.incrementx=play.incrementx/20
                    # play.incrementy=play.lastpos[1]-play.pos[1]
                    # play.incrementy=play.incrementy/20
                    play.angle=player['angle']
app.run()
