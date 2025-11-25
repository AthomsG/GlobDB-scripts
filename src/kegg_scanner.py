"""
KEGG annotation scanning functionality for finding KO-annotated genes.
"""

import gzip
from tqdm import tqdm


def scan_kegg_for_ko(tar_path: str, ko_of_interest: str, out_tsv_path: str) -> None:
    """Scan KEGG annotation file for genes with a specific KO."""
    print(f"[INFO] Scanning for KO: {ko_of_interest}")
    print(f"[INFO] Reading: {tar_path}")

    hit_count = 0
    line_count = 0
    
    with gzip.open(tar_path, "rt") as f, open(out_tsv_path, "w") as out:
        out.write("genome_id\tgene_id\te_value\n")

        pbar = tqdm(desc="Scanning", unit=" lines", unit_scale=True)
        for line in f:
            line_count += 1
            pbar.update(1)
            
            parts = line.strip().split("\t")
            if len(parts) < 5:
                continue

            gene_id, source, ko, description, e_value = parts[:5]

            if ko == ko_of_interest:
                genome_id = gene_id.rsplit("___", 1)[0] if "___" in gene_id else gene_id
                out.write(f"{genome_id}\t{gene_id}\t{e_value}\n")
                hit_count += 1
                
                if hit_count % 100 == 0:
                    pbar.set_postfix({"hits": hit_count})
        
        pbar.close()

    print(f"\n[INFO] Scanned {line_count:,} lines")
    print(f"[INFO] Found {hit_count} hits")
    print(f"[INFO] Saved to: {out_tsv_path}")