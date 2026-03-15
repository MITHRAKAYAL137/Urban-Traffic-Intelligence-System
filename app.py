import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import random
import joblib
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Smart City Traffic AI", layout="wide")

# -------- AUTO REFRESH EVERY 10 SECONDS --------
st_autorefresh(interval=10000, key="traffic_refresh")


# -------- LIVE TRAFFIC GENERATOR --------

def generate_live_traffic():

    data = []

    for i in range(24):

        traffic_volume = random.randint(100, 1000)

        data.append({
            "hour": i,
            "traffic_volume": traffic_volume
        })

    return pd.DataFrame(data)


# -------- SIDEBAR --------

st.sidebar.title("🚦 Smart Traffic AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Traffic Dashboard",
        "Traffic Heatmap",
        "Road Network",
        "Smart Traffic Map",
        "Real City Map",
        "Traffic Prediction AI",
        "Traffic Forecast (24H)"
    ]
)


# -------- HOME --------

if page == "Home":

    st.title("🚦 Smart City Traffic AI System")

    col1, col2, col3 = st.columns(3)

    col1.metric("City Sensors", "125")
    col2.metric("Active Roads", "58")
    col3.metric("Traffic Alerts", "3")

    st.write("""
### System Features

- 📊 Real-time Traffic Dashboard
- 🔥 Traffic Density Heatmap
- 🛣 Road Network Simulation
- 🗺 Smart Traffic Network Map
- 🌍 Real City Map (OpenStreetMap)
- 🤖 AI Traffic Prediction
- 📈 24 Hour Traffic Forecast
""")


# -------- DASHBOARD --------

elif page == "Traffic Dashboard":

    st.title("📊 Real-Time Traffic Dashboard")

    if st.button("🔄 Refresh Data"):
        st.rerun()

    df = generate_live_traffic()

    total = df["traffic_volume"].sum()
    avg = int(df["traffic_volume"].mean())
    peak = int(df["traffic_volume"].max())
    low = int(df["traffic_volume"].min())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Vehicles", total)
    c2.metric("Average Traffic", avg)
    c3.metric("Peak Traffic", peak)
    c4.metric("Lowest Traffic", low)

    fig = px.line(
        df,
        x="hour",
        y="traffic_volume",
        title="Traffic Volume by Hour"
    )

    st.plotly_chart(fig, use_container_width=True)

    if avg < 400:
        st.success("Traffic Condition: Smooth 🟢")
    elif avg < 700:
        st.warning("Traffic Condition: Moderate 🟡")
    else:
        st.error("Traffic Condition: Heavy Congestion 🔴")


# -------- HEATMAP --------

elif page == "Traffic Heatmap":

    st.title("🔥 Traffic Density Heatmap")

    df = pd.read_csv("data/traffic.csv")

    heat = df.pivot_table(
        values="traffic_volume",
        index="day_of_week",
        columns="hour"
    )

    fig = px.imshow(
        heat,
        labels=dict(x="Hour", y="Day", color="Traffic Volume"),
        title="Traffic Density Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)


# -------- ROAD NETWORK --------

elif page == "Road Network":

    st.title("🛣 Road Network Simulation")

    G = nx.grid_2d_graph(6, 6)
    G = nx.convert_node_labels_to_integers(G)

    traffic_data = []

    for edge in G.edges():

        traffic_flow = random.randint(10, 100)
        avg_speed = random.randint(20, 60)

        traffic_data.append({
            "road": edge,
            "traffic_flow": traffic_flow,
            "avg_speed": avg_speed
        })

    df = pd.DataFrame(traffic_data)

    st.dataframe(df)

    st.success("36 Smart Traffic Sensors Simulated")


# -------- SMART TRAFFIC NETWORK --------

elif page == "Smart Traffic Map":

    st.title("🗺 Smart Traffic Network")

    G = nx.grid_2d_graph(6, 6)
    G = nx.convert_node_labels_to_integers(G)

    pos = nx.spring_layout(G)

    edge_traces = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        traffic = random.randint(100, 1000)

        if traffic < 400:
            color = "green"
        elif traffic < 700:
            color = "yellow"
        else:
            color = "red"

        edge_traces.append(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(width=4, color=color)
            )
        )

    node_x = []
    node_y = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        marker=dict(size=10, color="blue")
    )

    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    st.write("🟢 Low Traffic | 🟡 Medium Traffic | 🔴 Heavy Traffic")


# -------- REAL CITY MAP --------

elif page == "Real City Map":

    st.title("🌍 Real City Traffic Map")

    center_lat = 13.0827
    center_lon = 80.2707

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    for i in range(20):

        lat = center_lat + random.uniform(-0.05, 0.05)
        lon = center_lon + random.uniform(-0.05, 0.05)

        traffic = random.randint(100, 1000)

        if traffic < 400:
            color = "green"
        elif traffic < 700:
            color = "orange"
        else:
            color = "red"

        folium.CircleMarker(
            location=[lat, lon],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Traffic Volume: {traffic}"
        ).add_to(m)

    st_folium(m, width=900, height=500)


# -------- TRAFFIC PREDICTION --------

elif page == "Traffic Prediction AI":

    st.title("🤖 Traffic Congestion Prediction")

    model = joblib.load("traffic_model.pkl")

    hour = st.slider("Hour", 0, 23, 8)

    day = st.selectbox(
        "Day",
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )

    weather = st.selectbox(
        "Weather",
        ["Clear","Rain","Fog"]
    )

    temperature = st.slider("Temperature", 20, 40, 30)

    day_map = {
        "Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,
        "Friday":4,"Saturday":5,"Sunday":6
    }

    weather_map = {
        "Clear":0,"Rain":1,"Fog":2
    }

    input_data = pd.DataFrame({
        "hour":[hour],
        "day_of_week":[day_map[day]],
        "weather":[weather_map[weather]],
        "temperature":[temperature]
    })

    if st.button("Predict Traffic"):

        prediction = model.predict(input_data)

        st.success(f"Predicted Traffic Volume: {int(prediction[0])} vehicles")


# -------- TRAFFIC FORECAST --------

elif page == "Traffic Forecast (24H)":

    st.title("📈 Traffic Forecast Next 24 Hours")

    model = joblib.load("traffic_model.pkl")

    forecast = []

    for hour in range(24):

        input_data = pd.DataFrame({
            "hour":[hour],
            "day_of_week":[1],
            "weather":[0],
            "temperature":[30]
        })

        pred = model.predict(input_data)[0]

        forecast.append({
            "hour": hour,
            "predicted_traffic": pred
        })

    df = pd.DataFrame(forecast)

    fig = px.line(
        df,
        x="hour",
        y="predicted_traffic",
        title="Predicted Traffic Next 24 Hours"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)
