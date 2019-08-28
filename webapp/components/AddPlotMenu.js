import React, { Component } from 'react'
import Icon from '@material-ui/core/Icon';
import Popover from '@material-ui/core/Popover';
import MenuItem from '@material-ui/core/MenuItem';
import { CompactPicker } from 'react-color';

const anchor = {
  origin: {
    vertical: 'bottom',
    horizontal: 'right',
  },

  transform: {
    vertical: 'top',
    horizontal: 'right',
  }
}

export default class AddPlotMenu extends Component {
  state = {
    anchorEl: null,
    hostId: null
  }

  goOnlyToTimeseriesWidgets = this.goOnlyToTimeseriesWidgets.bind(this)
  dontGoToSameHostTwice = this.dontGoToSameHostTwice.bind(this)

  clickAddToWidget (color) {
    const { hostId } = this.state
    const { instancePath, action } = this.props
    action({ hostId, instancePath, color: color.hex, type: "timeseries" })
    this.setState({ anchorEl: null, hostId: null })
  }

  dontGoToSameHostTwice (widget) {
    const { guestList } = widget
    if (guestList) {
      const list = guestList.map(guest => guest.instancePath)
      return list.indexOf(this.props.instancePath) == -1
    }
    return true
  }

  goOnlyToTimeseriesWidgets (widget) {
    const { instancePath } = this.props
    return widget.component == 'Plot' && widget.instancePath != instancePath
  }

  render () {
    const { anchorEl, hostId, color } = this.state;
    const { widgets, icon, instancePath } = this.props
    let popover = []

    const hostIds = Object.values(widgets)
      .filter(this.goOnlyToTimeseriesWidgets)
      .filter(this.dontGoToSameHostTwice)
      .map(widget => widget.id)

    if (anchorEl) {
      popover = (
        <Popover
          open={Boolean(anchorEl)}
          anchorEl={anchorEl}
          anchorOrigin={anchor.origin}
          onClose={() => this.setState({ anchorEl: null })}
          transformOrigin={anchor.transform}
        >
          {hostId
            ? <CompactPicker
              color={color}
              onChange={color => this.clickAddToWidget(color)}
            />
            : hostIds.map(hostId =>
              <MenuItem
                id={instancePath}
                key={hostId}
                onClick={() => this.setState({ hostId })}
              >
                { widgets[hostId].name }
              </MenuItem>
            )}

        </Popover>
      )
    }
    if (hostIds.length){
      return (
        <span
          style={{ color: color }}
          className='list-icon'
          title="Add to existing plot"
          onClick={e => hostIds.length > 0 ? this.setState({ anchorEl: e.currentTarget }) : {}}>
          <span
            className={icon}
            style={{ cursor: "pointer" }}
          />
          { popover }
        </span>
      )
    }
    return '';
    
  }
}