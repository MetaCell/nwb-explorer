import React from 'react';
import { Box, Paper, Grid, Link, Typography, Hidden, withStyles } from '@material-ui/core';

import FileUrlSelector from '../reduxconnect/FileUrlSelectorContainer';
import FileSampleSelector from '../reduxconnect/FileSampleSelectorContainer';

import logo_osb from '../../resources/logos/osb.png';
import logo_openworm from '../../resources/logos/openworm.png';
import logo_metacell from '../../resources/logos/metacell_new.png';
import logo_wellcome from '../../resources/logos/wellcome.png';
import logo_nwb_explorer from '../../resources/logos/nwb-explorer.png';

const styles = theme => ({
  leftColumn: {
    padding: "0 30px",
    [theme.breakpoints.up('sm')]: { padding: "0 89px 0 57px" },
    [theme.breakpoints.up('md')]: { padding: "0 30px" },
    [theme.breakpoints.up('lg')]: { padding: "0 89px 0 57px" }
  }
});

class SplashPage extends React.Component{
  render () {
    const { classes } = this.props;
    return <div id="splash" className="h-100">
      <Grid container className="h-100 p-0">
        <Grid item sm={12} md={7} className={ classes.leftColumn }>
          <Box>
            <img src={logo_nwb_explorer} alt="NWB Explorer" title="NWB Explorer" className="brand-logo"></img>
            <Typography variant="h1">
              Welcome to NWB Explorer <sup>beta</sup>
            </Typography>
            <Typography variant="h2">
              Visualise and understand your neurophysiology data
            </Typography>
          </Box>
          <Paper className="grey-box first">
            <FileUrlSelector/>
          </Paper>
          <Paper className="grey-box scrollbar">
            <FileSampleSelector/>
          </Paper>
          <Box container className="splash-footer" mb={5}>
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
            <Grid item align="right">
              <Box>
                  Supported by
              </Box>
              <Link href="https://wellcome.ac.uk/" title="Wellcome" className="m-0">
                <img src={logo_wellcome} alt="Wellcome" height="35"></img>
              </Link>
            </Grid>
          </Box>
        </Grid>
        <Hidden smDown>
          <Grid item sm={4} md={5} className="splash-background">
            <Box className="logo-container">
              <Link href="https://metacell.us/" className="logo" title="MetaCell">
                <img src={logo_metacell} alt="MetaCell" ></img>
              </Link>
            </Box>
          </Grid>
        </Hidden>
      </Grid>
    </div>;
  }
}

export default withStyles(styles, { withTheme: true })(SplashPage)
