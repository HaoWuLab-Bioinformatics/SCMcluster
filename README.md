# SCMcluster
SCMcluster is an ensemble clustering algorithm for single-cell RNA sequencing data.

## Introduction
This algorithm integrates two cell marker databases(CellMarker database and PanglaoDB database)with scRNA-seq data for feature extraction, and constructs an ensemble clustering model(including SNN-Cliq and SOM) based on the consensus matrix.

## Overview
The baron in the data folder contains the demo dataset Baron, where "baron_mouse_log" is the log-normalized dataset, "after_selection_baron" is the feature extraction dataset, and "baron_labels" is the label dataset. The marker folder contains the marker data merged from the marker database.    
The SOM_CLUST.py file is used to perform SOM clustering. The topology of the competition layer of this method supports both one-dimensional and two-dimensional.          
The SNN_Cliq.py file is used to perform SNN construction and Cliq merging. The input to this method is a similarity matrix.     
The feature_selection.py file is used to integrate marker genes for feature extraction.            
The SCMcluster.py file is used to perform ensemble clustering. This method needs to input the expression matrix after feature selection.         
The lable_transform.py file is used for label transformation of the reference dataset. This method converts the tag file into a tag list to calculate the accuracy.             

## Dependency
python 3.6    
numpy 1.19  
scikit-learn 0.24   
pandas 0.23   
tensorflow 1.12 

## Usage
