#!/usr/bin/env python

# export poertry to requirements.txt
echo "exporting...."
poetry export --format requirements.txt > requirements.txt

echo "exporting with development dependencies...."
poetry export --format requirements.txt > requirements_dev.txt --dev

