import React from 'react';
import { Box, Button, Typography, FormControl, Select, MenuItem } from '@material-ui/core';


const SAMPLE_LINK_FERGUSON = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb';
const SAMPLE_LINK_FERGUSON_2 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR2.nwb';
const SAMPLE_LINK_FERGUSON_3 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR3.nwb';
const SAMPLE_LINK_FERGUSON_4 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR4.nwb';
const SAMPLE_LINK_FERGUSON_5 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR5_rebound.nwb';

const SAMPLE_LINK_TIMESERIES = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb';
const SAMPLE_LINK_TRIPLETT = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/TriplettEtAl2018/TriplettEtAl2018.nwb';
const SAMPLE_LINK_LANTYER = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_170502_AL_257_CC.nwb';
const SAMPLE_LINK_LANORE = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/IgorPro/141210c3.nwb';
const SAMPLE_LINK_PACKER = 'https://github.com/OpenSourceBrain/CalciumImagingDriftingGrating/raw/master/neurofinder.01.01.jpg.nwb';
const SAMPLE_LINK_KATO = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/KatoEtAl2015/KatoEtAl2018.WT_Stim.6.nwb';

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
  handleChange = e => {
    this.handleClickLoadFile(e.target.value);
  }

  render () {
    return (
      <div >
        <Typography variant="h6">Don’t have a file to load?</Typography>
        <Typography variant="h3">Pick a sample and get started!</Typography>
        <Button
          id="loadFile"
          variant="outlined"
          className="button badge-button"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_TIMESERIES)}
          disabled={false}
        >
          Simple time series
        </Button>

        <Typography variant="h4">Intracellular Electrophysiology:</Typography>
        <Box display="flex" alignItems="flex-start" flexWrap="wrap">
          <FormControl variant="outlined" class="custom-select">
            <Select
              id="samplefile-select"
              value={''}
              onChange={this.handleChange}
              className="button badge-button"
              name="ferguson"
              displayEmpty
              inputProps={{ 'aria-label': 'ferguson' }}
            >
              <MenuItem value="" disabled>
                Ferguson et al. 2015
              </MenuItem>
              <MenuItem value={SAMPLE_LINK_FERGUSON}>Ferguson 1</MenuItem>
              <MenuItem value={SAMPLE_LINK_FERGUSON_2}>Ferguson 2</MenuItem>
              <MenuItem value={SAMPLE_LINK_FERGUSON_3}>Ferguson 3</MenuItem>
              <MenuItem value={SAMPLE_LINK_FERGUSON_4}>Ferguson 4</MenuItem>
              <MenuItem value={SAMPLE_LINK_FERGUSON_5}>Ferguson 5</MenuItem>
            </Select>
          </FormControl>

          <Button
            id="loadFile"
            variant="outlined"
            className="button badge-button"
            onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_LANTYER)}
            disabled={false}
            style={{ marginRight: '0.5em' }}
          >
            Lantyer et al. 2018
          </Button>
          <Button
            id="loadFile"
            variant="outlined"
            className="button badge-button"
            onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_LANORE)}
            disabled={false}
            style={{ marginRight: '0.5em' }}
          >
          Lanore et al. 2019
          </Button>
        </Box>
        <Typography variant="h4">Calcium fluorescence imaging (time series):</Typography>
        <Button
          id="loadFile"
          variant="outlined"
          className="button badge-button"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_TRIPLETT)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          Triplett et al. 2018
        </Button>
        <Button
          id="loadFile"
          variant="outlined"
          className="button badge-button"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_KATO)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          Kato et al. 2015
        </Button>

        <Typography variant="h4">Calcium fluorescence imaging (image series):</Typography>
        <Button
          id="loadFile"
          variant="outlined"
          className="button badge-button"
          onClick={ e => this.handleClickLoadFile(SAMPLE_LINK_PACKER)}
          disabled={false}
          style={{ marginRight: '0.5em' }}
        >
          Packer et al. 2015
        </Button>

      </div>


    );
  }
}
