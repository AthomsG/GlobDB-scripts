#!/usr/bin/env python3
"""
Extract protein FASTA sequences for genes annotated with specific KO terms.

Reads the output TSV from find_globdb_ko_genes.py and extracts sequences.
"""

import argparse
import os
import sys

from src.sequence_extractor import parse_hits_tsv, extract_all_ko_sequences

# Global path to local GlobDB mirror
LOCAL_GLOBDB_PATH = "/lisc/opt/mirror/globdb/r226"


def main():
    DEFAULT_OUTDIR = "outputs"
    
    parser = argparse.ArgumentParser(description="Extract protein sequences for KO-annotated genes")
    parser.add_argument("--ko", required=True, help="KO term")
    parser.add_argument("--hits-tsv", required=True, help="Path to KO hits TSV")
    parser.add_argument("--outdir", default=DEFAULT_OUTDIR, help=f"Output directory (default: {DEFAULT_OUTDIR})")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.hits_tsv):
        print(f"[ERROR] Hits TSV not found: {args.hits_tsv}")
        print(f"[ERROR] Expected path like: outputs/{args.ko}/{args.ko}_hits.tsv")
        sys.exit(1)
    
    genome_genes = parse_hits_tsv(args.hits_tsv, args.ko)
    
    if not genome_genes:
        print(f"[WARN] No hits found for: {args.ko}")
        sys.exit(0)
    
    print(f"[INFO] Found hits for {args.ko}")
    
    protein_dir = os.path.join(LOCAL_GLOBDB_PATH, "globdb_r226_protein_fasta")
    if not os.path.exists(protein_dir):
        print(f"[ERROR] Local GlobDB not found: {protein_dir}")
        sys.exit(2)
    
    print(f"[INFO] Using local GlobDB: {protein_dir}")
    extract_all_ko_sequences(protein_dir, genome_genes, args.ko, args.outdir)
    
    print("\n[INFO] Done!")


if __name__ == "__main__":
    main()
