import sys
import pynwb
from pynwb import NWBHDF5IO

print("NWB file to be examined:", str(sys.argv[1]))

nwb_file=sys.argv[1]

metadata_list = ['institution', 'lab', 'experimenter', 'experiment_description','modules', 'acquisition']

io = NWBHDF5IO(nwb_file, mode="r")
nwbfile = io.read()

# get pynwb info
notes = getattr(nwbfile,'notes')
# if field is not None
if bool(notes):
    # print file's pynwb info
    print('Info:"\t %s' % (notes))
    # print explorer's pynwb info
    print('pynwb version: %s' % (pynwb.__version__))
    # split notes to get pynwb ver elements
    notes_str = notes.split()
    # get file's pynwb version to match with explorer's version
    pynwb_file_ver = notes_str[notes_str.index('pynwb')+1]
    pynwb_explorer_ver = 'v'+str(pynwb.__version__)
    if pynwb_file_ver == pynwb_explorer_ver:
        print('pynwb versions match')
    else:
        print('pynbw versions do not match - potential file loading failure')
else:
    print('no information on pynwb version')

# print other information
for meta_ind in metadata_list:
    # get attribute from nwbfile
    metadata = getattr(nwbfile,meta_ind)
    if bool(metadata):
        # get number of acquisition timeseries
        if meta_ind =='acquisition':
            print('MetaField acquisition number:\t %s' % (len(metadata)))
        else:
            print('MetaField %s:\t %s' % (meta_ind,metadata))
