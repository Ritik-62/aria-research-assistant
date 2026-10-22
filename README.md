# ARIA
## Academic Research & Innovation Assistant

An evidence-grounded research assistant for literature
discovery, research gap analysis, and citation-grounded
report generation.

## Run locally

Activate the virtual environment and run:

    python app.py



## Current Features

- Structured research-plan generation
- Research-question input validation
- Suggested scholarly search queries
- Inclusion and exclusion criteria
- Expected research outputs
- Automated unit tests

## Run Tests

    python -m unittest -v test_research_planner.py

## Run ARIA

    python app.py



## Paper normalization and deduplication

ARIA converts paper records into a consistent structure
containing:

- Paper ID
- Title
- Authors
- Publication year
- Abstract
- Source
- URL

Duplicate records are detected using paper identifiers
and normalized titles. When possible, missing metadata
is filled from duplicate records.

## Run tests

```bash
python -m unittest -v
```
