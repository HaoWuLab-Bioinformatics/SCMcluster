# SCMcluster
SCMcluster is an ensemble clustering algorithm for single-cell RNA sequencing data.

## Introduction
This algorithm integrates two cell marker databases(CellMarker database and PanglaoDB database)with scRNA-seq data for feature extraction, and constructs an ensemble clustering model(including SNN-Cliq and SOM) based on the consensus matrix.

## Overview
The file SOM_CLUST.py contains SOM algorithm. You can use this method by:

` SOM_CLUST.CyrusSOM() `

The file SNN_cliq.py contains SNN_cliq algorithm. You can use this method by:

## Dependency
python 3.6

numpy 1.19

scikit-learn 0.24

pandas 0.23

tensorflow 1.12

## Usage
