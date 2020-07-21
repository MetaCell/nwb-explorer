import React from 'react';
import Console from '@geppettoengine/geppetto-client/components/interface/console/Console';
import TabbedDrawer from '@geppettoengine/geppetto-client/components/interface/drawer/TabbedDrawer';
import PythonConsole from '@geppettoengine/geppetto-client/components/interface/pythonConsole/PythonConsole';

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


