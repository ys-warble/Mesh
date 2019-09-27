import logging
import os

from Mesh.util.PlotterTool import PlotterTool

# Logging
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = None

LOGGING_CONSOLE = True
LOGGING_CONSOLE_LEVEL = None
LOGGING_CONSOLE_FORMAT = None

LOGGING_FILE = False
LOGGING_FILE_NAME = 'run.log'
LOGGING_FILE_LEVEL = None
LOGGING_FILE_FORMAT = '%(asctime)s - P%(process)d - %(name)s - %(levelname)s - %(message)s'

# Plotting
PLOTTER_TOOL = PlotterTool.PLOTLY

# Entity
ENTITY_TASK_POLLING_DURATION = 2  # in seconds

# RESOURCES
RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resources')
