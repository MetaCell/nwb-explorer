import React from 'react';
import { Box, Button, Typography, FormControl, Select, MenuItem, Grid, } from '@material-ui/core';

const SAMPLE_LINK_FERGUSON = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb';
const SAMPLE_LINK_FERGUSON_2 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR2.nwb';
const SAMPLE_LINK_FERGUSON_3 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR3.nwb';
const SAMPLE_LINK_FERGUSON_4 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR4.nwb';
const SAMPLE_LINK_FERGUSON_5 = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015_PYR5_rebound.nwb';

const SAMPLE_LINK_TIMESERIES = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb';
const SAMPLE_LINK_TRIPLETT = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/TriplettEtAl2018/TriplettEtAl2018.nwb';

const SAMPLE_LINK_LANORE = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/IgorPro/141210c3.nwb';
const SAMPLE_LINK_PACKER = 'https://github.com/OpenSourceBrain/CalciumImagingDriftingGrating/raw/master/neurofinder.01.01.jpg.nwb';
const SAMPLE_LINK_KATO = 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/KatoEtAl2015/KatoEtAl2018.WT_Stim.6.nwb';

const SAMPLE_LINK_LANTYER = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_170502_AL_257_CC.nwb';
const SAMPLE_LINK_LANTYER_2 = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_170315_AL_216_VC.nwb';
const SAMPLE_LINK_LANTYER_3 = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_170328_AB_277_ST50_C.nwb';
const SAMPLE_LINK_LANTYER_4 = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_170328_AL_238_VC.nwb';
const SAMPLE_LINK_LANTYER_5 = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_171220_NC_156_ST100_C.nwb';
const SAMPLE_LINK_LANTYER_6 = 'https://github.com/vrhaynes/NWBShowcase/raw/master/Lantyer/LantyerEtAl2018_180817_ME_9_CC.nwb';

export default class FileSampleSelector extends React.Component {
  constructor (props) {
    super(props);
    this.handleClickLoadFile = this.handleClickLoadFile.bind(this);

    this.state = {};
  }

  componentDidMount (prevProps, prevState) {
    console.log('Props in FileSampleSelector', this.props);
  }

  componentDidUpdate (prevProps, prevState) {
    console.log('Props in FileSampleSelector', this.props);
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
      <div>
        <Typography variant="h6">Don’t have a file to load? Pick a sample and get started!</Typography>
        <Box mt={2}>
          <Typography variant="h3">Intracellular Electrophysiology</Typography>
          <Box display="flex" className="left-bordered-container" mb={3}>
            <Grid container spacing={1}>
              <Grid item>
                <FormControl variant="outlined" className="custom-select">
                  <Select
                    id="samplefile-select"
                    value=""
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
              </Grid>
              <Grid item>
                <FormControl variant="outlined" className="custom-select">
                  <Select
                    id="samplefile-select"
                    value=""
                    onChange={this.handleChange}
                    className="button badge-button"
                    name="ferguson"
                    displayEmpty
                    inputProps={{ 'aria-label': 'ferguson' }}
                  >
                    <MenuItem value="" disabled>
                      Lantyer et al. 2018
                    </MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER}>Lantyer 1</MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER_2}>Lantyer 2</MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER_3}>Lantyer 3</MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER_4}>Lantyer 4</MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER_5}>Lantyer 5</MenuItem>
                    <MenuItem value={SAMPLE_LINK_LANTYER_6}>Lantyer 6</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item>
                <Button
                  id="loadFile"
                  variant="outlined"
                  className="button badge-button"
                  onClick={e => this.handleClickLoadFile(SAMPLE_LINK_LANORE)}
                  disabled={false}
                >
                  Lanore et al. 2019
                </Button>
              </Grid>
            </Grid>
          </Box>
          <Typography variant="h3">Calcium fluorescence imaging (time series)</Typography>
          <Box display="flex" className="left-bordered-container" mb={3}>
            <Grid container spacing={1}>
              <Grid item>
                <Button
                  id="loadFile"
                  variant="outlined"
                  className="button badge-button"
                  onClick={e => this.handleClickLoadFile(SAMPLE_LINK_TRIPLETT)}
                  disabled={false}
                >
                  Triplett et al. 2018
                </Button>
              </Grid>
              <Grid item>
                <Button
                  id="loadFile"
                  variant="outlined"
                  className="button badge-button"
                  onClick={e => this.handleClickLoadFile(SAMPLE_LINK_KATO)}
                  disabled={false}
                >
                  Kato et al. 2015
                </Button>
              </Grid>
            </Grid>
          </Box>
          <Typography variant="h3">Calcium fluorescence imaging (image series)</Typography>
          <Box display="flex" className="left-bordered-container">
            <Grid container spacing={1}>
              <Grid item>
                <Button
                  id="loadFile"
                  variant="outlined"
                  className="button badge-button"
                  onClick={e => this.handleClickLoadFile(SAMPLE_LINK_PACKER)}
                  disabled={false}
                >
                  Packer et al. 2015
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </div>

    );
  }
}
