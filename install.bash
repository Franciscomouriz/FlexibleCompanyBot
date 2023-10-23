#!/bin/bash
set -e

# Create conda environment
echo 'Creating conda environment...'
conda create --name FlexibleCompanyBot python=3.9 || { echo 'Failed to create conda environment'; exit 1; }

# Save variables
conda_path=$(conda env list | grep "^FlexibleCompanyBot " | awk '{print $2}') || { echo 'Failed to fetch conda path'; exit 1; }
echo "conda_path: $conda_path"
program_path=$(pwd) || { echo 'Failed to fetch program path'; exit 1; }

# Activate conda environment
echo 'Source your shell to use the conda environment...'
source "$(conda info --base)/etc/profile.d/conda.sh"
echo 'Activating conda environment...'
conda activate FlexibleCompanyBot || { echo 'Failed to activate conda environment'; exit 1; }

# Install pip
echo 'Installing pip...'
conda install pip || { echo 'Failed to install pip'; exit 1; }

# Install poetry
echo 'Installing poetry...'
$conda_path/bin/pip install "poetry-core>=1.1.0a6" "poetry>=1.2.0b3" || { echo 'Failed to install poetry'; exit 1; }

# Install pygaggle
echo 'Installing pygaggle...'
cd "$conda_path/lib/python3.9/site-packages/" || { echo 'Failed to change directory'; exit 1; }
rm -rf pygaggle && $conda_path/bin/pip uninstall -y pygaggle || { echo 'Failed to remove and uninstall pygaggle';}
git clone  --recursive https://github.com/castorini/pygaggle.git || { echo 'Failed to clone pygaggle'; exit 1; }
cd pygaggle || { echo 'Failed to change directory'; exit 1; }
$conda_path/bin/pip install install --editable . || { echo 'Failed to install pygaggle'; exit 1; }

# Install packages
echo 'Installing packages...'
cd "$program_path" || { echo 'Failed to change directory'; exit 1; }
poetry install || { echo 'Failed to install packages'; exit 1; }

# Install grobid
echo 'Installing grobid...'
cd "$program_path" || { echo 'Failed to change directory'; exit 1; }
wget https://github.com/kermitt2/grobid/archive/0.7.2.zip
unzip 0.7.2.zip
rm 0.7.2.zip
cd grobid-0.7.2 || { echo 'Failed to change directory'; exit 1; }
./gradlew clean install || { echo 'Failed to install grobid'; exit 1; }