#!/bin/bash
set -euo pipefail

# Load MMseqs2 module (latest version: https://wiki.lisc.univie.ac.at/software/programs/catalog/mmseqs2)
module load MMseqs2/18-8cc5c-gompi-2025b

# Config
FASTA_FILE="outputs/K00954/K00954_all_sequences.faa" # Change Manually
N_SEQS=242308   # All sequences (run to count): wc -l K00954_all_sequences.faa | awk '{print $1/2}'
MIN_SEQ_ID=0.5  # 50% identity (because we only care about the bits for the primer)
COVERAGE=0.8    # 80% coverage
SENSITIVITY=5.7 # Default sensitivity (fast, good for orthologs according to chatgpt)
OUTPUT_DIR="cluster_output"
OUTPUT_PREFIX="${OUTPUT_DIR}/K00954_clustered"

mkdir -p "$OUTPUT_DIR"

echo "[INFO] Extracting first ${N_SEQS} sequences..."
awk -v n="$N_SEQS" '/^>/ {if (count >= n) exit; count++} {print}' "$FASTA_FILE" > "${OUTPUT_PREFIX}_subset.faa"

ACTUAL_SEQS=$(grep -c "^>" "${OUTPUT_PREFIX}_subset.faa")
echo "[INFO] Extracted ${ACTUAL_SEQS} complete sequences"

echo "[INFO] Clustering at ${MIN_SEQ_ID} identity, ${COVERAGE} coverage, sensitivity ${SENSITIVITY}..."
mmseqs easy-cluster \
    "${OUTPUT_PREFIX}_subset.faa" \
    "$OUTPUT_PREFIX" \
    "${OUTPUT_DIR}/tmp" \
    --min-seq-id "$MIN_SEQ_ID" \
    -c "$COVERAGE" \
    --cov-mode 0 \
    -s "$SENSITIVITY" \
    --threads 40

N_CLUSTERS=$(cut -f1 "${OUTPUT_PREFIX}_cluster.tsv" | sort -u | wc -l)
echo "[INFO] Reduced ${ACTUAL_SEQS} sequences to ${N_CLUSTERS} clusters"
echo "[INFO] Reduction: $(echo "scale=1; 100 * $N_CLUSTERS / $ACTUAL_SEQS" | bc)% remaining"
echo "[INFO] Output directory: ${OUTPUT_DIR}/"
echo "[INFO] Representatives: ${OUTPUT_PREFIX}_rep_seq.fasta"
echo "[INFO] Assignments: ${OUTPUT_PREFIX}_cluster.tsv"