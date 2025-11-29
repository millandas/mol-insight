import pandas as pd
import re

# ---------- CONFIG ----------
EXPR_FILE = "/Users/millan/Desktop/AMARCHs3/AMARCHs3/OmicsExpressionTPMLogp1HumanAllGenes.csv"
HGNC_FILE = "/Users/millan/Desktop/AMARCHs3/AMARCHs3/HGNC.txt"   # your new HGNC export
OUTPUT_FILE = "Expression_TPMLogp1_ProteinCodingOnly.csv"

# Adjust if your metadata columns are named differently
META_COLS = ["SequencingID", "ModelID",'IsDefaultEntryForModel','ModelConditionID','IsDefaultEntryForMC']
# ----------------------------


def parse_gene(col_name: str):
    """
    Parse a gene column name into:
    - symbol (str or None)
    - entrez_id (str or None)
    - ensembl_id (str or None)

    Examples:
      "TSPAN6 (7105)"            -> ("TSPAN6", "7105", None)
      "ENSG00000002586.20_PAR_Y" -> (None, None, "ENSG00000002586")
      "TP53"                     -> ("TP53", None, None)
    """
    # Case 1: SYMBOL (ENTREZ_ID)
    m = re.match(r'^(.+?) \((\d+)\)$', col_name)
    if m:
        symbol = m.group(1)
        entrez = m.group(2)
        return symbol, entrez, None

    # Case 2: Ensembl gene ID (possibly with version/suffix)
    if col_name.startswith("ENSG"):
        m = re.match(r"(ENSG[0-9]+)", col_name)
        if m:
            ensg = m.group(1)
            return None, None, ensg

    # Fallback: treat as symbol-only
    return col_name, None, None


def main():
    print("Loading expression matrix...")
    expr = pd.read_csv(EXPR_FILE)

    # Identify gene columns (everything after metadata)
    gene_cols = expr.columns[len(META_COLS):]
    print(f"Total gene columns: {len(gene_cols):,}")

    print("Loading HGNC table...")
    # Your HGNC file is tab-separated
    hgnc = pd.read_csv(HGNC_FILE, sep="\t")

    required_cols = ["NCBI Gene ID", "Ensembl gene ID", "Locus group"]
    for c in required_cols:
        if c not in hgnc.columns:
            raise ValueError(f"HGNC file is missing required column: {c}")

    # Keep only protein-coding genes
    pc_mask = hgnc["Locus group"] == "protein-coding gene"

    # Protein-coding Entrez/NCBI IDs as strings
    pc_entrez = (
        hgnc.loc[pc_mask, "NCBI Gene ID"]
        .dropna()
        .astype(int)   # sometimes floats like 7105.0
        .astype(str)
    )
    pc_entrez = set(pc_entrez)

    # Protein-coding Ensembl IDs
    pc_ensg = set(
        hgnc.loc[pc_mask, "Ensembl gene ID"].dropna()
    )

    print(f"Protein-coding NCBI Gene IDs:  {len(pc_entrez):,}")
    print(f"Protein-coding Ensembl IDs:    {len(pc_ensg):,}")

    # Decide which gene columns to keep
    pc_gene_cols = []
    for col in gene_cols:
        symbol, entrez, ensg = parse_gene(col)

        keep = False
        if entrez is not None and entrez in pc_entrez:
            keep = True
        elif ensg is not None and ensg in pc_ensg:
            keep = True

        if keep:
            pc_gene_cols.append(col)

    print(f"Protein-coding gene columns kept: {len(pc_gene_cols):,}")

    # Build final matrix: metadata + protein-coding gene columns
    expr_pc = expr[META_COLS + pc_gene_cols]

    print("Saving filtered matrix to:", OUTPUT_FILE)
    expr_pc.to_csv(OUTPUT_FILE, index=False)
    print("Done.")
    print("Final shape (rows, cols):", expr_pc.shape)


if __name__ == "__main__":
    main()
