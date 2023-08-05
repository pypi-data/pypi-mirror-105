import numpy as np
import matplotlib.pyplot as plt

def plot_embedded(embedded,ax=None,clusters=None,labels=None,cmap=plt.cm.Spectral,**kwargs):
    """
    Helper function to perform 2D or 3D scatter plotting of a set of points that have undergone dimensionality reduction.

    Parameters
    ----------
    embedded : np.array(n,2) or (n,3)
        The embedded numpy array for visualization

    ax : plt.axes, default=None
        The matplotlib axis object that can be supplied to be plotted onto

    clusters : np.array(np.int), default=None
        An optional array of cluster identifiers that will be used to label and colour code the plot

    labels : iterable, default=None
        A python iterable containing labels for each cluster.

    cmap : plt.cm.Colormap, default=plt.cm.Spectral
        The colourmap that will be used during plotting.

    Returns
    -------
    plt.axes
        Either a new axis that has been initialized through the code, or the original axis that was provided with the new plot drawn on.
    """
    dims = embedded.shape[-1]
    assert dims == 2 or dims == 3, "Wrong number of dimensions for embedded plot, must be 2 or 3."
    if ax is None:
        fig = plt.figure(figsize=(16,16))
        if dims == 2:
            ax = fig.add_subplot()
        else:
            ax = fig.add_subplot(projection='3d')

    if clusters is not None:
        unique_labels = set(clusters)
        colors = [cmap(each) for each in np.linspace(0, 1, len(unique_labels))]
        if labels is None:
            labels = list(unique_labels)
        else:
            assert len(labels) == len(unique_labels), "Labels and the number of unique clusters must be equal"
        for k, col in zip(unique_labels, colors):
            if k == -1: # Grey used for noise.
                col = [0.7, 0.7, 0.7, 1]
            idxs = np.where(clusters == k)[0]
            ax.scatter(*[embedded[idxs,x] for x in range(dims)],c=[tuple(col) for x in range(len(idxs))],label=labels[k],**kwargs)

    else:
        ax.scatter(*[embedded[:,x] for x in range(dims)],**kwargs)
    return ax
