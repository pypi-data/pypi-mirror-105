import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score


def plot(X, n_clusters, scatter=True, columns=[0, 1]):
    """
    Function plots silhouette plots for all different number of clusters given to it.

    :param X: Pandas DataFrame of n features
    :param n_clusters: List of number of clusters to form using KMeans
    :param scatter: bool - To display scatter plot or not. Default is True
    :param columns: List of column index to consider of scatter plot, Default is [0,1]
    :return: Plots silhouette plots for given number of clusters
    """
    if scatter:
        if X.shape[1] == 1:
            columns = [0, 0]

        try:
            if X[:, columns[0]].all() and X[:, columns[1]].all():
                pass
        except IndexError:
            raise

    for n in n_clusters:
        if scatter:
            # Create a subplot with 1 row and 2 columns
            fig, (ax1, ax2) = plt.subplots(1, 2)
        else:
            # Create a subplot with 1 row and 1 columns
            fig, ax1 = plt.subplots(1, 1)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.1, 1])

        # The (n+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n + 1) * 10])

        # Initialize the cluster with n value and a random generator
        # seed of 10 for reproducibility.
        cluster = KMeans(n_clusters=n, random_state=10)
        cluster_labels = cluster.fit_predict(X)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(n):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        # Clear the yaxis labels / ticks
        ax1.set_yticks([])
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        if scatter:
            # 2nd Plot showing the actual clusters formed
            colors = cm.nipy_spectral(cluster_labels.astype(float) / n)
            ax2.scatter(X[:, columns[0]], X[:, columns[1]], marker='.', s=30, lw=0, alpha=0.7,
                        c=colors, edgecolor='k')

            # Labeling the clusters
            centers = cluster.cluster_centers_
            # Draw white circles at cluster centers
            ax2.scatter(centers[:, columns[0]], centers[:, columns[1]], marker='o',
                        c="white", alpha=1, s=200, edgecolor='k')

            for i, c in enumerate(centers):
                ax2.scatter(c[columns[0]], c[columns[1]], marker='$%d$' % i, alpha=1,
                            s=50, edgecolor='k')

            ax2.set_title("The Visualization of the Clustered Data.")
            ax2.set_xlabel("Feature space for the 1st feature (X[:,%d])" % (columns[0]))
            ax2.set_ylabel("Feature space for the 2nd feature (X[:,%d])" % (columns[1]))

        plt.suptitle(("Silhouette analysis for KMeans clustering with clusters = %d "
                      "\n Average Silhouette Score= %f" % (n, silhouette_avg)),
                     fontsize=14, fontweight='bold')

    plt.show()
