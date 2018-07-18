import pyglet

from pyglet.window import key

def preload_image(image):
    img = pyglet.image.load('res/sprites/'+image)
    return img


class GameObject:
    def __init__(self, posx, posy, sprite=None):
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.x = self.posx
        self.sprite.y = self.posy


class PlayerObject(GameObject):
    def __init__(self, posx, posy, sprite=None, scale=1.0):
        super().__init__(posx, posy, sprite)
        self.sprite.scale = scale

        self.up_rotation = True
        self.down_rotation = False
        self.right_rotation = False
        self.left_rotation = False

    def change_bool_rotation(self):
        self.up_rotation = False
        self.down_rotation = False
        self.right_rotation = False
        self.left_rotation = False

    def rotation(self, symbol):
        if symbol == key.RIGHT and not self.right_rotation:
            self.sprite.rotation = 90
            self.sprite.x += -40*int(self.left_rotation) - 40*int(self.down_rotation)
            self.sprite.y += 40*int(self.up_rotation) + 40*int(self.left_rotation)
            self.change_bool_rotation()
            self.right_rotation = True

            self.posx = self.sprite.x
            self.posy = self.sprite.y

            return True
        if symbol == key.LEFT and not self.left_rotation:
            self.sprite.rotation = -90
            self.sprite.x += 40*int(self.up_rotation) + 40*int(self.right_rotation)
            self.sprite.y += -40*int(self.right_rotation) - 40*int(self.down_rotation)
            self.change_bool_rotation()
            self.left_rotation = True

            self.posx = self.sprite.x
            self.posy = self.sprite.y

            return True
        if symbol == key.UP and not self.up_rotation:
            self.sprite.rotation = 0
            self.sprite.x += -40*int(self.left_rotation) - 40*int(self.down_rotation)
            self.sprite.y += -40*int(self.right_rotation) - 40*int(self.down_rotation)
            self.change_bool_rotation()
            self.up_rotation = True
            
            self.posx = self.sprite.x
            self.posy = self.sprite.y

            return True
        if symbol == key.DOWN and not self.down_rotation:
            self.sprite.rotation = 180
            self.sprite.x += 40*int(self.up_rotation) + 40*int(self.right_rotation)
            self.sprite.y += 40*int(self.left_rotation) + 40*int(self.up_rotation)
            self.change_bool_rotation()
            self.down_rotation = True
            
            self.posx = self.sprite.x
            self.posy = self.sprite.y

            return True
        
        return False

    def move(self, symbol):
        if symbol == key.LEFT:
            self.sprite.x -= 40
        if symbol == key.RIGHT:
            self.sprite.x += 40
        if symbol == key.UP:
            self.sprite.y += 40
        if symbol == key.DOWN:
            self.sprite.y -= 40
        
        
        self.posx = self.sprite.x
        self.posy = self.sprite.y

    def draw(self):
        super().draw()


class BrickObject(GameObject):
    def __init__(self, posx, posy, sprite=None, scale=1.0):
        super().__init__(posx, posy, sprite)
        self.sprite.scale = scale

    def draw(self):
        super().draw()        

class BulletObject(GameObject):
    def __init__(self, posx, posy, sprite=None, scale=1.0, rotation=None):
        super().__init__(posx, posy, sprite)
        self.sprite.scale = scale

        self.up_rotation = False
        self.down_rotation = False
        self.right_rotation = False
        self.left_rotation = False

        if rotation == 'up':
            self.sprite.x += 20 - self.sprite.width/2
            self.sprite.y += 40

            self.up_rotation = True
        elif rotation == 'right':
            self.sprite.rotation = 90

            self.sprite.x += 40
            self.sprite.y += -20 + self.sprite.width/2

            self.right_rotation = True
        elif rotation == 'left':
            self.sprite.rotation = -90

            self.sprite.x += -40
            self.sprite.y += 20 - self.sprite.width/2

            self.left_rotation = True
        elif rotation == 'down':
            self.sprite.rotation = 180

            self.sprite.x += -20 + self.sprite.width/2
            self.sprite.y += -40

            self.down_rotation = True

        self.posx = self.sprite.x
        self.posy = self.sprite.y
            
    def move(self, dt):
        if self.up_rotation:
            self.posy += 400 * dt
        elif self.down_rotation:
            self.posy -= 400 * dt
        elif self.left_rotation:
            self.posx -= 400 * dt
        elif self.right_rotation:
            self.posx += 400 * dt
        

    def draw(self):
        super().draw()        