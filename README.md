# SCMcluster
SCMcluster is an ensemble clustering algorithm for single-cell RNA sequencing data.

## Introduction
This algorithm integrates two cell marker databases(CellMarker database and PanglaoDB database)with scRNA-seq data for feature extraction, and constructs an ensemble clustering model(including SNN-Cliq and SOM) based on the consensus matrix.

## Overview
The file SOM_CLUST.py contains SOM algorithm. You can use this method by:
'SOM_CLUST.CyrusSOM()'
