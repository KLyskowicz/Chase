import random
import math
import json
import csv
import os
import logging

logger = logging.getLogger(__name__)

class Hunting:
    def __init__(self, round_amount = 50, sheep_amount = 15, 
                init_pos_limit = 10.0, sheep_move_dist = 0.5, 
                wolf_move_dist = 1.0, dir = os.getcwd(),
                wait = False):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        self.round_amount = round_amount
        self.sheep_amount = sheep_amount
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.round_no = 0
        logger.info('Round number: 0')
        self.wolf_pos = [0.0, 0.0]
        logger.info('Wolf podition: 0.0, 0.0')
        self.sheep_pos = [[random.uniform(-init_pos_limit, init_pos_limit), 
                        random.uniform(-init_pos_limit, init_pos_limit)] for i in range(self.sheep_amount)]
        for i, sheep in enumerate(self.sheep_pos):
            logger.info('Sheep nr ' + str(i) + ' position: ' + str(sheep))
        self.dir = dir
        self.wait = wait

    def sheep_move(self):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        for i, sheep_xy in enumerate(self.sheep_pos):
            if (sheep_xy[0] != None) and (sheep_xy[1] != None):
                direction = random.choice(['E', 'W', 'S', 'N'])
                pos = str(self.sheep_pos[i])
                if direction == 'E':
                    self.sheep_pos[i][0] += self.sheep_move_dist
                elif direction == 'W':
                    self.sheep_pos[i][0] -= self.sheep_move_dist
                elif direction == 'N':
                    self.sheep_pos[i][1] += self.sheep_move_dist
                elif direction == 'S':
                    self.sheep_pos[i][1] -= self.sheep_move_dist
                logger.info('Sheep moving from: ' + pos + ' to: ' + str(self.sheep_pos[i]))

    def get_sheep_distance(self, i):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        return math.sqrt((self.sheep_pos[i][0] - self.wolf_pos[0]) ** 2 
                        + (self.sheep_pos[i][1] - self.wolf_pos[1]) ** 2)

    def get_wolf_nearest_sheep(self):
        nearest_nr = -1
        nearest_distance = 0.0
        for i, sheep_xy in enumerate(self.sheep_pos):
            if ((sheep_xy[0] != None) and 
                    ((self.get_sheep_distance(i) < nearest_distance) or (nearest_nr == -1))):
                nearest_distance = self.get_sheep_distance(i)
                nearest_nr = i
        logger.debug(__name__ + ' - Arg:' + str(locals()) + ' Res:' + str(nearest_nr))
        return nearest_nr

    def eat_sheep(self, nearest_sheep):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        self.sheep_pos[nearest_sheep] = [None, None]
        self.sheep_amount -= 1
        logger.info('!!!Sheep nr ' + str(nearest_sheep) + ' was eaten!!! '
                    + str(self.sheep_amount) + ' sheeps remained')

    def wolf_move(self, nearest_sheep):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        pos = str(self.wolf_pos)
        x_diff = self.wolf_pos[0] - self.sheep_pos[nearest_sheep][0]
        y_diff = self.wolf_pos[1] - self.sheep_pos[nearest_sheep][1]
        factor = math.sqrt(x_diff**2 + y_diff**2)
        self.wolf_pos[0] -= x_diff/factor
        self.wolf_pos[1] -= y_diff/factor 
        logger.info('Wolf moving from: ' + pos + ' to: ' + str(self.wolf_pos))

    def print_terminal(self):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        print('----------------tura: ' + str(self.round_no)
            + '\npozycja wilka: (' + str(round(self.wolf_pos[0], 3))
            + ' ,' + str(round(self.wolf_pos[1], 3))
            + ')\nzywe owce: ' + str(self.sheep_amount))

    def begin_hunting_terminal(self):
        logger.debug(__name__ + ' - Arg:' + str(locals()))
        pos_json = open(os.path.join(self.dir, 'pos.json'), encoding='utf-8', mode="a")
        alive_csv = open(os.path.join(self.dir,'alive.csv'), mode='a', newline='')
        csv_writer = csv.writer(alive_csv)
        while (self.round_no < self.round_amount) and (self.sheep_amount!=0):
            self.print_terminal()
            d = {'round_no':self.round_no, 'wolf_pos':self.wolf_pos, 'sheep_pos':self.sheep_pos}
            json.dump(d, pos_json, indent=4)
            csv_writer.writerow([str(self.round_no), str(self.sheep_amount)])
            self.round_no += 1
            logger.info(str(self.round_no) + ' round begin')
            self.sheep_move()
            nearest_sheep = self.get_wolf_nearest_sheep()
            if self.get_sheep_distance(nearest_sheep) < self.wolf_move_dist:
                self.eat_sheep(nearest_sheep)
                print('!!! OWCA ' + str(nearest_sheep) + ' ZOSTALA ZJEDZONA !!!')
            else:
                self.wolf_move(nearest_sheep)
            if (self.wait):
                print('Runda ' + str(self.round_no) + ' zakonczona, wcisnij dowolny klawisz aby przejsc dalej')
                input()
        self.print_terminal()
        logger.info('Hunting ended ' + str(self.sheep_amount) + ' sheeps remained alive')
        d = {'round_no':self.round_no, 'wolf_pos':self.wolf_pos, 'sheep_pos':self.sheep_pos}
        json.dump(d, pos_json, indent=4)
        csv_writer.writerow([str(self.round_no),  str(self.sheep_amount)])
        alive_csv.close()
        pos_json.close()