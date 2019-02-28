from WarbleSimulation.System.Entity import Entity


class Concrete(Entity):
    default_dimension = (1, 1, 1)

    def __init__(self, uuid, dimension_x, matter_type):
        super().__init__(uuid)
        self.dimension_x = dimension_x
        self.dimension = tuple(
            [Concrete.default_dimension[i] * self.dimension_x[i] for i in range(len(Concrete.default_dimension))])
        self.matter_type = matter_type
