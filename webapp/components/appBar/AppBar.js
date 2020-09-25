import React, { Component, Fragment } from 'react';
import { Icon, Box, Tooltip, Grid, AppBar, Typography, Toolbar, IconButton, withStyles } from '@material-ui/core';
import Menu from "@geppettoengine/geppetto-ui//menu/Menu";
import { WidgetStatus, APPBAR_CONSTANTS } from '../constants';
import toolbarConfig from "./menuConfiguration";

const styles = theme => ({
  lightTooltip: {
    fontSize: 12,
    boxShadow: theme.shadows[1],
    color: theme.palette.common.black,
    backgroundColor: theme.palette.common.white
  },
  popper: { paddingRight: "10px" },
});

const CustomTooltip = withStyles(styles)(({ tooltip, children, classes }) => (
  <Tooltip
    title={tooltip}
    placement="bottom-end"
    disableFocusListener
    disableTouchListener
    classes={{ tooltip: classes.lightTooltip, popper: classes.popper }}
  >
    {children}
  </Tooltip>
))

export default class Appbar extends Component {
  constructor (props) {
    super(props);
    this.exit = this.props.exit ? this.props.exit : () => console.debug('exit not defined in ' + typeof this);
    this.showList = this.props.showList ? this.props.showList : () => console.debug('showList not defined in ' + typeof this);
    this.showAcquisition = this.props.showAcquisition ? this.props.showAcquisition : () => console.debug('showAcquisition not defined in ' + typeof this);
    this.showStimulus = this.props.showStimulus ? this.props.showStimulus : () => console.debug('showStimulus not defined in ' + typeof this);
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

  menuHandler (click) {
    if (!click) {
      return;
    }
    switch (click.handlerAction) {
    case "redux": {
      const [action, payload] = click.parameters;
      if (payload !== undefined) {
        this.props.dispatchAction(action(payload));
      } else {
        this.props.dispatchAction(action);
      }
      break;
    }
    case APPBAR_CONSTANTS.HOME: {
      this.handleClickBack()
      break;
    }
    case APPBAR_CONSTANTS.SHOW_ALL_CONTENT: {
      this.handleShowAll()
      break;
    }
    case APPBAR_CONSTANTS.RESTORE_VIEW: {
      this.handleShowLists()
      break;
    }
    case APPBAR_CONSTANTS.NEW_PAGE: {
      const [url] = click.parameters;
      window.open(url, "_blank");
      break;
    }
    default:
      console.log("Menu action not mapped, it is " + click);
    }
  }

  render () {

    const { classes } = this.props;
    return (
      <Fragment>
        <AppBar position="static" color="secondary" >
          <Toolbar classes={{ gutters: 'toolbar-gutters' }}>
            <Grid
              container
              justify="space-between"
            >
              <Menu
                configuration={toolbarConfig}
                menuHandler={this.menuHandler.bind(this)}
              />
              {/* <Grid item >
                <Box id="main-header">
                  <Typography variant="h1">
                    NWB Explorer <sup>beta</sup>
                  </Typography>
                </Box>
              </Grid>

              <Grid item className="icon-container">

                <CustomTooltip tooltip="Back">
                  <IconButton
                    onClick={() => this.handleClickBack()}
                  >
                    <Icon color="error" className='fa fa-home'/>
                  </IconButton>
                </CustomTooltip>


                <CustomTooltip tooltip="Restore tabs">
                  <IconButton
                    onClick={() => this.handleShowLists()}
                  >
                    <Icon color="error" className='fa fa-sitemap' />
                  </IconButton>
                </CustomTooltip>

                <CustomTooltip tooltip="Show all content">
                  <IconButton
                    onClick={() => this.handleShowAll()}
                  >
                    <Icon color="error" className='fa fa-list' />
                  </IconButton>
                </CustomTooltip>

              </Grid>
             */}
            </Grid>
          </Toolbar>

        </AppBar>
      </Fragment>
    );
  }
}
