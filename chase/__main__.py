import argparse
import configparser
import errno
import os
import logging

from .hunting import Hunting

min_round_amount = 5
min_wolf_move = 0.1
min_sheep_move = 0.1
min_init_pos_limit = 1
min_sheep_amount = 2

def agrparse_create(customization):
    parser = argparse.ArgumentParser(description='Hunting symulation')
    parser.add_argument('-c', '--config', metavar='FILE', 
                        help='additional config file',
                        type=str)
    parser.add_argument('-d', '--dir', metavar='DIR',
                        help='''subdirectory for
                        files pos.json, alive.csv and chase.log''',
                        type=str)
    parser.add_argument('-l', '--log', metavar='LEVEL',
                        help='''store chosen level of event in event collector:
                        DEBUG, INFO, WARNING, ERROR, CRITICAL''',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-r', '--rounds', metavar='NUM',
                        help='rounds amount', type=int)
    parser.add_argument('-s', '--sheep', metavar='NUM',
                        help='sheep amount', type=int)
    parser.add_argument('-w', '--wait', action='store_true',
                        help='''wait for key press after every round''')

    args = parser.parse_args()

    if (args.dir):
        customization['dir'] = os.path.join(os.getcwd(), args.dir)
        if (os.path.isdir(args.dir)==False):
            os.mkdir(args.dir)

    if (args.log):
        fName = ''
        if (args.dir):
            fName = os.path.join(os.getcwd(), args.dir, 'chase.log')
        else:
            fName = os.path.join(os.getcwd(), 'chase.log')
        logging.basicConfig(filename=fName, level=args.log,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    if (args.config):
        config_file = configparser.ConfigParser()
        config_file.read(args.config)
        if (len(config_file) > 1):
            try:
                float(config_file['Movement']['sheepmovedist'])
                float(config_file['Movement']['wolfmovedist'])
                float(config_file['Terrain']['initpostlimit'])
            except ValueError:
                logging.error('ValueError exception thrown: given variable from config file is not a number, default was set')
                raise ValueError('ValueError exception thrown: given variable from config file is not a number, default was set')
            if (float(config_file['Movement']['sheepmovedist']) < min_sheep_move):
                logging.error('ValueError exception thrown: sheep_move_distance smaller than ' + str(min_sheep_move) + ', default was set')
                raise ValueError('ValueError exception thrown: sheep_move_distance smaller than ' + str(min_sheep_move) + ', default was set')
            elif(float(config_file['Movement']['wolfmovedist']) < min_wolf_move):
                logging.error('ValueError exception thrown: wolf_move_distance smaller than ' + str(min_wolf_move) + ', default was set')
                raise ValueError('ValueError exception thrown: wolf_move_distance smaller than ' + str(min_wolf_move) + ', default was set')
            elif (float(config_file['Terrain']['initpostlimit']) < min_init_pos_limit):
                logging.error('ValueError exception thrown: init_pos_limit smaller than ' + str(min_init_pos_limit) + ', default was set')
                raise ValueError('ValueError exception thrown: init_pos_limit smaller than ' + str(min_init_pos_limit) + ', default was set')
            else:
                customization['sheep_move_dist'] = float(config_file['Movement']['sheepmovedist'])
                customization['wolf_move_dist'] = float(config_file['Movement']['wolfmovedist'])
                customization['init_pos_limit'] = float(config_file['Terrain']['initpostlimit'])  
        else:
            logging.error('File ' + str(args.config) + ' not found')
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), args.config)

    if (args.rounds):
        if (args.rounds < min_round_amount):
            logging.error('Given round_amount smaller than ' + str(min_round_amount))
            raise ValueError('Given round_amount smaller than ' + str(min_round_amount))
        else:
            customization['round_amount'] = args.rounds

    if (args.sheep):
        if (args.sheep < min_sheep_amount):
            logging.error('Given sheep_amount smaller than ' + str(min_sheep_amount))
            raise ValueError('Given sheep_amount smaller than ' + str(min_sheep_amount))
        else:
            customization['sheep_amount'] = args.sheep

    if (args.wait):
        customization['wait'] = True



customization = {'round_amount': 50, 'sheep_amount': 15,
                'init_pos_limit': 10.0, 'sheep_move_dist': 0.5, 
                'wolf_move_dist': 1.0, 'dir': os.getcwd(), 'wait': False}

if __name__ == '__main__':
    agrparse_create(customization)

h = Hunting(round_amount=customization['round_amount'],
            sheep_amount=customization['sheep_amount'],
            init_pos_limit=customization['init_pos_limit'],
            sheep_move_dist=customization['sheep_move_dist'],
            wolf_move_dist=customization['wolf_move_dist'],
            dir=customization['dir'],
            wait=customization['wait'])
h.begin_hunting_terminal()