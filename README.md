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
The lable_transform.py file is used for label transformation of the reference dataset. This method converts the label file into a label list to calculate the accuracy.

Before using feature_selection.py, you must import SOM_CLUST.py and SNN_Cliq.py. If you want to calculate the clustering accuracy, you have to hold the reference labels and transform them using lable_transform.py.

## Dependency
python 3.6    
numpy 1.19  
scikit-learn 0.24   
pandas 0.23   
tensorflow 1.12 

## Usage
Enter the normalized expression matrix into feature_selection.py.You need to enter the matrix path in the following statement: 

` df=pd.read_csv('./yourpath',index_col=0,sep='\t') `
Use the following statement for feature extraction：
` python featrue_selection.py `

When using SCMcluster.py, you need to input the matrix path after feature extraction. Enter the path of your data as above. At the same time, you need to enter the number of clusters according to the prompts.Use the following statement for ensemble clustering：

` python SCMcluster.py `
