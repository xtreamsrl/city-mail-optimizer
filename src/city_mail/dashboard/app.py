from io import StringIO

import streamlit as st
import leafmap.foliumap as leafmap
import osmnx as ox

from city_mail.delivery_optimizer.addresses_data_adapter import NominatimAddressesDataAdapter
from city_mail.delivery_optimizer.osm_streets_graph_adapter import OsmStreetsGraphAdapter
from city_mail.delivery_optimizer.path_optimizer_service import PathOptimizerApplication

with st.sidebar:
    st.title("City Mail Deliveries Optimizer")
    city_name = st.text_input("City Name", key="city_name")

    uploaded_file = st.file_uploader("Choose an addresses file")


m = leafmap.Map()
m.add_basemap('OpenStreetMap')
if city_name:
    address_adapter = NominatimAddressesDataAdapter()
    osm_street_graph = OsmStreetsGraphAdapter(city_name)
    path_optimizer = PathOptimizerApplication(
        streets_graph_adapter=osm_street_graph,
        address_data_adapter=address_adapter
    )

    m = leafmap.Map(center=(address_adapter.get_address_data(city_name).latitude,
                            address_adapter.get_address_data(city_name).longitude), zoom=16)

    if uploaded_file is not None:
        addresses = StringIO(uploaded_file.getvalue().decode("utf-8")).readlines()
        best_route, delivery_nodes, starting_node = path_optimizer.calculate_shortest_path(
             addresses
        )

        ox.plot_route_folium(osm_street_graph.city_graph, best_route, m)

m.to_streamlit()