import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.clock import Clock

from ai import Dqn
from widgets import Game, MyPaintWidget

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class CarApp(App):

    sand = None
    goal_x = None
    goal_y = None
    longueur = None
    largeur = None
    brain = Dqn(input_size=5, nb_action=3, gamma=0.9)
    last_distance = 0
    last_x = 0
    last_y = 0
    n_points = 0
    length = 0
    action2rotation = [0,20,-20]
    last_reward = 0
    scores = []
    first_update = True  # init to true


    def build(self):
        parent = Game()
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0/60.0)
        self.painter = MyPaintWidget()
        clearbtn = Button(text = 'clear')
        savebtn = Button(text = 'save', pos = (parent.width, 0))
        loadbtn = Button(text = 'load', pos = (2 * parent.width, 0))
        clearbtn.bind(on_release = self.clear_canvas)
        savebtn.bind(on_release = self.save)
        loadbtn.bind(on_release = self.load)
        parent.add_widget(savebtn)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(loadbtn)
        return parent


    def clear_canvas(self, obj):
        app = App.get_running_app()
        self.painter.canvas.clear()
        app.sand = np.zeros((app.longueur, app.largeur))


    def save(self, obj):
        app = App.get_running_app()
        print("saving brain...")
        app.brain.save()
        plt.plot(app.scores)
        plt.show()


    def load(self, obj):
        app = App.get_running_app()
        print("loading last saved brain...")
        app.brain.load()


if __name__ == '__main__':
    CarApp().run()
