import os

import Mesh.System.SpaceFactor as SpaceFactor
import Mesh.util.numpy_ext as npx
from Mesh import settings
from Mesh.util import Plotter
import numpy as np
import plotly.offline as py


class Space:
    def __init__(self, dimension, resolution=1, space_factor_types=None, default_value=True):
        if space_factor_types is None:
            space_factor_types = []

        if (isinstance(dimension, tuple) or isinstance(dimension, list)) \
                and len(dimension) == 3 \
                and all(isinstance(d, int) for d in dimension) \
                and isinstance(resolution, int):
            self.dimension = dimension
            self.resolution = resolution
        elif len(dimension) != 3:
            raise IndexError
        else:
            raise TypeError

        self.space_factors = {}
        self.add_space_factor(space_factor_types, default_value)

    def add_space_factor(self, space_factor_type, default_value=True):
        space_factor_type = [space_factor_type] if isinstance(space_factor_type,
                                                              SpaceFactor.SpaceFactor) else space_factor_type

        if isinstance(space_factor_type, list) and all(
                isinstance(sf, SpaceFactor.SpaceFactor) for sf in space_factor_type):
            for sf in space_factor_type:
                self.space_factors[sf] = SpaceFactor.generate(sf, self.dimension, self.resolution, default_value)
        else:
            raise TypeError

    def init_space_factor(self, space_factor_type, space_subfactor, value):
        # TODO do testing on valid input
        self.space_factors[space_factor_type][space_subfactor].fill(value)

    def __str__(self):
        string = ''
        string += 'Space'
        string += '('
        string += '\n  dimension=%s,' % str(self.dimension)
        string += '\n  resolution=%s,' % str(self.resolution)

        temp1 = []
        for a, b in self.space_factors.items():
            temp2 = []
            for c, d in b.items():
                temp2.append('%s:%s' % (str(c), d.shape))
            temp1.append('%s:{\n      ' % a + ',\n      '.join(temp2) + ']')
        if len(temp1) > 0:
            string_space_factors = '{\n    ' + ',\n    '.join(temp1) + '\n  }'
        else:
            string_space_factors = '{}'

        string += '\n  space_factors=%s' % string_space_factors
        string += '\n)'
        return string

    def plot(self, name=None, directory=None):
        if name is None:
            name = 'space'

        if directory is None:
            directory = settings.RESOURCES_PATH

        # PLOT MATTER
        Plotter.plot_scatter_3d(
            array3d=self.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(directory, name + '_matter_plot.html'),
            auto_open=True,
            opacity=1
        )

        # PLOT TEMPERATURE
        Plotter.plot_scatter_3d(
            array3d=self.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][SpaceFactor.Temperature.TEMPERATURE],
            zero_value=273,
            filename=os.path.join(directory, name + '_temperature_plot.html'),
            auto_open=True,
            opacity=0.4
        )

        # PLOT HUMIDITY
        Plotter.plot_scatter_3d(
            array3d=self.space_factors[SpaceFactor.SpaceFactor.HUMIDITY][SpaceFactor.Humidity.HUMIDITY],
            zero_value=-1,
            filename=os.path.join(directory, name + '_humidity_plot.html'),
            auto_open=True,
            opacity=0.4
        )

        # PLOT LUMINOSITY
        luminosity = npx.char.mod('hsl(%d,%d%,%d%)', (
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE],
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION],
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS]))
        Plotter.plot_scatter_3d(
            array3d=luminosity,
            zero_value=-1,
            filename=os.path.join(directory, name + '_luminosity_plot.html'),
            auto_open=True,
            opacity=0.4
        )

        # PLOT AIR MOVEMENT
        x, y, z = np.meshgrid(np.arange(0, self.dimension[0] + 1, 1),
                              np.arange(0, self.dimension[1] + 1, 1),
                              np.arange(0, self.dimension[2] + 1, 1))

        u = self.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.X]
        v = self.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Y]
        w = self.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Z]

        def flatten_vf(x, y, z, u, v, w):
            return x.flatten(), y.flatten(), z.flatten(), u.flatten(), v.flatten(), w.flatten()

        x, y, z, u, v, w = flatten_vf(x, y, z, u, v, w)
        pl_deep = [[0.0, 'rgb(39, 26, 44)'],
                   [0.1, 'rgb(53, 41, 74)'],
                   [0.2, 'rgb(63, 57, 108)'],
                   [0.3, 'rgb(64, 77, 139)'],
                   [0.4, 'rgb(61, 99, 148)'],
                   [0.5, 'rgb(65, 121, 153)'],
                   [0.6, 'rgb(72, 142, 157)'],
                   [0.7, 'rgb(80, 164, 162)'],
                   [0.8, 'rgb(92, 185, 163)'],
                   [0.9, 'rgb(121, 206, 162)'],
                   [1.0, 'rgb(165, 222, 166)']]
        trace2 = dict(type='cone',
                      x=x,
                      y=y,
                      z=z,
                      u=u,
                      v=v,
                      w=w,
                      sizemode='scaled',
                      sizeref=0.25,  # this is the default value
                      showscale=True,
                      colorscale=pl_deep,
                      colorbar=dict(thickness=20, ticklen=4),
                      anchor='tail'
                      )

        fig2 = dict(data=[trace2])
        py.offline.plot(fig2, filename=os.path.join(directory, name + '_airmovement_plot.html'), validate=False)
