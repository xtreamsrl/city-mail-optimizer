import logging
import os
import re

import networkx as nx
import osmnx as ox

from src.city_mail.addresses_data_adapter import AddressData


class StreetsGraphPort:
    def get_city_graph(self) -> dict:
        pass

    def closest_node_id_from_address(self, address: AddressData) -> int:
        pass

    def city_name(self) -> str:
        pass

    def city_graph(self) -> nx.MultiDiGraph:
        pass


class OsmStreetsGraphAdapter(StreetsGraphPort):
    def __init__(self, city: str):
        self._city_name = city
        self._file_path = self._build_file_path_from_city_name(self._city_name)

        self._city_graph = self.get_city_graph()

    @property
    def city_name(self) -> str:
        return self._city_name

    @property
    def city_graph(self) -> nx.MultiDiGraph:
        return self._city_graph

    def get_city_graph(self) -> nx.MultiDiGraph:
        if not os.path.exists(self._file_path):
            logging.info(f"Cannot find the graphml file in {self._file_path}")
            logging.info(f"Downloading {self.city_name} street city graph")
            city_graph = ox.graph_from_place(
                query=self.city_name,
                network_type="drive",
                retain_all=False,
                truncate_by_edge=True,
            )
            city_graph = ox.truncate.largest_component(city_graph, strongly=True)

            ox.io.save_graphml(city_graph, filepath=self._file_path)
            logging.info(f"City graph of {self.city_name} downloaded")
        else:
            logging.info(
                f"Loading city graph of {self.city_name} from {self._file_path}"
            )
            city_graph = ox.io.load_graphml(filepath=self._file_path)

        assert nx.is_strongly_connected(city_graph)

        return city_graph

    def closest_node_id_from_address(self, address: AddressData) -> int:
        return ox.distance.nearest_nodes(
            self.city_graph, address.longitude, address.latitude
        )

    def _build_file_path_from_city_name(self, city_name: str) -> str:
        return f"graphs_data/{self._urlify(city_name)}.graphml"

    @staticmethod
    def _urlify(s):
        # Remove all non-word characters (everything except numbers and letters)
        s = re.sub(r"[^\w\s]", "", s)

        # Replace all runs of whitespace with a single dash
        s = re.sub(r"\s+", "-", s)

        return s
