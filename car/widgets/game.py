import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.vector import Vector

from widgets.car import Car, Ball1, Ball2, Ball3


class Game(Widget):

    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)


    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update(self, dt):
        app = App.get_running_app()

        if app.first_update:
            app.longueur = self.width
            app.largeur = self.height
            app.sand = np.zeros((app.longueur,app.largeur))
            app.goal_x = 20
            app.goal_y = app.largeur - 20
            app.first_update = False

        xx = app.goal_x - self.car.x
        yy = app.goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx,yy))/180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]
        action = app.brain.update(app.last_reward, last_signal)
        app.scores.append(app.brain.score())
        rotation = app.action2rotation[action]
        self.car.move(rotation)
        distance = np.sqrt((self.car.x - app.goal_x)**2 + (self.car.y - app.goal_y)**2)
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

        if app.sand[int(self.car.x),int(self.car.y)] > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            app.last_reward = -1
        else: # otherwise
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            app.last_reward = -0.2
            if distance < app.last_distance:
                app.last_reward = 0.1

        if self.car.x < 10:
            self.car.x = 10
            app.last_reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            app.last_reward = -1
        if self.car.y < 10:
            self.car.y = 10
            app.last_reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            app.last_reward = -1

        if distance < 100:
            app.goal_x = self.width-app.goal_x
            app.goal_y = self.height-app.goal_y

        app.last_distance = distance
