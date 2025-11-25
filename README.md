# GlobDB Stuff

Find genes with specific KEGG annotations in GlobDB and extract their **protein sequences**.

## About GlobDB

GlobDB is a dereplicated database of LOTS of species-representative microbial genomes. All genomes are annotated with KEGG, COG, and Pfam. More info [here](https://www.globdb.org).

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make bash scripts executable
chmod +x *.sh
```

## Workflow (in order)

### Step 1: Find KEGG genes
```bash
python find_globdb_ko_genes.py --ko K00954
```
Scans GlobDB KEGG annotations and creates `outputs/K00954/K00954_hits.tsv` with columns: `genome_id`, `gene_id`, `e_value`.

### Step 2: Extract protein sequences
```bash
python extract_ko_sequences.py --ko K00954 --hits-tsv outputs/K00954/K00954_hits.tsv
```
Extracts amino acid sequences to `outputs/K00954/K00954_all_sequences.faa`.

### Step 3: Cluster sequences
```bash
cd exploratory-scripts
chmod +x cluster_ko_sequences.sh
./cluster_ko_sequences.sh
```
Clusters genes using MMseqs2. Results in `cluster_output/`.

## Output

- `outputs/K00954/K00954_hits.tsv` - Gene IDs and metadata
- `outputs/K00954/K00954_all_sequences.faa` - Protein sequences
- `cluster_output/K00954_clustered_rep_seq.fasta` - Cluster representatives (if clustered)

## Configuration (for when GlobDB is updated)

**GlobDB Path**: Edit `LOCAL_GLOBDB_PATH` in both scripts if the mirror location changes:
```python
LOCAL_GLOBDB_PATH = "/lisc/opt/mirror/globdb/r226"
```
