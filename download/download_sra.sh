#!/bin/bash
#samle SRR26754803     
# Vérifier qu'un identifiant SRA est donné
if [ -z "$1" ]; then
    echo "Usage : $0 <SRR_ID> [dossier_sortie]"
    exit 1
fi

SRR=$1
OUTDIR=${2:-fastq}

echo "Téléchargement de $SRR..."
prefetch $SRR

echo "Conversion en FASTQ..."
mkdir -p $OUTDIR
fasterq-dump --split-files --outdir $OUTDIR $SRR

echo "Terminé ! Les fichiers sont dans : $OUTDIR"

