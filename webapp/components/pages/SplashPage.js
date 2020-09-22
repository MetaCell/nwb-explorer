import React from 'react';
import Box from '@material-ui/core/Box';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';

import FileUrlSelector from '../reduxconnect/FileUrlSelectorContainer';
import FileSampleSelector from '../reduxconnect/FileSampleSelectorContainer';

import logo_osb from '../../resources/logos/osb.png';
import logo_openworm from '../../resources/logos/openworm.png';
import logo_metacell from '../../resources/logos/metacell_new.png';
import logo_gsoc from '../../resources/logos/gsoc.png';
import logo_wellcome from '../../resources/logos/wellcome.png';
import logo_nwb_explorer from '../../resources/logos/nwb-explorer.png';

export default class SplashPage extends React.Component{
  render () {

    return <div id="splash" className="splash-main-container">
      <Grid container className="{classes.root} container bg-grey">

        <Grid item sm={12} md={7} className="splash-container">
          <Box>
            <img src={logo_nwb_explorer} alt="NWB Explorer" title="NWB Explorer" className="brand-logo"></img>
            <Typography variant="h1">
              Welcome to NWB Explorer<sup>beta</sup>
            </Typography>
            <Typography variant="h2">
              Visualise and understand your neurophysiology data
            </Typography>
          </Box>
          <Paper className="grey-box">
            <FileUrlSelector/>
          </Paper>
          <Paper className="grey-box">
            <FileSampleSelector/>
          </Paper>
          <Grid container className="splash-footer">
            <Grid item>
              <Box>
                In collaboration with
              </Box>
              <Link href="http://www.opensourcebrain.org/" title="Open Source Brain">
                <img src={logo_osb} alt="Open Source Brain" width="166"></img>
              </Link>
              <Link href="http://openworm.org/" title="OpenWorm Foundation">
                <img src={logo_openworm} alt="OpenWorm Foundation" height="35"></img>
              </Link>
            </Grid>
            <Grid item>
              <Box>
                Supported by
              </Box>
              <Link href="https://summerofcode.withgoogle.com/" title="Google Summer of Code">
                <img src={logo_gsoc} alt="Google Summer of Code" height="35"></img>
              </Link>
              <Link href="https://wellcome.ac.uk/" title="Wellcome">
                <img src={logo_wellcome} alt="Wellcome" height="35"></img>
              </Link>
            </Grid>
          </Grid>
        </Grid>
        <Box component={Grid} item display={{ sm: 'none', md: 'flex' }} sm={4} md={5} className="splash-background">
          <Box className="logo-container">
            <Link href="https://metacell.us/" className="logo" title="MetaCell">
              <img src={logo_metacell} alt="MetaCell" ></img>
            </Link>
          </Box>
        </Box>

      </Grid>
    </div>;
  }
}
{/*  */}

