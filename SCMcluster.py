import sklearn.cluster
import numpy as np
import SNN_Cliq
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import SpectralClustering
from sklearn.feature_selection import VarianceThreshold
import SOM_CLUST
import argparse
import sys

def variance_select(Cmatrix, p):
    selector = VarianceThreshold(p)
    after_data = selector.fit_transform(Cmatrix)
    return after_data

def co_clust(dmat, data, n_clusters):
    n = []
    for i in range(n_clusters):
        n.append(1)
    estimators = [
        SNN_Cliq,
        SOM_CLUST.CyrusSOM(net=n, epochs=25)
    ]

    # Declare the weight of each vote
    vote = 1 / len(estimators)
    # (n,m)=data.T.shape
    (n, m) = data.shape
    #print(n)
    # co_association matrix is 5X5 (5 patterns)
    co_association = np.zeros((n, n))
    #print(co_association)

    # for each of your estimators
    for est in estimators:
        # fit the data and grab the labels
        if est == SNN_Cliq:
            print("snn")
            labels = SNN_Cliq.snn_cliq(dmat, 0.5, 0.7, n_clusters)
        #         print(len(labels))
        #         ari = metrics.adjusted_rand_score(lable_transform.lable, labels)
        #         NMI = metrics.adjusted_mutual_info_score(lable_transform.lable, labels)
        #         print('ari:', ari)
        #         print('NMI:', NMI)

        else:
            print("other")
            labels = est.transform_fit(data)

        # find all associations and transform it into a numpy array
        res = [[int(i == j) for i in labels] for j in labels]
        res = np.array(res)
        #print("vote", vote)
        #print("res", res)
        # Vote and update the co_association matriz
        res = res * vote
        co_association = co_association + res
        #print(co_association)
    return co_association

def main_run(data_path, out_clusters, k_clusters):
    """
    Parameters
    ----------
    data_path: Path to matrix generated from feature_selection.py
    out_clusters: Path to output clusters
    Returns
    -------
    """
    d = pd.read_csv(data_path, index_col=0, sep='\t')
    data = d.values.T
    print(data.shape)
    a = variance_select(data, 0.03)
    print(a.shape)
    dmat = euclidean_distances(variance_select(data, 0.03))
    print(dmat.shape)
    n_clusters = k_clusters
    # co--
    co = co_clust(dmat, data, int(n_clusters))
    print(co.shape)
    pre_labels = list(
        SpectralClustering(n_clusters=int(n_clusters), affinity='precomputed', assign_labels='discretize').fit_predict(
            co))  #discretize/kmeans,‘nearest_neighbors
    print(pre_labels)
    labels = pd.DataFrame(pre_labels)
    labels.columns = ['cluster_label']
    labels.to_csv(out_clusters, index=None)

def parse(args=None):
    '''arguments.
    '''
    parser = argparse.ArgumentParser(prog='SCMclsuter main',
                                     description='Clustering using SCMclsuter. doi: 10.1093/bfgp/elad004',
                                     epilog='(c) authors')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + '1',
                        help="Show program's version number and exit.")
    parser.add_argument('-m', '--mat_file', type=str, help='Path to the input matrix')
    parser.add_argument('-o', '--out_file', type=str, help='Path to the output matrix')
    parser.add_argument('-k', '--cluster', type=str, help='Number of clusters')

    args_parsed = parser.parse_args(args)
    return args_parsed

if __name__ == "__main__":

    args = parse(sys.argv[1:])
    if args.mat_file and args.out_file and args.cluster:
        print('Matrix have been submitted...')
        main_run(args.mat_file, args.out_file, args.cluster)
        print('Labels have been returned...')


