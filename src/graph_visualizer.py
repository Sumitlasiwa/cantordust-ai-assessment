# visualize_graph.py
from graph import graph  # Use absolute import (src.graph)

def save_graph_visualization():
    # Generate the PNG bytes
    png_data = graph.get_graph().draw_mermaid_png()
    
    # Save to file
    output_path = "workflow_graph.png"
    with open(output_path, "wb") as f:
        f.write(png_data)
    
    print(f"✅ Graph saved successfully to {output_path}")

if __name__ == "__main__":
    save_graph_visualization()   