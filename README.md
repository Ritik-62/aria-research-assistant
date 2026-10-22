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


## Multi-query research retrieval pipeline

ARIA generates multiple search queries from a research
question and searches each query using the selected
paper-search source.

The retrieval pipeline:
- Collects results from multiple queries
- Continues if an individual query fails
- Normalizes paper metadata into a consistent format
- Deduplicates papers using identifiers and titles
- Reports failed queries and their errors

By default, the pipeline uses offline sample data.

## Run tests

```bash
python -m unittest discover -v
```

## LLM Integration

ARIA includes a provider-independent LLM client foundation.

- Supports injectable generation functions for testing.
- Validates prompts and provider responses.
- Reads the OpenAI API key from environment variables.
- Raises a clear configuration error when the API key is missing.
- Supports unit tests without live API calls or API costs.

### Configuration

Create a local `.env` file with:

    OPENAI_API_KEY=

Keep the key blank until you are ready to configure a real provider. Never commit API keys or other secrets to Git.

The `.env.example` file is a safe configuration template containing placeholder values.

### Run LLM Tests

    python -m unittest test_llm_client -v

### Run All Tests

    python -m unittest discover -v
