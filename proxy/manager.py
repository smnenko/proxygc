from .grabber import ProxyGrabber
from .checker import ProxyChecker

AVAILABLE_OPTIONS = {
    1: {
        'option': 'Grab proxies from our list of sites',
        'class': ProxyGrabber
    },
    2: {
        'option': 'Check proxies for valid',
        'class': ProxyChecker
    }
}


class ProxyManager:

    def __init__(self):
        self.choice = None

    def set_choice(self, choice):
        self.choice = choice

    def run(self):
        if self.choice.isdigit() and int(self.choice) in AVAILABLE_OPTIONS:
            return AVAILABLE_OPTIONS[int(self.choice)]['class'](open('proxy.txt', mode='w', encoding='utf-8')).start()
        raise Exception('Invalid input')

    @classmethod
    def available_options(cls):
        for key, value in AVAILABLE_OPTIONS.items():
            print(f"{key}: {value['option']}")
