import pyglet

from pyglet.window import key
from pyglet.sprite import Sprite
from pyglet.text import Label

from GameObjects import *
from Map.level1 import *


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0

        area_image = preload_image('area.png')
        self.area_spr = Sprite(area_image, x=190, y=190)

        player_image = preload_image('tanks.png')
        self.player = PlayerObject(200, 200, Sprite(player_image), 0.1)

        self.enemy_image = preload_image('enemy.png')
        self.enemy_list = []
        self.enemy_list.append(PlayerObject(320, 320, Sprite(self.enemy_image), 0.1))

        self.bullet_image = preload_image('bullet.png')
        self.bullet_list = []

        brick_image = preload_image('brick.png')
        brick_spr = pyglet.sprite.Sprite(brick_image)
        self.brick_list = []
        for i in range(0, 13):
            for j in range(0, 13):
                if mapConfiguration[i][j] == 1:
                    posx = 200 + j*40
                    posy = 680 - i*40
                    self.brick_list.append(BrickObject(posx, posy, Sprite(brick_image), scale=0.2))

        self.brick_destroyed_label = Label('Brick destroyed', x=1000, y=850)
        self.brick_destroyed_label.italic = True
        self.brick_destroyed_label.bold = True

        self.brick_destroyed_number_label = Label('0', x=1000, y=750)
        self.brick_destroyed_number_label.italic = True
        self.brick_destroyed_number_label.bold = True

        self.brick_destroyed_number = 0

        self.enemy_destroyed_label = Label('Enemy destroyed', x = 1000, y=650)
        self.enemy_destroyed_label.italic = True
        self.enemy_destroyed_label.bold = True

        self.enemy_destroyed_number_label = Label('0', x=1000, y=550)
        self.enemy_destroyed_number_label.italic = True
        self.enemy_destroyed_number_label.bold = True

        self.enemy_destroyed_number = 0

    def player_move_to(self, posx, posy):
        for brick in self.brick_list:
            if posx == brick.posx_center and posy == brick.posy_center:
                return False
        for enemy in self.enemy_list:
            if posx == enemy.posx_center and posy == enemy.posy_center:
                return False
        return True

    def player_move(self, symbol):
        if symbol == key.LEFT and self.player.sprite.x > 200 + 40 \
                and self.player_move_to(self.player.posx_center-40.0, self.player.posy_center):
            self.player.sprite.x -= 40
            self.player.posx_center -= 40
        if symbol == key.RIGHT and self.player.sprite.x < 720 - 40 \
                and self.player_move_to(self.player.posx_center+40.0, self.player.posy_center):
            self.player.sprite.x += 40
            self.player.posx_center += 40
        if symbol == key.UP and self.player.sprite.y < 720 - 40 \
                and self.player_move_to(self.player.posx_center, self.player.posy_center+40.0):
            self.player.sprite.y += 40
            self.player.posy_center += 40
        if symbol == key.DOWN and self.player.sprite.y > 200 + 40 \
                and self.player_move_to(self.player.posx_center, self.player.posy_center-40.0):
            self.player.sprite.y -= 40
            self.player.posy_center -= 40
        
        self.player.posx = self.player.sprite.x
        self.player.posy = self.player.sprite.y

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
            self.player_move(symbol)
    
    def on_draw(self):
        self.clear()
        self.area_spr.draw()
        self.player.draw()
        for enemy in self.enemy_list:
            enemy.draw()
        for bullet in self.bullet_list:
            bullet.draw()
        for brick in self.brick_list:
            brick.draw()

        self.brick_destroyed_label.draw()
        self.brick_destroyed_number_label.draw()

        self.enemy_destroyed_label.draw()
        self.enemy_destroyed_number_label.draw()


    def update_player(self, dt):
        self.player.update()
        
    def update_player_bullet(self, dt):
        for bullet in self.bullet_list:
            bullet.update(dt)
            bullet.move(dt)
            for brick in self.brick_list:
                if bullet.check_collision(brick):
                    self.bullet_list.remove(bullet)
                    self.brick_list.remove(brick)
                    self.brick_destroyed_number += 1
                    self.brick_destroyed_number_label.text = str(self.brick_destroyed_number)
            for enemy in self.enemy_list:
                if bullet.check_collision(enemy):
                    self.enemy_list.remove(enemy)
                    self.bullet_list.remove(bullet)
                    self.enemy_destroyed_number += 1
                    self.enemy_destroyed_number_label.text = str(self.enemy_destroyed_number)

    def update(self, dt):
        self.update_player_bullet(dt)
        pass


if __name__ == '__main__':
    window = GameWindow(1200, 900, 'Tanks', resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()     # 170 x 201
