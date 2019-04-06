import numpy as np

from Mesh.System.Entity import Entity
from Mesh.System.Entity.Function import Function, FunctionSetError


def transform_shape(entity_shape, from_direction, to_direction):
    # TODO check validity of entity and to_direction
    if not isinstance(entity_shape, np.ndarray) or \
            not isinstance(from_direction, tuple) or \
            not isinstance(to_direction, tuple):
        raise TypeError

    if len(from_direction) != 3 or len(to_direction) != 3:
        raise IndexError

    if not ((from_direction.count(1) == 1 or from_direction.count(-1) == 1) and from_direction.count(0) == 2) or \
            not ((to_direction.count(1) == 1 or to_direction.count(-1) == 1) and to_direction.count(0) == 2):
        raise NotImplementedError

    if from_direction == to_direction:
        return entity_shape
    else:
        f_s = False
        f = 0
        if 1 in from_direction:
            f = from_direction.index(1)
            f_s = False
        elif -1 in from_direction:
            f = from_direction.index(-1)
            f_s = True

        t_s = False
        t = 0
        if 1 in to_direction:
            t = to_direction.index(1)
            t_s = False
        elif -1 in to_direction:
            t = to_direction.index(-1)
            t_s = True

        if f_s is not t_s and f == t:
            rot_k = 2
            if t == 0:
                t = 1
            else:
                t = 0
            rot_dir = (f, t)
        elif f_s is not t_s:
            rot_k = 1
            rot_dir = (t, f)
        else:
            rot_k = 1
            rot_dir = (f, t)

        return np.rot90(entity_shape, rot_k, rot_dir)


class Concrete(Entity):
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x, matter_type, selected_functions):
        super().__init__(uuid)
        self.dimension_x = dimension_x
        self.dimension = tuple([
            type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))
        ])
        self.matter_type = matter_type

        # Functions
        self.functions = dict()
        if not self.validate_functions(selected_functions):
            raise FunctionSetError
        self.define_functions(selected_functions)
        self.eval_functions()

    # SHAPE
    def get_shape(self):
        return self.get_multiplied_shape()

    def get_default_shape(self):
        raise NotImplementedError

    def get_multiplied_shape(self):
        if self.get_default_shape() is None:
            return None
        else:
            multiplier = tuple(
                [int(self.dimension[i] / type(self).default_dimension[i]) for i in range(len(self.dimension))])
            return np.kron(self.get_default_shape(), np.ones(multiplier))

    # FUNCTIONS
    def validate_functions(self, selected_functions):
        raise NotImplementedError

    def define_functions(self, selected_functions):
        raise NotImplementedError

    def eval_functions(self):
        for key, val in self.functions.items():
            val.eval()

    def has_function(self, function):
        if function in self.functions and self.functions[function] is not None:
            return True
        else:
            return False

    def get_function(self, function):
        if self.has_function(function):
            return self.functions[function]
        else:
            return None

    # TASK
    def send_task(self, task):
        return self.get_function(Function.TASKED).send(task)

    def recv_task_resp(self):
        return self.get_function(Function.TASKED).recv()

    # PYTHON BUILT IN
    def __str__(self):
        return '%s(uuid=.%s,dim=%s,matter=%s)' % (type(self).__name__,
                                                  str(self.uuid)[-8:],
                                                  self.dimension,
                                                  self.matter_type)
