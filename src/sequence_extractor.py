"""
Helper functions for extracting protein sequences from FASTA files.
"""

import os
import gzip
from collections import defaultdict
from typing import Dict, Set
from tqdm import tqdm


def find_genome_fasta(protein_dir: str, genome_id: str) -> str:
    """Find the FASTA file for a genome in the chunk directories."""
    for chunk in os.listdir(protein_dir):
        if not chunk.startswith("R226CHUNK"):
            continue
        chunk_dir = os.path.join(protein_dir, chunk)
        fasta_path = os.path.join(chunk_dir, f"{genome_id}.faa.gz")
        if os.path.exists(fasta_path):
            return fasta_path
    return None


def extract_gene_sequence(fasta_path: str, gene_id: str) -> tuple:
    """
    Extract a single gene sequence from FASTA file.
    Returns (header, sequence) or (None, None) if not found.
    """
    with gzip.open(fasta_path, 'rt') as f:
        current_header = None
        current_seq = []
        
        for line in f:
            if line.startswith('>'):
                # Check if previous sequence matches
                if current_header:
                    seq_id = current_header[1:].split()[0]
                    if seq_id == gene_id:
                        return current_header, ''.join(current_seq)
                
                current_header = line.rstrip()
                current_seq = []
            else:
                current_seq.append(line.rstrip())
        
        # Check last sequence
        if current_header:
            seq_id = current_header[1:].split()[0]
            if seq_id == gene_id:
                return current_header, ''.join(current_seq)
    
    return None, None


def parse_hits_tsv(tsv_path: str, ko: str) -> Dict[str, Set[str]]:
    """Parse KO hits TSV and return {genome_id: {gene_id1, gene_id2, ...}}."""
    genome_genes = defaultdict(set)
    
    print(f"[INFO] Parsing hits TSV: {tsv_path}")
    with open(tsv_path, 'r') as f:
        next(f)  # Skip header
        for line in tqdm(f, desc="Reading hits", unit=" lines"):
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            genome_id, gene_id = parts[0], parts[1]
            genome_genes[genome_id].add(gene_id)
    
    return genome_genes


def extract_all_ko_sequences(
    protein_dir: str,
    genome_genes: Dict[str, Set[str]],
    ko: str,
    outdir: str
) -> None:
    """Extract all sequences for a KO into a single combined FASTA file."""
    print(f"[INFO] Extracting sequences for KO: {ko}")
    
    ko_dir = os.path.join(outdir, ko)
    os.makedirs(ko_dir, exist_ok=True)
    
    output_file = os.path.join(ko_dir, f"{ko}_all_sequences.faa")
    
    total_genes = sum(len(genes) for genes in genome_genes.values())
    print(f"[INFO] {len(genome_genes)} genomes, {total_genes} genes total")
    
    extracted = 0
    
    with open(output_file, 'w') as out:
        for genome_id in tqdm(sorted(genome_genes.keys()), desc=f"Extracting {ko}", unit=" genome"):
            gene_ids = genome_genes[genome_id]
            
            # Find FASTA file for this genome
            fasta_path = find_genome_fasta(protein_dir, genome_id)
            if not fasta_path:
                tqdm.write(f"[WARN] FASTA not found for genome: {genome_id}")
                continue
            
            # Extract each gene
            for gene_id in gene_ids:
                try:
                    header, sequence = extract_gene_sequence(fasta_path, gene_id)
                    if header and sequence:
                        out.write(f"{header}\n{sequence}\n")
                        extracted += 1
                except Exception as e:
                    tqdm.write(f"[WARN] {gene_id}: {e}")
    
    print(f"[INFO] Extracted {extracted}/{total_genes} sequences")
    print(f"[INFO] Saved to: {output_file}")