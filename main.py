from loguru import logger as ll
from pacboom import Pacboom


if __name__ == '__main__':
    ll.info('start')
    acc = Pacboom(private_key='YOUR PRIVATE KEY')
    acc.pacboom()



