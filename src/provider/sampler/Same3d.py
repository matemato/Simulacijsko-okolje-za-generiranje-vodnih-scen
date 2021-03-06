import random

import mathutils

from src.main.Provider import Provider


class Same3d(Provider):
    """
    Uniformly samples a 3-dimensional vector.

    Example 1: Return a uniform;y sampled 3d vector from a range [min, max].

    .. code-block:: yaml

        {
          "provider": "sampler.Uniform3d",
          "max": [0.5, 0.5, 0.5],
          "min": [-0.5, -0.5, -0.5]
        }

    **Configuration**:

    .. list-table:: 
        :widths: 25 100 10
        :header-rows: 1

        * - Parameter
          - Description
          - Type
        * - min
          - A list of three values, describing the minimum values of 1st, 2nd, and 3rd dimensions.
          - list
        * - max
          - A list of three values, describing the maximum values of 1st, 2nd, and 3rd dimensions.
          - list
    """

    def __init__(self, config):
        Provider.__init__(self, config)

    def run(self):
        """
        :return: Sampled value. Type: mathutils.Vector
        """
        # minimum values vector
        val_min = self.config.get_float('min')
        val_max = self.config.get_float('max')

        value = random.uniform(val_min, val_max)

        position = mathutils.Vector()
        for i in range(3):
            position[i] = value

        return position
