import json
import os
import threading

import matplotlib.pyplot as plt
import networkx as nx
import requests
import streamlit as st
import websocket

API = os.getenv("API_URL", "http://localhost:8000")
WS_URL = os.getenv("WS_URL", "ws://localhost:8000/ws")

st.title("MindGraph OS")

if "alerts" not in st.session_state:
    st.session_state.alerts = []


def on_message(ws, message):
    try:
        data = json.loads(message)
        msg = data.get("message", message)
    except json.JSONDecodeError:
        msg = message

    st.session_state.alerts.append(msg)

def start_ws():
    if st.session_state.get("ws_started"):
        return

    st.session_state.ws_started = True

    def _run():
        ws = websocket.WebSocketApp(WS_URL, on_message=on_message)
        ws.run_forever()

    threading.Thread(target=_run, daemon=True).start()


def safe_request(method, url, **kwargs):
    timeout = kwargs.pop("timeout", 30)
    try:
        resp = requests.request(method, url, timeout=timeout, **kwargs)
    except requests.Timeout:
        st.error("Request timed out. The backend may still be processing.")
        return None
    except requests.ConnectionError:
        st.error("Backend is not reachable. Start the FastAPI server first.")
        st.sidebar.info("Run: uvicorn main:app --reload --port 8000")
        return None
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return None

    if resp.status_code >= 400:
        detail = resp.text
        if "application/json" in resp.headers.get("content-type", ""):
            try:
                detail = resp.json().get("detail", detail)
            except requests.JSONDecodeError:
                pass

        st.error(f"Backend error {resp.status_code}: {detail}")
        return None

    return resp


def safe_json(resp):
    try:
        return resp.json()
    except requests.JSONDecodeError:
        st.error("Backend returned a non-JSON response.")
        st.code(resp.text[:800])
        return None


st.sidebar.subheader("Live Alerts")
if st.sidebar.button("Connect"):
    start_ws()

if st.session_state.alerts:
    for msg in st.session_state.alerts[-5:]:
        st.sidebar.write(msg)

tab1, tab2, tab3 = st.tabs(["Upload", "Chat", "Graph"])

with tab1:

    file = st.file_uploader("Upload PDF")

    if st.button("Upload"):
        if file is None:
            st.warning("Please choose a PDF file first.")
        else:
            r = safe_request(
                "post",
                f"{API}/upload",
                files={"file": (file.name, file.getvalue(), file.type or "application/pdf")},
                timeout=120,
            )

            if r is not None:
                data = safe_json(r)
                if data is not None:
                    st.write(data)

with tab2:

    q = st.text_input("Ask")

    if st.button("Query"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            r = safe_request(
                "post",
                f"{API}/query",
                params={"q": q},
                timeout=120,
            )

            if r is not None:
                data = safe_json(r)
                if data is not None:
                    st.write(data.get("answer"))

with tab3:

    if st.button("Load Graph"):
        r = safe_request("get", f"{API}/graph")

        if r is not None:
            data = safe_json(r)
            if data is None:
                st.stop()

            edges = data.get("edges", [])

            if not edges:
                st.info("No graph data yet.")
            else:
                G = nx.Graph()
                G.add_edges_from(edges)
                fig = plt.figure()
                nx.draw(G, with_labels=True)
                st.pyplot(fig)