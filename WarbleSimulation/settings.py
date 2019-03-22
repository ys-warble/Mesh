import logging

from WarbleSimulation.util.PlotterTool import PlotterTool

# Logging
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = None

LOGGING_CONSOLE = True
LOGGING_CONSOLE_LEVEL = LOGGING_LEVEL
LOGGING_CONSOLE_FORMAT = '%(asctime)s - P%(process)d - %(name)s - %(levelname)s - %(message)s'

LOGGING_FILE = True
LOGGING_FILE_NAME = 'run.log'
LOGGING_FILE_LEVEL = LOGGING_LEVEL
LOGGING_FILE_FORMAT = '%(asctime)s - P%(process)d - %(name)s - %(levelname)s - %(message)s'

# Plotting
PLOTTER_TOOL = PlotterTool.PLOTLY

# Entity
ENTITY_TASK_POLLING_DURATION = 2  # in seconds
