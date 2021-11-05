from position_type import PositionType


class Position:
    def __init__(self, position):
        self.name = position.split('\\')[-1]
        self.path = position
        self.type = self._get_type_of_position(position)

    @staticmethod
    def _get_type_of_position(position):
        if "heads" in position:
            return PositionType.branch
        if "tags" in position:
            return PositionType.tag
        else:
            return PositionType.commit