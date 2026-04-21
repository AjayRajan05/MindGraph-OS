import json
import os
import threading

import matplotlib.pyplot as plt
import networkx as nx
import requests
import streamlit as st
import streamlit.components.v1 as components
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

            raw_edges = data.get("edges", [])
            edges = []
            for edge in raw_edges:
                if isinstance(edge, (list, tuple)) and len(edge) >= 2:
                    source, target = edge[0], edge[1]
                elif isinstance(edge, dict):
                    payload = edge.get("data", {})
                    source = payload.get("source")
                    target = payload.get("target")
                else:
                    continue

                if source is None or target is None:
                    continue

                edges.append((source, target))

            if not edges:
                st.info("No graph data yet.")
            else:
                G = nx.Graph()
                G.add_edges_from(edges)
                fig = plt.figure()
                nx.draw(G, with_labels=True)
                st.pyplot(fig)
    r = safe_request("get", f"{API}/graph")
    if r is None:
        st.info("Graph data is unavailable until the backend is running.")
    else:
        graph_data = safe_json(r)
        if graph_data is None:
            st.stop()

        graph_data = {
            "nodes": graph_data.get("nodes", []),
            "edges": graph_data.get("edges", []),
        }

        # Cytoscape.js HTML component
        html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MindGraph OS - Interactive Knowledge Graph</title>
        <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
        <style>
            #cy {{
                width: 100%;
                height: 600px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}
            .controls {{
                margin-bottom: 10px;
                padding: 10px;
                background: #f0f2f6;
                border-radius: 8px;
            }}
            .node-info {{
                margin-top: 10px;
                padding: 10px;
                background: #e8f4fd;
                border-radius: 8px;
                border-left: 4px solid #2196F3;
            }}
        </style>
    </head>
    <body>
        <div class="controls">
            <button onclick="resetLayout()">Reset Layout</button>
            <button onclick="fitToScreen()">Fit to Screen</button>
            <select id="layoutSelect" onchange="changeLayout()">
                <option value="cose">Force-directed</option>
                <option value="circle">Circle</option>
                <option value="grid">Grid</option>
                <option value="breadthfirst">Hierarchical</option>
            </select>
        </div>
        <div id="cy"></div>
        <div id="nodeInfo" class="node-info" style="display: none;">
            <h4>Selected Node:</h4>
            <p id="nodeDetails"></p>
        </div>

        <script>
            var graphData = {json.dumps(graph_data)};
            
            var cy = cytoscape({{
                container: document.getElementById('cy'),
                elements: [
                    ...graphData.nodes.map(node => ({{
                        data: node.data,
                        style: {{
                            'background-color': getNodeColor(node.data.type),
                            'label': node.data.label,
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'color': '#fff',
                            'font-size': '12px',
                            'border-width': 2,
                            'border-color': '#333'
                        }}
                    }})),
                    ...graphData.edges.map(edge => ({{
                        data: edge.data,
                        style: {{
                            'width': 2,
                            'line-color': '#666',
                            'target-arrow-color': '#666',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier',
                            'label': edge.data.label,
                            'font-size': '10px',
                            'color': '#333'
                        }}
                    }}))
                ],
                layout: {{
                    name: 'cose',
                    idealEdgeLength: 100,
                    nodeOverlap: 20,
                    refresh: 20,
                    fit: true,
                    padding: 30,
                    randomize: false,
                    componentSpacing: 100,
                    nodeRepulsion: 400000,
                    edgeElasticity: 100,
                    nestingFactor: 5,
                    gravity: 80,
                    numIter: 1000,
                    initialTemp: 200,
                    coolingFactor: 0.95,
                    minTemp: 1.0
                }},
                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'width': '60px',
                            'height': '60px'
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 2,
                            'line-color': '#666',
                            'target-arrow-color': '#666',
                            'target-arrow-shape': 'triangle'
                        }}
                    }}
                ]
            }});

            function getNodeColor(type) {{
                switch(type) {{
                    case 'Concept': return '#2196F3';
                    case 'Chunk': return '#4CAF50';
                    case 'Document': return '#FF9800';
                    default: return '#9E9E9E';
                }}
            }}

            function changeLayout() {{
                var layoutName = document.getElementById('layoutSelect').value;
                cy.layout({{ name: layoutName }}).run();
            }}

            function resetLayout() {{
                cy.layout({{ name: 'cose' }}).run();
            }}

            function fitToScreen() {{
                cy.fit();
            }}

            // Node selection handler
            cy.on('tap', 'node', function(evt) {{
                var node = evt.target;
                var nodeInfo = document.getElementById('nodeInfo');
                var nodeDetails = document.getElementById('nodeDetails');
                
                nodeInfo.style.display = 'block';
                nodeDetails.innerHTML = `
                    <strong>ID:</strong> ${{node.data('id')}}<br>
                    <strong>Type:</strong> ${{node.data('type')}}<br>
                    <strong>Label:</strong> ${{node.data('label')}}<br>
                    <strong>Connections:</strong> ${{node.degree()}} nodes
                `;
            }});

            // Click on empty space to deselect
            cy.on('tap', function(event) {{
                if(event.target === cy) {{
                    document.getElementById('nodeInfo').style.display = 'none';
                }}
            }});
        </script>
    </body>
    </html>
    """

        components.html(html_code, height=700)