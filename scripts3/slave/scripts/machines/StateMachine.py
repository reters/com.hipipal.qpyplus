#! -*- coding=utf-8 -*-
import time
import random


class Machine(object):
    def __init__(self, start_state):
        self.start_state = start_state
        self.running = False
        self.current_state = self.start_state

    def run(self):
        self.current_state = self.start_state
        self.running = True
        while self.running:
            print(("in %s " % self.current_state))
            self.current_state = self.current_state()

    def exit(self):
        self.running = False
        print("going to Exit")
        return self.start_state  # 退回初始的状态


class WeatherMachine(Machine):
    def __init__(self):
        super(WeatherMachine, self).__init__(self.sunny)
        self.m = BadWeatherMachine()

    def sunny(self):
        print("is sunday now")
        time.sleep(1)

        r = random.random()
        if r < 0.2:
            return self.rainy
        elif r < 0.6:
            return self.cloudy
        elif r > 0.99:
            return self.exit
        else:
            return self.sunny

    def rainy(self):
        def _bad_weather():
            self.m.run()
            return self.sunny

        print("is Rainy now")
        time.sleep(1)

        r = random.random()
        if r < 0.3:
            return self.rainy
        elif r < 0.8:
            return self.cloudy
        elif r < 0.9:
            print("baddd day")
            return _bad_weather
        else:
            return self.sunny

    def cloudy(self):
        print("is Cloudy now")
        time.sleep(1)

        r = random.random()
        if r < 0.2:
            return self.rainy
        elif r < 0.5:
            return self.cloudy
        else:
            return self.sunny

    def exit(self):
        self.running = False
        return None


class BadWeatherMachine(Machine):
    def __init__(self):
        super(BadWeatherMachine, self).__init__(self.cloudy)

    def cloudy(self):
        print("is Cloudy now")
        time.sleep(1)

        r = random.random()
        if r < 0.2:
            return self.thunder
        elif r < 0.5:
            return self.cloudy
        elif r < 0.7:
            return self.storm
        else:
            print("Thank God Bad Weather Gone")
            self.running = False
            return None

    def thunder(self):
        print("is Thunder now")
        time.sleep(1)

        r = random.random()
        if r < 0.2:
            return self.storm
        elif r < 0.5:
            return self.cloudy
        else:
            return self.thunder

    def storm(self):
        print("is Strom now")
        time.sleep(1)

        r = random.random()
        if r < 0.2:
            return self.storm
        elif r < 0.5:
            return self.cloudy
        else:
            return self.thunder


if __name__ == "__main__":
    print("hehe")
    # m = BadWeatherMachine()
    m = WeatherMachine()
    m.run()
