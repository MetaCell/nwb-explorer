import React from 'react';
import Button from '@material-ui/core/Button';

const SAMPLE_LINK_FERGUSON = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb';
const SAMPLE_LINK_FERGUSON_2 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR2.nwb';
const SAMPLE_LINK_FERGUSON_3 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR3.nwb';
const SAMPLE_LINK_FERGUSON_4 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR4.nwb';
const SAMPLE_LINK_FERGUSON_5 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR5_rebound.nwb';

const SAMPLE_LINK_TIMESERIES = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb';
const SAMPLE_LINK_TRIPLETT = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/TriplettEtAl2018/TriplettEtAl2018.nwb';
const SAMPLE_LINK_LANTYER = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018.170502_AL_257_CC.nwb';
const SAMPLE_LINK_LANORE = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/IgorPro/141210c3.nwb';
const SAMPLE_LINK_PACKER = 'https://github.com/OpenSourceBrain/CalciumImagingDriftingGrating/raw/master/neurofinder.01.01.jpg.nwb';

export default class FileSampleSelector extends React.Component {

  constructor (props) {
    super(props);
    this.handleClickLoadFile = this.handleClickLoadFile.bind(this);

    this.state = {};
  } 

  componentDidMount (prevProps, prevState) {
    console.log("Props in FileSampleSelector", this.props);
  }
  componentDidUpdate (prevProps, prevState) {
    console.log("Props in FileSampleSelector", this.props);
  }
  handleClickLoadFile (url) {
    const { loadNWBFile } = this.props;
    loadNWBFile(url);
  }
  render () {
    

    return (
      <div >
        <h2>Don't have a file to load?</h2>
        <p>Pick a sample and get started!</p>
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_TIMESERIES)}
          disabled={false}
          
        >
          Simple time series
        </Button>
        <br />
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_FERGUSON)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          Ferguson et al. 2015
        </Button> 
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_FERGUSON_2)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          2
        </Button> 
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_FERGUSON_3)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          3
        </Button> 
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_FERGUSON_4)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          4
        </Button> 
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_FERGUSON_5)}
          disabled={false}
        >
          5
        </Button>
        <br />
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_TRIPLETT)}
          disabled={false}
        >
          Triplett et al. 2018 
        </Button>
        <br />
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_LANTYER)}
          disabled={false}
        >
          Lantyer et al. 2018 
        </Button>
        <br />
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_LANORE)}
          disabled={false}
        >
          Lanore et al. 2019 
        </Button>
        <br />
        <Button
          id="loadFile"
          variant="outlined"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_PACKER)}
          disabled={false}
        >
          Packer et al. 2015 
        </Button>
      </div>


    );
  }
}
