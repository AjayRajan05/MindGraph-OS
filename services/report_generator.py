from weasyprint import HTML
from agents.staleness_agent import find_stale_concepts
from agents.connection_agent import find_connections


def generate_report():

    stale = find_stale_concepts()

    connections = find_connections()

    html = f"""
    <h1>MindGraph Knowledge Debt Report</h1>

    <h2>Stale Knowledge</h2>
    <ul>
    {"".join(f"<li>{s}</li>" for s in stale)}
    </ul>

    <h2>Potential Connections</h2>
    <ul>
    {"".join(f"<li>{a} ↔ {b}</li>" for a,b in connections)}
    </ul>
    """

    HTML(string=html).write_pdf("knowledge_report.pdf")

    return "knowledge_report.pdf"