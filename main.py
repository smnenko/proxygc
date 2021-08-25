import time

from proxy import config
from proxy.manager import ProxyManager


if __name__ == '__main__':
    print(config.Color.FAIL + '''
    ██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
    █░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░██░░░░░░░░█░░░░░░░░██░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█
    █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
    █░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░█░░░░▄▀░░██░░▄▀░░░░█░░░░▄▀░░██░░▄▀░░░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░░░█
    █░░▄▀░░██░░▄▀░░█░░▄▀░░████░░▄▀░░███░░▄▀░░██░░▄▀░░███░░▄▀▄▀░░▄▀▄▀░░█████░░▄▀▄▀░░▄▀▄▀░░███░░▄▀░░█████████░░▄▀░░█████████
    █░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░██░░▄▀░░███░░░░▄▀▄▀▄▀░░░░█████░░░░▄▀▄▀▄▀░░░░███░░▄▀░░█████████░░▄▀░░█████████
    █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀░░██░░▄▀░░█████░░▄▀▄▀▄▀░░█████████░░░░▄▀░░░░█████░░▄▀░░██░░░░░░█░░▄▀░░█████████
    █░░▄▀░░░░░░░░░░█░░▄▀░░░░░░▄▀░░░░███░░▄▀░░██░░▄▀░░███░░░░▄▀▄▀▄▀░░░░█████████░░▄▀░░███████░░▄▀░░██░░▄▀░░█░░▄▀░░█████████
    █░░▄▀░░█████████░░▄▀░░██░░▄▀░░█████░░▄▀░░██░░▄▀░░███░░▄▀▄▀░░▄▀▄▀░░█████████░░▄▀░░███████░░▄▀░░██░░▄▀░░█░░▄▀░░█████████
    █░░▄▀░░█████████░░▄▀░░██░░▄▀░░░░░░█░░▄▀░░░░░░▄▀░░█░░░░▄▀░░██░░▄▀░░░░███████░░▄▀░░███████░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░░░█
    █░░▄▀░░█████████░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░███████░░▄▀░░███████░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
    █░░░░░░█████████░░░░░░██░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░██░░░░░░░░███████░░░░░░███████░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█
    ██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
                                        https://github.com/smnenko/proxygc
            ''' + config.Color.ENDC)
    manager = ProxyManager()
    print('Available options:')
    manager.available_options()
    manager.set_choice(input('\nEnter what you would like to do: '))
    tic = time.perf_counter()
    manager.run()
    toc = time.perf_counter()
    print(f'\nProgram finished by {toc - tic:0.4f} seconds')
