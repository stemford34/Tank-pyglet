import pyglet

from pyglet.window import key
from pyglet.sprite import Sprite

from GameObjects import *


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0

        player_image = pyglet.image.load('res/sprites/tanks.png')
        player_spr = pyglet.sprite.Sprite(player_image)
        self.player = PlayerObject(400, 400, player_spr, 0.1)

        self.bullet_image = pyglet.image.load('res/sprites/bullet.png')
        self.bullet_list = []

        brick_image = pyglet.image.load('res/sprites/brick.png')
        brick_spr = pyglet.sprite.Sprite(brick_image)
        self.brick = BrickObject(500, 500, brick_spr, scale=0.25)

    def on_key_press(self, symbol, midifiers):
        if symbol == key.SPACE:
            if self.player.up_rotation:
                self.bullet_list.append(BulletObject(self.player.posx, self.player.posy, Sprite(self.bullet_image), scale=0.1, rotation='up'))
            elif self.player.right_rotation:
                self.bullet_list.append(BulletObject(self.player.posx, self.player.posy, Sprite(self.bullet_image), scale=0.1, rotation='right'))
            elif self.player.left_rotation:
                self.bullet_list.append(BulletObject(self.player.posx, self.player.posy, Sprite(self.bullet_image), scale=0.1, rotation='left'))
            elif self.player.down_rotation:
                self.bullet_list.append(BulletObject(self.player.posx, self.player.posy, Sprite(self.bullet_image), scale=0.1, rotation='down'))
            
        if not self.player.rotation(symbol):
            self.player.move(symbol)
    
    def on_draw(self):
        self.clear()
        self.player.draw()
        # self.bullet.draw()
        for bullet in self.bullet_list:
            bullet.draw()
        self.brick.draw()

    def update_player_bullet(self, dt):
        for bullet in self.bullet_list:
            bullet.update(dt)
            bullet.move(dt)

    def update(self, dt):
        self.update_player_bullet(dt)
        pass


if __name__ == '__main__':
    window = GameWindow(1200, 900, 'Tanks', resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()     # 170 x 201
