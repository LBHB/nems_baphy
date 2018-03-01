import nems_baphy.db as nd
import nems_baphy.utilities.baphy as baphy


def list_recordings(batch):
    ''' 
    Returns a list of all cellids for a given batch.
    '''
    cell_data = nd.get_batch_cells(batch=batch)
    cellids = list(cell_data['cellid'].unique())
    return cellids


def load_recording_from_baphy(batch, cellid, **options):
    '''
    Returns a recording object loaded from Baphy.
    '''
    if batch in [271]:
        return _load_from_271(cellid, **options)
    else:
        raise NotImplementedError


def _load_from_271(cellid,
                   rasterfs=100,
                   chancount=18,
                   includeprestim=True,
                   pupil=False,
                   stimfmt='ozgf',
                   stim=True):
    '''
    Returns a Recording loaded from a cell in batch 271.
    '''
    batch = 271
    stimfmt = stimfmt if stim else 'none'
    options = {'rasterfs': rasterfs,
               'chancount': chancount,
               'stimfmt': stimfmt,
               'includeprestim': includeprestim,
               'pupil': pupil,
               'stim': stim}
    recording = baphy.baphy_load_recording(cellid, batch, options)
    return recording

def test_load_recording_from_baphy():

    rec = load_recording_from_baphy(batch=271, cellid='bbl086b-23-1')
    print(rec)
    
    # # TODO: Recording should contain more info
    # save_path="/auto/data/tmp/batch{0}_fs{1}_{2}{3}/".format(batch, 
    #                                                          rasterfs,
    #                                                          stimfmt,
    #                                                          chancount])

    # recording.save(save_path)

test_load_recording_from_baphy()
