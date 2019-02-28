import os
from unittest import TestCase

import numpy as np

from WarbleSimulation.util import Plotter
from WarbleSimulationTest import test_settings


class TestPlotter(TestCase):
    def test_plotly_plot_scatter_3d(self):
        dimension = (20, 10, 5)
        resolution = 4

        space_factor_matter = np.zeros(tuple([i * resolution for i in dimension]))

        space_factor_matter[:, 0:10, 0:5] = 5
        space_factor_matter[:, 30:40, 0:5] = 3

        space_factor_matter[0:20, :, 15:20] = 4
        space_factor_matter[60:80, :, 15:20] = 3

        Plotter.plotly_plot_scatter_3d(space_factor_matter, 2,
                                       filename=os.path.join(test_settings.actual_path, '3d-scatter-colorscale.html'))
