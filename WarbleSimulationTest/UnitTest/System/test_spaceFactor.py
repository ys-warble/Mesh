import WarbleSimulation.System.SpaceFactor as SpaceFactor
from WarbleSimulationTest.AppTestCase import AppTestCase


class TestSpaceFactor(AppTestCase):
    def setUp(self):
        super().setUp()

        # Define the default dimension and resolution
        self.dimension = (5, 5, 5)
        self.resolution = 3

    # Enum Total
    def test_space_factor_enum_total(self):
        space_factors = SpaceFactor.SpaceFactor

        total_enum = len(space_factors)

        self.logger.info('Total SpaceFactor = %d' % total_enum)
        self.logger.info('List = %s' % [i for i in space_factors])

        self.assertEqual(total_enum, 5)

    def test_matter_enum_total(self):
        total_enum = len(SpaceFactor.Matter)
        self.assertEqual(total_enum, 1)

    def test_matter_type_enum_total(self):
        total_enum = len(SpaceFactor.MatterType)
        self.assertEqual(total_enum, 13)

    def test_temperature_enum_total(self):
        total_enum = len(SpaceFactor.Temperature)
        self.assertEqual(total_enum, 1)

    def test_humidity_enum_total(self):
        total_enum = len(SpaceFactor.Humidity)
        self.assertEqual(total_enum, 1)

    def test_luminosity_enum_total(self):
        total_enum = len(SpaceFactor.Luminosity)
        self.assertEqual(total_enum, 3)

    def test_air_movement_enum_total(self):
        total_enum = len(SpaceFactor.AirMovement)
        self.assertEqual(total_enum, 3)

    # generate()
    def test_generate_valid(self):
        for space_factor_type in SpaceFactor.SpaceFactor:
            self.logger.info(space_factor_type)

            space_factor = SpaceFactor.generate(space_factor_type, self.dimension, self.resolution)

            self.logger.info('- Testing space_factor has correct keys ...')
            if space_factor_type == SpaceFactor.SpaceFactor.MATTER:
                self.assertEqual(list(space_factor.keys()), [i for i in SpaceFactor.Matter])
            elif space_factor_type == SpaceFactor.SpaceFactor.TEMPERATURE:
                self.assertEqual(list(space_factor.keys()), [i for i in SpaceFactor.Temperature])
            elif space_factor_type == SpaceFactor.SpaceFactor.HUMIDITY:
                self.assertEqual(list(space_factor.keys()), [i for i in SpaceFactor.Humidity])
            elif space_factor_type == SpaceFactor.SpaceFactor.LUMINOSITY:
                self.assertEqual(list(space_factor.keys()), [i for i in SpaceFactor.Luminosity])
            elif space_factor_type == SpaceFactor.SpaceFactor.AIR_MOVEMENT:
                self.assertEqual(list(space_factor.keys()), [i for i in SpaceFactor.AirMovement])
            else:
                raise Exception('Unknown SpaceFactor: %s' % space_factor_type)

            self.logger.info('- Testing each space factor matrices ...')
            for key, value in space_factor.items():
                self.assertEqual(value.shape, tuple([i * self.resolution for i in self.dimension]))

            self.logger.info('')
