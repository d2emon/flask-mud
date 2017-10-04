from global_vars import logger


class WorldFile():
    SIZE_OF_LONG = 4
    data = [0] * 600

    @property
    def pos(self):
        return self.__pos * 64 * self.SIZE_OF_LONG

    def open(self, unit):
        self.unit = unit
        self.__pos = 0
        logger().debug("fopen(%s)", unit)

    def seek(self, pos):
        self.__pos = pos
        logger().debug("fseek(%s, %d, %d)", self.unit, self.pos, 0)

    def sec_read(self, l):
        block = []
        lw = l * self.SIZE_OF_LONG
        logger().debug("%d (%d)", self.pos, self.__pos)
        logger().debug("fread(%s, %d, %d, %s)", block, lw, 1, self.unit)
        return block

    def sec_write(self, block, l):
        lw = l * self.SIZE_OF_LONG
        logger().debug("%d (%d)", self.pos, self.__pos)
        logger().debug("fwrite(%s, %d, %d, %s)", block, lw, 1, self.unit)
