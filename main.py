from ursina import *
from ursina import curve
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(borderless=False)

window.title = "Grapvle"
window.fps_counter.disable()

window.exit_button = True


player = FirstPersonController(
    position=(50, 10, 40), model='cube', color=color.orange)


class Grapple(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            model='models/grapple.obj',
            texture="white_cube",
            collider='box',
            position=position
        )
        self.player = player

    def update(self):
        self.on_click = Func(self.player.animate_position,
                             self.position, duration=1, curve=curve.linear)

        ray = raycast(self.player.position, self.player.forward,
                      distance=0.5,  ignore=[player, ])

        if ray.entity == self:
            self.player.y += 2


class Wall(Entity):
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.gray,
            texture="grappler_texture.png",
            collider='box',
            position=position,
            scale=scale,
        )


class NormalBlock(Entity):
    def __init__(self, position=(0, 0, 0), scale=(5, 2, 5)):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.lime,
            collider='box',
            position=position,
            scale=scale,
        )


class Maze(Entity):
    def __init__(self, position=(0, 0, 0), scale=(50, 50, 50)):
        super().__init__(
            parent=scene,
            model='models/maze.obj',
            color=color.lime,
            collider='mesh',
            position=position,
            scale=scale
        )


class Level(NormalBlock):
    Wall((10, 10, 50), (120, 100, 10))
    Wall((10, 10, -50), (120, 100, 10))
    Wall((-57, 10, 50), (10, 100, 50))
    Wall((-57, 10, -50), (10, 100, 50))
    Wall((57, -10, 50), (10, 140, 200))
    Maze((0, 5, 0))
    # NormalBlock((10, 5, 5))


ground = Entity(model='cube', color=color.red,
                texture="white_cube", collider='box', scale=(120, 10, 100))


Grapple((5, 10, 0))
Grapple((0, 20, 5))
Grapple((10, 30, 5))
Grapple((-50, 30, 5))

Sky()

Level()
PointLight(parent=camera, color=color.white, position=(0, 10, -1.5))
AmbientLight(color=color.rgba(100, 100, 100, 0.1))


app.run()
