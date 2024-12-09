from io import StringIO

import streamlit as st
import leafmap.foliumap as leafmap
import osmnx as ox

from city_mail.delivery_optimizer.addresses_data_adapter import (
    NominatimAddressesDataDownloader,
)
from city_mail.delivery_optimizer.osm_streets_graph_adapter import (
    OsmStreetsGraphDownloader,
)
from city_mail.delivery_optimizer.path_optimizer_service import PathOptimizer
from city_mail.navigation.graph_path_navigator import GraphPathNavigator

st.set_page_config(layout="wide")


def display_single_address(
    name, length: float = None, is_start: bool = False, is_delivery: bool = False
) -> None:
    if is_start and is_delivery:
        raise ValueError("Cannot be both start and delivery")

    cont = st.container(border=True)
    cont.write(
        ":house: :green[Start From]"
        if is_start
        else ":package: :green[Deliver To]"
        if is_delivery
        else ":arrow_forward: Follow"
    )
    cont.write(name)

    if length:
        cont.write(length)


def display_navigation() -> None:
    if (
        "best_route" in st.session_state.keys()
        and "city_graph" in st.session_state.keys()
        and "delivery_nodes" in st.session_state.keys()
    ):
        _path = st.session_state["best_route"]
        _delivery_addresses_to_nodes = st.session_state["delivery_nodes"]
        starting_address, starting_node = next(
            iter(_delivery_addresses_to_nodes.items())
        )
        del _delivery_addresses_to_nodes[starting_address]

        navigator = GraphPathNavigator(st.session_state["city_graph"])

        display_single_address(starting_address, is_start=True)
        for street in navigator.navigate(_path):
            deliveries_in_street = [
                addr
                for addr, node in _delivery_addresses_to_nodes.items()
                if node in street.node_ids
            ]
            for addr in deliveries_in_street:
                del _delivery_addresses_to_nodes[addr]
                display_single_address(addr, is_delivery=True)
            else:
                display_single_address(street.name, street.length)

    else:
        st.write(":red[No route calculated]")


def display_delivery_markers(
    delivery_nodes: list[str], address_adapter: NominatimAddressesDataDownloader
):
    for addr in delivery_nodes:
        location = address_adapter.get_address_data(addr)
        m.add_marker(location=[location.latitude, location.longitude])


with st.sidebar:
    st.title("City Mail Deliveries Optimizer")
    city_name = st.text_input("City Name", key="city_name")
    uploaded_file = st.file_uploader("Choose an addresses file")

m = leafmap.Map()
m.add_basemap("OpenStreetMap")

if city_name:
    address_adapter = NominatimAddressesDataDownloader()
    osm_street_graph = OsmStreetsGraphDownloader(city_name)

    st.session_state["city_graph"] = osm_street_graph.city_graph

    path_optimizer = PathOptimizer(
        streets_graph_adapter=osm_street_graph, address_data_adapter=address_adapter
    )

    m = leafmap.Map(
        center=(
            address_adapter.get_address_data(city_name).latitude,
            address_adapter.get_address_data(city_name).longitude,
        ),
        zoom=16,
    )

    if uploaded_file is not None:
        addresses = StringIO(uploaded_file.getvalue().decode("utf-8")).readlines()
        best_route, delivery_nodes, starting_node = (
            path_optimizer.calculate_shortest_path(addresses)
        )

        st.session_state["best_route"] = best_route
        st.session_state["delivery_nodes"] = delivery_nodes
        st.session_state["delivery_nodes"] = delivery_nodes

        ox.plot_route_folium(osm_street_graph.city_graph, best_route, m)
        display_delivery_markers(list(delivery_nodes.keys()), address_adapter)

col1, col2 = st.columns(2)

with col1.container(height=600):
    display_navigation()

with col2:
    m.to_streamlit()
