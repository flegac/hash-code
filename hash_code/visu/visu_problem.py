import matplotlib.pyplot as plt


class Points(object):
    def __init__(self):
        self.data = dict()

    def point(self, x, y, size=1, color: str = 'blue'):
        self._init_color(color)
        self.data[color]['x'].append(x)
        self.data[color]['y'].append(y)
        self.data[color]['size'].append(size)

    def show(self, filename: str):
        for color, points in self.data.items():
            plt.scatter(points['x'], points['y'], s=points['size'], c=color, alpha=.75)

        plt.title(filename)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('{}.png'.format(filename))
        plt.show()

    def _init_color(self, color: str):
        if not self.data.get(color):
            self.data[color] = {
                'x': [],
                'y': [],
                'size': []
            }
