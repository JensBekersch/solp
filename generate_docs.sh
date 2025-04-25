#!/bin/bash

echo "📝 Generating documentation files..."

# Fail fast on error
set -e

# Go into script dir and run generators
python3 scripts/generate_architecture_doc.py
python3 scripts/generate_testdoc.py
python3 scripts/generate_readme.py

echo "✅ Done. Documentation updated:"
echo " - README.md"
echo " - ARCHITEKTUR.md"
echo " - TESTDOC.md"
