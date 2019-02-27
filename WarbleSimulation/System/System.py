from WarbleSimulation.System.Space import Space


class System:
    def __init__(self, name):
        self.name = name

        self.space = None
        self.entities = []

    def put_space(self, dimension, resolution=1, space_factor_types=None):
        """

        :param dimension: tuple: representing 3-dimensional space measures
        :param resolution: int: resolution for each space measure
        :param space_factor_types: list: ...
        :return:
        """
        if space_factor_types is None:
            space_factor_types = []

        self.space = Space(dimension, resolution, space_factor_types)

        # TODO: How if the space is re-put after putting entities?

    def put_entity(self, entity, location, direction):
        # TODO check validity

        # Matter placement
        # self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER]

        is_fit = False

        if is_fit:
            self.entities.append((entity, location, direction))

        return is_fit

    def remove_entity(self):
        pass
