import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        app = App.get_running_app()
        with self.canvas:
            Color(0.8,0.7,0)
            touch.ud['line'] = Line(points = (touch.x, touch.y), width = 10)
            app.last_x = int(touch.x)
            app.last_y = int(touch.y)
            app.n_points = 0
            app.length = 0
            app.sand[int(touch.x),int(touch.y)] = 1

    def on_touch_move(self, touch):
        app = App.get_running_app()
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            app.length += np.sqrt(max((x - app.last_x)**2 + (y - app.last_y)**2, 2))
            app.n_points += 1.
            density = app.n_points/(app.length)
            touch.ud['line'].width = int(20 * density + 1)
            app.sand[int(touch.x) - 10 : int(touch.x) + 10, int(touch.y) - 10 : int(touch.y) + 10] = 1
            app.last_x = x
            app.last_y = y
