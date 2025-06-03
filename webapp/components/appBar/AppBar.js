import React, { Component, Fragment } from 'react';
import { Icon, Box, Tooltip, Grid2 as Grid, AppBar, Typography, Toolbar, IconButton } from '@mui/material';
import Menu from '@metacell/geppetto-meta-ui//menu/Menu';
import { WidgetStatus, APPBAR_CONSTANTS } from '../../constants';
import toolbarConfig from './menuConfiguration';

export default class Appbar extends Component {
  constructor (props) {
    super(props);
    this.exit = this.props.exit ? this.props.exit : () => console.debug(`exit not defined in ${typeof this}`);
    this.showList = this.props.showList ? this.props.showList : () => console.debug(`showList not defined in ${typeof this}`);
    this.showAcquisition = this.props.showAcquisition ? this.props.showAcquisition : () => console.debug(`showAcquisition not defined in ${typeof this}`);
    this.showStimulus = this.props.showStimulus ? this.props.showStimulus : () => console.debug(`showStimulus not defined in ${typeof this}`);
    this.showProcessing = this.props.showProcessing ? this.props.showProcessing : () => console.debug(`showProcessing not defined in ${typeof this}`);
  }

  handleClickBack () {
    this.exit();
  }

  handleShowLists () {
    this.showAcquisition();
    this.showStimulus();
    this.showProcessing();
  }

  handleShowAll () {
    this.showList('Content index', 'nwbfile.', '^(?!LabelledDict).*');
  }

  menuHandler (click) {
    if (!click) {
      return;
    }
    switch (click.handlerAction) {
    case 'redux': {
      const [action, payload] = click.parameters;
      if (payload !== undefined) {
        this.props.dispatchAction(action(payload));
      } else {
        this.props.dispatchAction(action);
      }
      break;
    }
    case APPBAR_CONSTANTS.HOME: {
      this.handleClickBack();
      break;
    }
    case APPBAR_CONSTANTS.SHOW_ALL_CONTENT: {
      this.handleShowAll();
      break;
    }
    case APPBAR_CONSTANTS.RESTORE_VIEW: {
      this.handleShowLists();
      break;
    }
    case APPBAR_CONSTANTS.NEW_PAGE: {
      const [url] = click.parameters;
      window.open(url, '_blank');
      break;
    }
    default:
      console.log(`Menu action not mapped, it is ${click}`);
    }
  }

  render () {
    return (<>
      <AppBar position="static" color="secondary" sx={{ px :1, gap: 1 }}>
        <Toolbar variant="dense" classes={{ gutters: 'toolbar-gutters' }}>
          <Grid
            container
            justifyContent="space-between"
          >
            <Menu
              configuration={toolbarConfig}
              menuHandler={this.menuHandler.bind(this)}
            />
          </Grid>
        </Toolbar>

      </AppBar>
    </>);
  }
}
