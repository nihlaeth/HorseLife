from sqlalchemy import func

from generator import Generator
from models.building import Building
from models.buildingproperties import BuildingProperties


class BuildingGenerator(Generator):
    @classmethod
    def _gen_one(cls, location, b_type):
        # TODO: store as much as possible in config
        # files and fetch from there.
        if b_type == "Stable":
            properties = [
                BuildingProperties(
                    name="Cleanliness",
                    value=100)]
        else:
            properties = []
        return Building(name=b_type,
                        building_type=b_type,
                        location=location,
                        properties=properties)

    @classmethod
    def gen_many(cls, session, n, b_type="Stable"):
        max_l = session.query(func.max(Building.location)).scalar()
        if max_l is None:
            max_l = -1
        result = []
        for i in range(n):
            max_l += 1
            result.append(cls._gen_one(max_l, b_type))
        session.add_all(result)
