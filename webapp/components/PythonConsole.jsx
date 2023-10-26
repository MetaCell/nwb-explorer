import React, { Component } from "react";
import CircularProgress from "@material-ui/core/CircularProgress";

export class NWBPythonConsole extends Component {
  componentDidMount () {}

  componentWillUnmount () {
    console.info("unmounting python console");
  }

  render () {
    return (
      <>
        <iframe
          id="pythonConsoleFrame"
          src={this.props["pythonNotebookPath"]}
          allowtransparency="true"
          style={{
            visibility: !this.props.extensionLoaded ? "hidden" : "visible",
          }}
        ></iframe>
        {!this.props.extensionLoaded && (
          <CircularProgress
            color="primary"
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              bottom: 0,
              top: 0,
              margin: "auto"
            }}
          />
        )}
      </>
    );
  }
}

export default NWBPythonConsole;
