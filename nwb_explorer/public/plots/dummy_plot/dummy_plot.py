import holoviews as hv
 
def plot(nwbfile):

        data = nwbfile.stimulus['locally_sparse_noise_4deg'].indexed_timeseries.data.value
        dictionary = {ii:hv.Image(data[ii,:,:]) for ii in range(5)}
        return hv.HoloMap(dictionary, kdims='ii')
