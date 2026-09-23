import re
import json

class MermaidCompiler:
    """
    Compiles a Mermaid.js flowchart string into a deterministic NetworkX-compatible
    DAG dictionary used by the Sweetbrier Architecture.
    """
    def __init__(self):
        # Regex to capture node definitions like: A[Node Label]
        self.node_def_pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*\[(.*?)\]\s*$')
        
        # Regex to capture edge definitions like: A --> B or A[Label] --> B[Label]
        self.edge_pattern = re.compile(r'^\s*(.*?)\s*-->\s*(.*?)\s*$')
        
        # Regex to capture node ID and label inline, e.g., A[Label]
        self.inline_node_pattern = re.compile(r'^([A-Za-z0-9_]+)\s*\[(.*?)\]$')

    def parse(self, mermaid_string: str) -> dict:
        """
        Parses a Mermaid string and returns a Sweetbrier-compatible DAG dict:
        { "nodes": [list of strings], "edges": [[source, target], ...] }
        """
        lines = mermaid_string.strip().split('\n')
        
        node_map = {} # Maps ID to Label (e.g., 'A': 'Protect Truth')
        edges = []
        
        for line in lines:
            # Clean up the line
            line = line.strip()
            # Remove trailing semicolons
            if line.endswith(';'):
                line = line[:-1]
                
            if not line or line.startswith('graph') or line.startswith('flowchart') or line.startswith('%'):
                continue
                
            # Check if it's an edge: A --> B
            if '-->' in line:
                source_part, target_part = self.edge_pattern.match(line).groups()
                
                # Extract source ID and optional label
                src_match = self.inline_node_pattern.match(source_part)
                if src_match:
                    src_id, src_label = src_match.groups()
                    node_map[src_id] = src_label
                else:
                    src_id = source_part.strip()
                    if src_id not in node_map:
                        node_map[src_id] = src_id # Default label is the ID
                        
                # Extract target ID and optional label
                tgt_match = self.inline_node_pattern.match(target_part)
                if tgt_match:
                    tgt_id, tgt_label = tgt_match.groups()
                    node_map[tgt_id] = tgt_label
                else:
                    tgt_id = target_part.strip()
                    if tgt_id not in node_map:
                        node_map[tgt_id] = tgt_id
                        
                edges.append([node_map[src_id], node_map[tgt_id]])
                
            else:
                # Might be a standalone node definition: A[Protect Truth]
                node_match = self.node_def_pattern.match(line)
                if node_match:
                    node_id, label = node_match.groups()
                    node_map[node_id] = label
                else:
                    # Could just be a raw node name if no special chars
                    if line and not '[' in line and not '{' in line:
                        if line not in node_map:
                            node_map[line] = line

        nodes = list(set(node_map.values()))
        
        return {
            "nodes": nodes,
            "edges": edges
        }

if __name__ == "__main__":
    test_mermaid = """
    graph TD;
        A[Inherent Dignity] --> B[Freedom of Conscience];
        B --> C[No State Coercion];
        D[Protect Truth] --> A;
    """
    
    compiler = MermaidCompiler()
    dag = compiler.parse(test_mermaid)
    print("Compiled Sweetbrier DAG:")
    print(json.dumps(dag, indent=2))
