import React from 'react';
import Grid from '@material-ui/core/Grid';

import FileUrlSelector from '../reduxconnect/FileUrlSelectorContainer';
import FileSampleSelector from '../reduxconnect/FileSampleSelectorContainer';

import img from '../../resources/splash.jpg';
import logo_osb from '../../resources/logos/osb.png';
import logo_openworm from '../../resources/logos/openworm.png';
import logo_metacell from '../../resources/logos/metacell.png';
import logo_gsoc from '../../resources/logos/gsoc.png';
import logo_wellcome from '../../resources/logos/wellcome.png';
 
export default class SplashPage extends React.Component{

  render () {
    return <div id="splash">
      <Grid container className="{classes.root} container" spacing={2}>
        <Grid item sm={12} >
          <header id="main-header">
            <h1>Welcome to NWB Explorer<sub>beta</sub></h1>
            <p>Visualise and understand your neurophysiology data</p>
          </header>
        </Grid>

        <Grid className="sidebar center-filler" item xs={12} sm={12} md={6} lg={5} xl={4} >
          <div className="greybox">
            <FileUrlSelector/>
          </div>
          <div className="greybox flex-filler">
            <FileSampleSelector/>
          </div>
        </Grid>
        <Grid className="center-filler" item xs={12} sm={12} md={6} lg={7} xl={8} >
          <div className="slide-image">
            <img className="grid-fill" src={img} />
          </div>
            
        </Grid>
        
        <Grid item sm={12} >
          <footer id="nwb-footer">
            <div className="footer-left footer-aligned-container">
              <a className="footer-aligned" href="https://github.com/MetaCell/nwb-explorer/blob/development/README.md" >Brought to you by</a>
              <a className="footer-aligned" href="http://www.opensourcebrain.org/"><img src={logo_osb} alt="Open source brain" title="Open source brain"></img></a>
              <a className="footer-aligned" href="http://openworm.org/"><img src={logo_openworm} alt="OpenWorm Foundation" title="OpenWorm Foundation"></img></a>
              <a className="footer-aligned" href="https://metacell.us/"><img src={logo_metacell} alt="MetaCell" title="MetaCell"></img></a>
            </div>
            <div className="footer-right footer-aligned-container">
              <span>Supported by</span>
              <a className="footer-aligned" href="https://summerofcode.withgoogle.com/"><img src={logo_gsoc} alt="Google Summer of Code" title="Google Summer of Code"></img></a>
              <a className="footer-aligned" href="https://wellcome.ac.uk/"><img src={logo_wellcome} alt="Wellcome" title="Wellcome"></img></a>
            </div>
          </footer>
        </Grid>
      </Grid>
    </div>;
  }
}
{/*  */}

