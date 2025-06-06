#!/usr/bin/env python3
"""
Author: Parth Bandivadekar
Lab: Ahn Lab, UC Davis
Date: 2025-06-05
Purpose: [Auto-generated placeholder purpose; please edit]
Usage: python add_headers.py
Dependencies: [Auto-detected; please edit]
"""

import os
import re
from datetime import date

# Today's date
today = date.today().strftime("%Y-%m-%d")

# Directory to search for .py files (change if needed)
root_dir = "."

# Header template
header_template = '''#!/usr/bin/env python3
"""
Author: Parth Bandivadekar
Lab: Ahn Lab, UC Davis
Date: {date}
Purpose: {purpose}
Usage: python {script_name} {usage}
Dependencies: {dependencies}
"""
'''

def detect_dependencies_and_purpose(file_path):
    """
    Inspect the Python file to detect imported modules and guess purpose.
    """
    dependencies = set()
    purpose = "Auto-generated placeholder purpose; please edit"

    # Guess purpose from filename
    filename = os.path.basename(file_path)
    name_no_ext = os.path.splitext(filename)[0]
    # Replace underscores/hyphens with spaces and capitalize first letter
    formatted_name = name_no_ext.replace('_', ' ').replace('-', ' ').capitalize()
    purpose = f"Performs {formatted_name}"

    with open(file_path, 'r') as f:
        for line in f:
            # Detect import statements (e.g., `import numpy` or `from mdanalysis import *
            match_import = re.match(r'\s*(?:import|from)\s+([\w_]+)', line)
            if match_import:
                dependencies.add(match_import.group(1))

    if dependencies:
        deps_str = ", ".join(sorted(dependencies))
    else:
        deps_str = "[None detected; please edit]"

    return deps_str, purpose

def add_header_to_file(file_path):
    # Read the original content
    with open(file_path, 'r') as f:
        content = f.read()

    # Skip if header already present (simple check)
    if content.startswith("#!/usr/bin/env python3") and 'Author:' in content:
        print(f"Skipping {file_path}: header exists")
        return

    deps, purpose = detect_dependencies_and_purpose(file_path)
    script_name = os.path.basename(file_path)
    usage = "[--args]"  # Placeholder; user can adjust

    header = header_template.format(
        date=today,
        purpose=purpose,
        script_name=script_name,
        usage=usage,
        dependencies=deps
    )

    new_content = header + "\n" + content

    # Write back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f"Updated header in {file_path}")

if __name__ == "__main__":
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fname in filenames:
            if fname.endswith('.py') and fname != os.path.basename(__file__):
                file_path = os.path.join(dirpath, fname)
                add_header_to_file(file_path)

