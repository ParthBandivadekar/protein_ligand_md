#!/usr/bin/env bash
#
# reorganize_repo.sh
#
# This script reorganizes the “protein_ligand_md” repository into:
#   • docs/01-Basic-MD-Setup/
#   • docs/02-Data-Analysis/
#   • docs/03-Visualization/
#   • docs/04-Troubleshooting/
#   • scripts/cpptraj/
#   • scripts/pymol/
#   • scripts/analysis/
#   • utilities/     (formerly “Common Operations”)
# It creates a new branch, moves files via git mv, and commits the changes.
#

# 1. Ensure we are in the repo root
if [ ! -f "./README.md" ]; then
  echo "ERROR: Please run reorganize_repo.sh from the root of the cloned repository."
  exit 1
fi

# 2. Create and switch to a new branch
BRANCH="reorg/logical-folders"
git checkout -b $BRANCH

# 3. Create new folder structure
mkdir -p docs/01-Basic-MD-Setup
mkdir -p docs/02-Data-Analysis
mkdir -p docs/03-Visualization
mkdir -p docs/04-Troubleshooting

mkdir -p scripts/cpptraj
mkdir -p scripts/pymol
mkdir -p scripts/analysis

mkdir -p utilities

# 4. Move all top-level .md files into docs/ subfolders
# (Adjust file names as they actually appear in your repo)

# --- 4a. Basic MD Setup guides → docs/01-Basic-MD-Setup
if [ -f "Protein Ligand MD.md" ]; then
  git mv "Protein Ligand MD.md" "docs/01-Basic-MD-Setup/Protein_Ligand_MD.md"
fi
if [ -f "Packmol Protein Systems.md" ]; then
  git mv "Packmol Protein Systems.md" "docs/01-Basic-MD-Setup/Packmol_Protein_Systems.md"
fi

# --- 4b. Data-Analysis guides → docs/02-Data-Analysis
if [ -f "PCA + Reweighting.md" ]; then
  git mv "PCA + Reweighting.md" "docs/02-Data-Analysis/PCA_Reweighting.md"
fi
# (If you have more .md files belonging to Data Analysis, add them here)

# --- 4c. Visualization guides → docs/03-Visualization
if [ -f "PyMOL Guide.md" ]; then
  git mv "PyMOL Guide.md" "docs/03-Visualization/PyMOL_Guide.md"
fi
if [ -f "PyMOL Examples.md" ]; then
  git mv "PyMOL Examples.md" "docs/03-Visualization/PyMOL_Examples.md"
fi

# --- 4d. Troubleshooting → docs/04-Troubleshooting
if [ -f "Troubleshooting.md" ]; then
  git mv "Troubleshooting.md" "docs/04-Troubleshooting/Troubleshooting.md"
fi

# 5. Move “Common Operations/” → “utilities/”
if [ -d "Common Operations" ]; then
  # Rename the folder
  git mv "Common Operations" "utilities"
fi

# 6. Move scripts into their respective subfolders
#    – *.sh, *.in (cpptraj workflows) → scripts/cpptraj/
#    – *.pml, PyMOL-based Python scripts → scripts/pymol/
#    – Any other .py for analysis → scripts/analysis/

# 6a. Move all .sh and .in files (except reorganize_repo.sh) into scripts/cpptraj/
find . -maxdepth 1 -type f \( -name "*.sh" -o -name "*.in" \) \
  ! -name "reorganize_repo.sh" \
  -exec bash -c 'for f; do git mv "$f" scripts/cpptraj/; done' bash {} +

# 6b. Move PyMOL scripts (.pml) and any “generate_*_pymol.py” to scripts/pymol
if [ -d "scripts" ]; then
  # (In case you already have a scripts/ folder with mixed content)
  find scripts -maxdepth 1 -type f -name "*.pml" \
    -exec bash -c 'for f; do git mv "$f" scripts/pymol/; done' bash {} +
  # Also move any PyMOL-related .py (you can refine this pattern)
  find scripts -maxdepth 1 -type f -name "*pymol*.py" \
    -exec bash -c 'for f; do git mv "$f" scripts/pymol/; done' bash {} +
fi

# If you had a flat “scripts/” directory with .sh or .py files, move them too
if [ -d "scripts" ]; then
  # Move any remaining .py not already moved → scripts/analysis/
  find scripts -maxdepth 1 -type f -name "*.py" \
    -exec bash -c 'for f; do git mv "$f" scripts/analysis/; done' bash {} +
fi

# (If you had any other leftover top-level .py or .ipynb that belong to analysis,
#  you can add similar find/mv commands here.)

# 7. Move images into an images/ folder if they are not already there
# (Optional: if you want all images under images/, uncomment below)
# mkdir -p images
# find . -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.svg" \) \
#   -exec bash -c 'for f; do git mv "$f" images/; done' bash {} +

# 8. Update README.md to reflect new paths (you may need to edit manually after)
#    At minimum, rename any link targets. The script won’t rewrite the links,
#    but after this commit you can open README.md and change paths from “X.md” to “docs/.../X.md”.

# 9. Commit all changes
git add -A
git commit -m "Reorganize files into logical folders (docs/, scripts/, utilities/)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Done. A new branch '$BRANCH' has been created with your changes."
echo "Review the moved files, update any internal links, then merge into main."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

