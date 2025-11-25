#!/bin/bash

set -e

echo "=== Détection du système ==="
OS=$(uname -s)
ARCH=$(uname -m)

echo "OS : $OS"
echo "Architecture : $ARCH"

# Vérifier si conda est déjà installé
if command -v conda >/dev/null 2>&1; then
    echo "Conda est déjà installé : $(conda --version)"
else
    echo "Conda non trouvé, installation nécessaire."

    INSTALLER=""

    echo "=== Sélection de l'installateur Conda ==="
    if [[ "$OS" == "Linux" ]]; then
        if [[ "$ARCH" == "x86_64" ]]; then
            INSTALLER="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        elif [[ "$ARCH" == "aarch64" ]]; then
            INSTALLER="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh"
        else
            echo "Architecture Linux non prise en charge."
            exit 1
        fi
    elif [[ "$OS" == "Darwin" ]]; then
        if [[ "$ARCH" == "x86_64" ]]; then
            INSTALLER="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
        elif [[ "$ARCH" == "arm64" ]]; then
            INSTALLER="https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-arm64.sh"
        else
            echo "Architecture macOS non prise en charge."
            exit 1
        fi
    else
        echo "OS non supporté automatiquement."
        exit 1
    fi

    echo "Téléchargement de l'installateur Conda : $INSTALLER"
    curl -L -o installer.sh "$INSTALLER"

    echo "=== Installation de Conda ==="
    bash installer.sh -b -p "$HOME/miniconda"

    echo "Initialisation de conda"
    source "$HOME/miniconda/etc/profile.d/conda.sh"
    conda init

    # Recharger le shell
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
fi

echo "=== Conda prêt ==="
conda --version

echo "=== Ajout des canaux bioconda / conda-forge ==="
conda config --add channels defaults || true
conda config --add channels bioconda || true
conda config --add channels conda-forge || true

echo "=== Installation de SRA Toolkit ==="
conda install -y sra-tools

echo "=== Vérification de SRA Toolkit ==="
if command -v fasterq-dump >/dev/null 2>&1; then
    echo "SRA Toolkit installé avec succès !"
    fasterq-dump --version
else
    echo "Échec de l'installation du SRA Toolkit."
    exit 1
fi


