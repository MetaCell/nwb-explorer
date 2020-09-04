import React, { Component } from "react";
import Menu from "@material-ui/core/Menu";
import Popover from "@material-ui/core/Popover";
import MenuItem from "@material-ui/core/MenuItem";


const anchor = {
  origin: {
    vertical: "bottom",
    horizontal: "right",
  },

  transform: {
    vertical: "top",
    horizontal: "right",
  },
};

export default class AddPlotMenu extends Component {
  state = {
    anchorEl: null,
  };

  goOnlyToTimeseriesWidgets = this.goOnlyToTimeseriesWidgets.bind(this);
  dontGoToSameHostTwice = this.dontGoToSameHostTwice.bind(this);

  clickAddToWidget (selectedPlot) {

    const { instancePath, action } = this.props;
    action({
      hostId: selectedPlot.id,
      instancePath,
      type: "timeseries",
    });
    this.setState({ anchorEl: null });
  }

  dontGoToSameHostTwice (widget) {
    const { instancePaths } = widget;

    return instancePaths && instancePaths.indexOf(this.props.instancePath) == -1;
  }

  goOnlyToTimeseriesWidgets (widget) {
    const { instancePath } = this.props;
    return widget.instancePath != instancePath;
  }

  render () {
    const { anchorEl, selectedPlot, color } = this.state;
    const { widgets, icon, instancePath } = this.props;

    const availablePlots = widgets
      .filter(this.goOnlyToTimeseriesWidgets)
      .filter(this.dontGoToSameHostTwice);
    if (!availablePlots.length) {
      return '';
    }
    return <React.Fragment>
      <span
        style={{ color: color }}
        className="list-icon"
        title="Add to existing plot"
        onClick={e =>
          availablePlots.length > 0
            ? this.setState({ anchorEl: e.currentTarget })
            : {}
        }
      >
        {" "}
        <span className={icon} style={{ cursor: "pointer" }} />
      </span>
      <Menu
        open={Boolean(anchorEl) && !selectedPlot}
        anchorEl={anchorEl}
        onClose={() => this.setState({ anchorEl: null })}
      >
        {
          availablePlots.map(availablePlot => (
            <MenuItem
              id={instancePath}
              key={availablePlot}
              onClick={() => this.clickAddToWidget(availablePlot) }
            >
              {availablePlot.name}
            </MenuItem>
          ))
        }
      </Menu>
      
  
    </React.Fragment>
  }
}
