import streamlit as st
import requests
import websocket
import json
import streamlit.components.v1 as components

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
    
    graph_data=r.json()
    
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