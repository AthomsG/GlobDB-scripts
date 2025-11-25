# GlobDB KO Gene Finder & Sequence Extractor

Find genes with specific KEGG KO annotations in GlobDB and extract their **protein sequences**.

## About GlobDB

GlobDB is a dereplicated database of 306,260 species-representative microbial genomes from 14 major genome resources (GTDB, mOTUs, SPIRE, MGnify, etc.). All genomes are annotated with KEGG, COG, and Pfam. More info [here](https://www.globdb.org).

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# 1. Find genes for a KO
python find_globdb_ko_genes.py --ko K00954

# 2. Extract protein sequences
python extract_ko_sequences.py --ko K00954 --hits-tsv outputs/K00954/K00954_hits.tsv
```

## Output

- `outputs/K00954/K00954_hits.tsv` - Gene IDs and metadata
- `outputs/K00954/K00954_all_sequences.faa` - Protein sequences

## Configuration

**GlobDB Path**: Edit `LOCAL_GLOBDB_PATH` in both scripts if the mirror location changes:
```python
LOCAL_GLOBDB_PATH = "/lisc/opt/mirror/globdb/r226"
```