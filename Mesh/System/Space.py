import Mesh.System.SpaceFactor as SpaceFactor


class Space:
    def __init__(self, dimension, resolution=1, space_factor_types=None):
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
        self.add_space_factor(space_factor_types)

    def add_space_factor(self, space_factor_type):
        space_factor_type = [space_factor_type] if isinstance(space_factor_type,
                                                              SpaceFactor.SpaceFactor) else space_factor_type

        if isinstance(space_factor_type, list) and all(
                isinstance(sf, SpaceFactor.SpaceFactor) for sf in space_factor_type):
            for sf in space_factor_type:
                self.space_factors[sf] = SpaceFactor.generate(sf, self.dimension, self.resolution)
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
