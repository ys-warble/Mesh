import numpy as np
import plotly.graph_objs as go
import plotly.offline as py

from Mesh import settings
from Mesh.util.PlotterTool import PlotterTool


def plot_scatter_3d(array3d,
                    zero_value=0,
                    filename=None,
                    auto_open=True,
                    opacity=1):
    func = None

    if settings.PLOTTER_TOOL == PlotterTool.PLOTLY:
        func = plotly_plot_scatter_3d

    func(array3d=array3d, zero_value=zero_value, filename=filename, auto_open=auto_open, opacity=opacity)


def plotly_plot_scatter_3d(array3d, zero_value=0, filename=None, auto_open=True, cc=1, opacity=1):
    # zero_value = 0 if ('zero_value' not in kwargs or not isinstance(kwargs['zero_value'], int)) else kwargs[
    #     'zero_value']

    x_shape = array3d.shape[0]
    y_shape = array3d.shape[1]
    z_shape = array3d.shape[2]

    y, x, z = np.meshgrid(np.arange(array3d.shape[1]), np.arange(array3d.shape[0]), np.arange(array3d.shape[2]))

    x = x.reshape(-1)
    y = y.reshape(-1)
    z = z.reshape(-1)
    array3d = array3d.reshape(-1)

    if array3d.dtype in [int, float]:
        nz_array3d_indices = (array3d > zero_value).nonzero()
    else:
        nz_array3d_indices = array3d.nonzero()

    trace1 = go.Scatter3d(
        x=x[nz_array3d_indices],
        y=y[nz_array3d_indices],
        z=z[nz_array3d_indices],
        mode='markers',
        marker=dict(
            symbol='circle',
            size=4,
            color=array3d[nz_array3d_indices],  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=opacity
        )
    )

    data = [trace1]
    layout = go.Layout(
        scene=dict(
            aspectmode='manual',
            aspectratio=go.layout.scene.Aspectratio(x=(x_shape / x_shape), y=(y_shape / x_shape),
                                                    z=(z_shape / x_shape)),
            xaxis=dict(range=[0, x_shape]),
            yaxis=dict(range=[0, y_shape]),
            zaxis=dict(range=[0, z_shape])
        )
    )
    fig = go.Figure(data=data, layout=layout)
    if filename is None:
        filename = r'3d-scatter-colorscale.html'
    py.offline.plot(fig, filename=filename, auto_open=auto_open)
