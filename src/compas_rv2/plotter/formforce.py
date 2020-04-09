import matplotlib.pyplot as plt


class FormForcePlotter(object):

    def __init__(self, form, force):
        self._figure = None
        self._axes = None
        self.form = form
        self.force = force

    @property
    def figure(self):
        if not self._figure:
            self.init()
        return self._figure

    @property
    def axes(self):
        if not self._axes:
            self.init()
        return self._axes

    def init(self):
        figure, (ax0, ax1) = plt.subplots(1, 2, sharex=True, sharey=True)
        ax0.set_aspect('equal')
        ax0.grid(b=False)
        ax0.set_frame_on(False)
        ax0.set_xscale('linear')
        ax0.set_yscale('linear')
        ax0.set_xticks([])
        ax0.set_yticks([])
        ax1.set_aspect('equal')
        ax1.grid(b=False)
        ax1.set_frame_on(False)
        ax1.set_xscale('linear')
        ax1.set_yscale('linear')
        ax1.set_xticks([])
        ax1.set_yticks([])
        self._figure = figure
        self._axes = ax0, ax1

    def show(self):
        for axes in self.axes:
            axes.autoscale()
        plt.tight_layout()
        plt.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
