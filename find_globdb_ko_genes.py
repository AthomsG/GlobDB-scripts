#!/usr/bin/env python3
"""
Scan GlobDB KEGG annotations and list all genes annotated with a given KO term.

Output: a TSV file with genome_id, gene_id, ko, description, e_value
"""

import argparse
import os
import sys

from src.kegg_scanner import scan_kegg_for_ko

# Global path to local GlobDB mirror
LOCAL_GLOBDB_PATH = "/lisc/opt/mirror/globdb/r226"


def main():
    DEFAULT_OUTDIR = "outputs"
    DEFAULT_KO = "K00954"

    parser = argparse.ArgumentParser(
        description="Find genes annotated with a KEGG KO in GlobDB"
    )
    parser.add_argument("--ko", default=DEFAULT_KO, help=f"KO term (default: {DEFAULT_KO})")
    parser.add_argument("--outdir", default=DEFAULT_OUTDIR, help=f"Output directory (default: {DEFAULT_OUTDIR})")

    args = parser.parse_args()

    local_kegg_file = os.path.join(
        LOCAL_GLOBDB_PATH, "combined_files", "globdb_r226_kegg_all.gz"
    )
    if not os.path.exists(local_kegg_file):
        print(f"[ERROR] Local GlobDB KEGG file not found: {local_kegg_file}")
        sys.exit(1)

    print(f"[INFO] Using local GlobDB: {local_kegg_file}")

    ko_dir = os.path.join(args.outdir, args.ko)
    os.makedirs(ko_dir, exist_ok=True)
    
    out_tsv = os.path.join(ko_dir, f"{args.ko}_hits.tsv")

    scan_kegg_for_ko(local_kegg_file, args.ko, out_tsv)


if __name__ == "__main__":
    main()