import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List


class DataLoader:
    _instance = None
    _data_cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"

    def load_json(self, filename: str) -> List[Dict[str, Any]]:
        if filename not in self._data_cache:
            file_path = self.data_dir / filename
            with open(file_path, "r", encoding="utf-8") as f:
                self._data_cache[filename] = json.load(f)
        return self._data_cache[filename]

    @property
    def provinces(self) -> List[Dict[str, Any]]:
        return self.load_json("provinces.min.json")

    @property
    def districts(self) -> List[Dict[str, Any]]:
        return self.load_json("districts.min.json")

    @property
    def neighborhoods(self) -> List[Dict[str, Any]]:
        return self.load_json("neighborhoods.min.json")

    @property
    def villages(self) -> List[Dict[str, Any]]:
        return self.load_json("villages.min.json")

    @property
    def towns(self) -> List[Dict[str, Any]]:
        return self.load_json("towns.min.json")

    @property
    @lru_cache(maxsize=1)
    def districts_by_province(self) -> Dict[int, List[Dict[str, Any]]]:
        """
        Index districts by province_id for O(1) lookups.

        Returns:
            Dictionary mapping province_id to list of district summaries
        """
        index = defaultdict(list)
        for district in self.districts:
            index[district["provinceId"]].append(
                {
                    "id": district["id"],
                    "name": district["name"],
                    "population": district["population"],
                    "area": district["area"],
                }
            )
        return dict(index)

    @property
    @lru_cache(maxsize=1)
    def neighborhoods_by_district(self) -> Dict[int, List[Dict[str, Any]]]:
        """
        Index neighborhoods by district_id for O(1) lookups.

        Returns:
            Dictionary mapping district_id to list of neighborhood summaries
        """
        index = defaultdict(list)
        for neighborhood in self.neighborhoods:
            index[neighborhood["districtId"]].append(
                {"id": neighborhood["id"], "name": neighborhood["name"], "population": neighborhood["population"]}
            )
        return dict(index)

    @property
    @lru_cache(maxsize=1)
    def villages_by_district(self) -> Dict[int, List[Dict[str, Any]]]:
        """
        Index villages by district_id for O(1) lookups.

        Returns:
            Dictionary mapping district_id to list of village summaries
        """
        index = defaultdict(list)
        for village in self.villages:
            index[village["districtId"]].append(
                {"id": village["id"], "name": village["name"], "population": village["population"]}
            )
        return dict(index)


data_loader = DataLoader()
