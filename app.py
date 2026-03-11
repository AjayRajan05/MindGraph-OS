import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt
import websocket
import json

API="http://localhost:8000"

st.title("MindGraph OS")

def on_message(ws, message):

    data = json.loads(message)

    st.sidebar.write("Agent Alert:", data["message"])

ws = websocket.WebSocketApp(
    "ws://localhost:8000/ws",
    on_message=on_message
)

ws.run_forever()

tab1,tab2,tab3=st.tabs(["Upload","Chat","Graph"])

with tab1:

    file=st.file_uploader("Upload PDF")

    if st.button("Upload"):

        r=requests.post(
            f"{API}/upload",
            files={"file":file}
        )

        st.write(r.json())

with tab2:

    q=st.text_input("Ask")

    if st.button("Query"):

        r=requests.post(
            f"{API}/query",
            params={"q":q}
        )

        st.write(r.json()["answer"])

with tab3:

    r=requests.get(f"{API}/graph")

    edges=r.json()["edges"]

    G=nx.Graph()

    G.add_edges_from(edges)

    fig=plt.figure()

    nx.draw(G,with_labels=True)

    st.pyplot(fig)