import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Car(Widget):
    'Define sensors for density of sand around the car'

    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):

        app = App.get_running_app()

        # update car position
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation

        # update position of sensors
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle+30)%360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30)%360) + self.pos

        # get signal value for each sensor
        self.signal1 = int(np.sum(app.sand[int(self.sensor1_x)-10:int(self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        self.signal2 = int(np.sum(app.sand[int(self.sensor2_x)-10:int(self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(app.sand[int(self.sensor3_x)-10:int(self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.

        # if sensor position is reaching bounds of map, put signal to 1 == full sand
        # this is to penalize getting outside of map
        def is_out_of_bounds(x, y):
            if x>app.longueur-10 or x<10 or y>app.largeur-10 or y<10:
                return 1

        if is_out_of_bounds(self.sensor1_x, self.sensor1_y):
            self.signal1 = 1.
        if is_out_of_bounds(self.sensor2_x, self.sensor2_y):
            self.signal2 = 1.
        if is_out_of_bounds(self.sensor3_x, self.sensor3_y):
            self.signal3 = 1.


class Ball1(Widget):
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass
