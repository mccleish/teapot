import sys
import re

def parse_and_convert(data):
    vertices = []
    faces = []

    # 1. Parse the input data
    lines = data.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split()
        identifier = parts[0]
        
        if identifier == 'v':
            # Parse Vertex: v x y z
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            vertices.append({'x': x, 'y': y, 'z': z})
            
        elif identifier == 'f':
            # Parse Face: f v1 v2 v3 ...
            # OBJ files use 1-based indexing, JS uses 0-based.
            # We subtract 1 from every index.
            face_indices = []
            for p in parts[1:]:
                # Handle cases like "v/vt/vn" or just "v"
                index_str = p.split('/')[0]
                face_indices.append(int(index_str) - 1)
            faces.append(face_indices)

    if not vertices:
        return "// No vertices found in input."

    # 2. Normalize Vertices (Range -1 to 1)
    
    # Find min/max for each axis
    min_x = min(v['x'] for v in vertices)
    max_x = max(v['x'] for v in vertices)
    min_y = min(v['y'] for v in vertices)
    max_y = max(v['y'] for v in vertices)
    min_z = min(v['z'] for v in vertices)
    max_z = max(v['z'] for v in vertices)

    # Calculate center of the bounding box
    center_x = (min_x + max_x) / 1.0
    center_y = (min_y + max_y) / 1.0
    center_z = (min_z + max_z) / 1.0

    # Determine the largest dimension (to scale uniformly)
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    max_dim = max(width, height, depth)

    # Scale factor (Target size is 2.0, i.e., from -1 to 1)
    scale = 1.0 / max_dim if max_dim != 0 else 1.0

    normalized_vs = []
    for v in vertices:
        nx = (v['x'] - center_x) * scale
        ny = (v['y'] - center_y) * scale
        nz = (v['z'] - center_z) * scale
        normalized_vs.append({'x': nx, 'y': ny, 'z': nz})

    # 3. Generate Output String
    output = []
    
    # Output Vertices
    output.append(f"// Normalized vertices ({len(normalized_vs)} total)")
    output.append("const vs = [")
    for v in normalized_vs:
        # Formatting to 6 decimal places for precision
        output.append(f"    {{x: {v['x']:.6f}, y: {v['y']:.6f}, z: {v['z']:.6f}}},")
    output.append("]")
    output.append("")

    # Output Faces
    output.append(f"// Faces ({len(faces)} total)")
    output.append("const fs = [")
    for f in faces:
        # Convert list to string brackets
        indices_str = ", ".join(map(str, f))
        output.append(f"    [{indices_str}],")
    output.append("]")

    return "\n".join(output)

if __name__ == "__main__":
    # check if input is piped or file provided, else prompt
    input_data = ""
    if not sys.stdin.isatty():
        input_data = sys.stdin.read()
    elif len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            print(f"Error: File {sys.argv[1]} not found.")
            sys.exit(1)
    else:
        print("Please provide input via pipe or filename argument.")
        print("Usage: python convert.py input.txt > output.js")
        sys.exit(1)

    print(parse_and_convert(input_data))