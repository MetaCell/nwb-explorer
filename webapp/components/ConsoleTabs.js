import React from 'react';
import Console from 'geppetto-client/js/components/interface/console/Console';
import TabbedDrawer from 'geppetto-client/js/components/interface/drawer/TabbedDrawer';
import PythonConsole from 'geppetto-client/js/components/interface/pythonConsole/PythonConsole';

export default class ConsoleTabs extends React.Component {

  render () {
    
    if (this.props.enabled) {
      return (
        <div className = { this.props.hidden ? 'hidden' : ''} >
          <TabbedDrawer labels={["Console", "Python"]} iconClass={["fa fa-terminal", "fa fa-flask"]} >
            <Console />
            <PythonConsole pythonNotebookPath={"notebooks/notebook.ipynb"} />
          </TabbedDrawer>
        </div>
      );
    } else {
      return '';
    }
  }
}


