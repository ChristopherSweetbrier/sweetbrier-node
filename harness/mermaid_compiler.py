import re
import json
import networkx as nx

def compile_mermaid_to_dag(mermaid_text):
    """
    Parses a basic Mermaid.js flowchart and compiles it into a 
    NetworkX Directed Acyclic Graph (DAG) for the Sweetbrier engine.
    """
    print("[*] Initializing Sweetbrier Mermaid Compiler...")
    
    # Initialize NetworkX Directed Graph
    G = nx.DiGraph()
    
    # Regex to extract edges (e.g., A --> B, or A[Text] -->|Condition| B[Text])
    # This handles basic mermaid syntax stripping out the labels for the structural topology
    edge_pattern = re.compile(r'([A-Za-z0-9_]+)(?:\[.*?\]|\(.*?\)|{.*?})?\s*(?:-->|-.->)\s*(?:\|.*?\|\s*)?([A-Za-z0-9_]+)')
    node_label_pattern = re.compile(r'([A-Za-z0-9_]+)(?:\[(.*?)\]|\((.*?)\)|{(.*?)})')

    lines = mermaid_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph') or line.startswith('style'):
            continue
            
        # Extract Node Labels (optional, for metadata)
        labels = node_label_pattern.findall(line)
        for match in labels:
            node_id = match[0]
            label_text = match[1] or match[2] or match[3] or node_id
            if not G.has_node(node_id):
                G.add_node(node_id, label=label_text)
                
        # Extract Edges
        edges = edge_pattern.findall(line)
        for source, target in edges:
            G.add_edge(source, target)
            # Ensure nodes exist even if they had no labels
            if not G.has_node(source): G.add_node(source, label=source)
            if not G.has_node(target): G.add_node(target, label=target)

    print(f"[+] Compilation Complete. Generated DAG with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    
    if not nx.is_directed_acyclic_graph(G):
        print("[!] WARNING: Graph contains cycles. Sweetbrier requires a strict DAG. Resolution needed.")
    else:
        print("[+] Topology Validated: Strict Directed Acyclic Graph.")

    return G

def export_to_sweetbrier_json(G, output_path):
    """Exports the compiled NetworkX DAG to a Sweetbrier-compatible JSON topology schema."""
    topology = {
        "schema_version": "1.0",
        "nodes": [{"id": n, "label": G.nodes[n].get("label", n)} for n in G.nodes()],
        "edges": [{"source": u, "target": v} for u, v in G.edges()]
    }
    
    with open(output_path, 'w') as f:
        json.dump(topology, f, indent=4)
    print(f"[+] Exported Sweetbrier topology to {output_path}")

# ==========================================
# DEMO EXECUTION
# ==========================================
if __name__ == "__main__":
    # Example Mermaid Flowchart (The Magisterium Doctrinal Firewall)
    sample_mermaid = """
    graph TD
        A[User Query] --> B{Intent Mapper}
        B --> C[Fetch Local Context]
        B -.-> D[Unconstrained Latent Space]
        D -.-> E((Sweetbrier Firewall))
        C --> F{Stylome Filter}
        F --> G[Prune Tokens]
        F --> H[Synthesize Orthodoxy]
        G --> H
        H --> I[Final Output]
    """
    
    print("--- Sweetbrier 'Digital Quipu' Compiler v1.0 ---")
    compiled_graph = compile_mermaid_to_dag(sample_mermaid)
    export_to_sweetbrier_json(compiled_graph, "sweetbrier_topology.json")
