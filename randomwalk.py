# A simple 2D random walker
# Originally created for Tampere University of Technology course FYS-1350 Nanophysics
# Copyright Mika "AgenttiX" Mäki, 2016


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np
import random

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui


class Random:
    def __init__(self):
        self.__iter = 1000000

        self.__size = 5000

        self.__xstart = self.__size / 2
        self.__ystart = self.__size / 2
        self.__x = self.__xstart
        self.__y = self.__ystart

        self.__mat = np.zeros([self.__size, self.__size])
        self.__dist = np.zeros(self.__iter)

        self.move()

        app = pg.mkQApp()

        pg.setConfigOptions(antialias=True)

        win = QtGui.QMainWindow()
        win.resize(1200, 700)
        self.imv = pg.ImageView()
        win.setCentralWidget(self.imv)
        win.setWindowTitle("Particle path")

        win2 = pg.GraphicsWindow(title="Particle distance")
        plot = win2.addPlot(y=self.__dist)

        win.show()

        self.imv.setImage(self.__mat)

        app.exec_()

    def move(self):
        for i in range(0, self.__iter):
            dir = random.randint(0,3)
            if dir == 0:
                self.__x += 1
            elif dir == 1:
                self.__x -= 1
            elif dir == 2:
                self.__y += 1
            elif dir == 3:
                self.__y -= 1

            if self.__x == self.__size:
                self.__x = 0
            elif self.__x == -1:
                self.__x = self.__size-1
            elif self.__y == self.__size:
                self.__y = 0
            elif self.__y == -1:
                self.__y = self.__size-1

            self.__mat[self.__x, self.__y] = i + self.__iter / 10
            self.__dist[i] = np.sqrt((self.__x - self.__xstart)**2 + (self.__y - self.__ystart)**2)


def main():
    Random()

main()
