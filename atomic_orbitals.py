# A software for computing and rendering atomic orbitals
# (solutions of the Schrödinger equation for atoms with a single electron)
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


import scipy.special
import sympy.physics.hydrogen
import sympy
import numpy as np

# Must be imported after scipy to prevent errors
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui

# import matplotlib.pyplot as plt


class Main:
    def __init__(self):
        # Prepare Qt
        app = QtGui.QApplication([])

        # Prepare window and OpenGL environment
        self.__widget = gl.GLViewWidget()
        self.__widget.setWindowTitle("Quantum by AgenttiX")
        self.__widget.show()

        # Create grid
        # grid = gl.GLGridItem()
        # grid.scale(10, 10, 1)
        # self.__widget.addItem(grid)

        # Default quantum numbers
        self.__n = 3
        self.__l = 1
        self.__m = 1
        self.__Z = 1

        self.__rdist = 50
        self.__data = np.zeros((self.__rdist, self.__rdist, self.__rdist), dtype=np.complex)

        # Computation parameters
        self.__zoom = 1

        widget2 = QtGui.QWidget()
        widget2.setWindowTitle("Quantum by AgenttiX")

        layout = QtGui.QGridLayout()
        widget2.setLayout(layout)

        self.radial = None
        self.__abs = None
        self.__volume = None

        labels = ["n", "l", "m", "Z"]

        for i, text in enumerate(labels):
            label = QtGui.QLabel()
            label.setText(text)
            layout.addWidget(label, i, 0)

        # Value inputs
        self.__input_n = pg.SpinBox(value=self.__n, int=True, dec=True, minStep=1, step=1)
        layout.addWidget(self.__input_n, 0, 1)

        self.__input_l = pg.SpinBox(value=self.__l, int=True, dec=True, minStep=1, step=1)
        layout.addWidget(self.__input_l, 1, 1)

        self.__input_m = pg.SpinBox(value=self.__m, int=True, dec=True, minStep=1, step=1)
        layout.addWidget(self.__input_m, 2, 1)

        self.__input_Z = pg.SpinBox(value=self.__Z, int=True, dec=True, minStep=1, step=1)
        layout.addWidget(self.__input_Z, 3, 1)

        self.__updateButton = QtGui.QPushButton("Update")
        layout.addWidget(self.__updateButton, 4, 1)

        self.__updateButton.clicked.connect(self.update)

        self.__infoLabel = QtGui.QLabel()
        layout.addWidget(self.__infoLabel, 5, 1)

        widget2.show()

        # Compute for the first time
        self.__first = True
        self.update()

        # Main loop
        app.exec_()

    def update(self):
        self.__n = self.__input_n.value()
        self.__l = self.__input_l.value()
        self.__m = self.__input_m.value()
        self.__Z = self.__input_Z.value()
        # print("Plotting", self.__n, self.__l, self.__m, self.__Z)
        if self.__n <= 0 or not 0 <= self.__l < self.__n or abs(self.__m) > self.__l:
            self.__infoLabel.setText("Invalid values")
            return
        self.__infoLabel.setText("Plotting")

        # Radial wavefunction
        sym_r = sympy.var("sym_r")
        self.radial = sympy.lambdify(sym_r, sympy.physics.hydrogen.R_nl(self.__n, self.__l, sym_r, self.__Z))

        offset = self.__rdist / 2

        # Compute psi for every point in the desired space
        for x in range(0, self.__rdist):
            for y in range(0, self.__rdist):
                for z in range(0, self.__rdist):
                    self.__data[x, y, z] = self.psi_cartesian(self.__zoom*(x - offset), self.__zoom*(y - offset), self.__zoom*(z - offset))

        self.__abs = np.abs(self.__data)
        self.__abs.astype(np.float)
        self.__abs = np.power(self.__abs, 2)

        # print(abs)
        # print(abs.max())
        # print(abs.min())

        # print(abs[0,:,:])

        # clipped = np.log(np.clip(abs, 0, abs.max()) ** 2)

        # positive = np.log(np.clip(abs, 0, abs.max()) ** 2)
        # negative = np.log(np.clip(-abs, 0, -abs.min()) ** 2)

        # d2 array has the form x, y, z, RGBA
        # http://www.pyqtgraph.org/documentation/3dgraphics/glvolumeitem.html
        d2 = np.zeros(self.__abs.shape + (4,), dtype=np.ubyte)

        # R
        d2[..., 0] = self.__abs * (255. / self.__abs.max())
        # G
        d2[..., 1] = d2[..., 0]
        # B
        d2[..., 2] = d2[..., 0]

        # A
        d2[..., 3] = d2[..., 0]
        d2[..., 3] = ((d2[..., 3] / 255.)**2) * 255

        d2[:, 0, 0] = [255, 0, 0, 100]
        d2[0, :, 0] = [0, 255, 0, 100]
        d2[0, 0, :] = [0, 0, 255, 100]

        # plt.imshow(abs[0,:,:])
        # plt.show()

        if self.__first:
            self.__first = False
            self.__volume = gl.GLVolumeItem(d2)
            self.__volume.translate(-offset, -offset, -offset)
            self.__widget.addItem(self.__volume)
        else:
            self.__volume.setData(d2)

        self.__infoLabel.setText("Ready")

    def psi_radial(self, r, theta, phi):
        # Radial * spherical
        if self.__l == 0:
            return self.radial(r)
        else:
            return self.radial(r) * ((-1)**self.__m) * scipy.special.sph_harm(self.__m, self.__l, phi, theta)

    def psi_cartesian(self, x, y, z):
        theta = np.arctan2(z, (x**2 + y**2)**0.5)
        phi = np.arctan2(y, x)
        r = (x**2 + y**2 + z**2)**0.5
        return self.psi_radial(r, theta, phi)


def main():
    Main()

main()
