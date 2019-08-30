import React, { Fragment } from 'react';
import Icon from '@material-ui/core/Icon';
import Grid from '@material-ui/core/Grid';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import { WidgetStatus } from './constants';


export default class Appbar extends React.Component {
  constructor (props) {
    super(props);
    this.exit = this.props.exit ? this.props.exit : () => console.debug('exit not defined in ' + typeof this);
    this.showList = this.props.showList ? this.props.showList : () => console.debug('showList not defined in ' + typeof this);
    this.showAcquisition = this.props.showAcquisition ? this.props.showAcquisition : () => console.debug('showAcquisition not defined in ' + typeof this);
    this.showStimulus = this.props.showStimulus ? this.props.showStimulus : () => console.debug('showStimulus not defined in ' + typeof this);
  }

  componentDidMount () {

  }
  
  componentDidUpdate (prevProps, prevState) {

  }

  
  handleClickBack () {
    this.exit();
  }

  handleShowLists () {
    this.showAcquisition();
    this.showStimulus();
  }

  handleShowAll () {
    this.showList('Content index', "nwbfile.", "^(?!LabelledDict).*")
  }
  
  render () {
 
    return (
      <Fragment>
        <AppBar position="static" color="secondary">
          <Toolbar classes={{ gutters: 'toolbar-gutters' }}>
            <Grid
              container 
              spacing={8}
              justify="space-between"
            >
              <Grid item >
                <header id="main-header">
                  <h1>NWB Explorer<sub>beta</sub></h1>
           
                </header>
              </Grid>

              <Grid item className="icon-container">

                <IconButton
                  onClick={() => this.handleClickBack()}
                >
                  <Icon color="error" className='fa fa-home' title="Back" />
                </IconButton>
                
                
                <IconButton 
                  onClick={() => this.handleShowLists()}
                >
                  <Icon color="error" className='fa fa-sitemap' title="restore default lists" />
                </IconButton>

                <IconButton 
                  onClick={() => this.handleShowAll()}
                >
                  <Icon color="error" className='fa fa-list' title="Show all content" />
                </IconButton>
              </Grid>
            </Grid>
          </Toolbar>
          
        </AppBar>
      </Fragment>
    );
  }
}