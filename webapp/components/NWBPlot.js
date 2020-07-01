import React from 'react';
import PlotComponent from 'geppetto-client/js/components/interface/plot/PlotComponent.js';

import ExternalInstance from 'geppetto-client/js/geppettoModel/model/ExternalInstance';

export default class NWBTimeseriesPlotComponent extends React.Component {

  getLegendName (projectId, experimentId, instance, sameProject) {
    const instancePath = instance.getInstancePath()
      .split('.')
      .filter((word, index, arr) => index != 0 && index != arr.length - 1)
      .join('.')

    if (sameProject) {
      window.Project.getExperiments().forEach(experiment => {
        if (experiment.id == experimentId) {
          return `${instancePath} [${experiment.name}]`;
        }
      })
    } else {
      GEPPETTO.ProjectsController.getUserProjects().forEach(project => {
        if (project.id == projectId) {
          project.experiments.forEach(experiment => {
            if (experiment == experimentId) {
              return `${instancePath} [${project.name} - ${experiment.name}]`;
            }
          })
        }
      })
    }
  }
  
  extractLegendName (instanceY) {
    let legendName = instanceY.getInstancePath()
      .split('.')
      .filter((word, index, arr) => index != 0 && index != arr.length - 1)
      .join('.')

    if (instanceY instanceof ExternalInstance) {
      legendName = this.getLegendName(instanceY.projectId, instanceY.experimentId, instanceY, window.Project.getId() == instanceY.projectId);
    }  
    return legendName
  }

  render () {
    const { instancePaths } = this.props;


    const plots = instancePaths.map(instancePath => ({ 
      x: `${instancePath}.timestamps`,
      y: `${instancePath}.data`,
      lineOptions: { color: Instances.getInstance(instancePath).color } // TODO move color information to redux
    }));
    

    return (
      <PlotComponent
        plots={plots}
        extractLegendName={this.extractLegendName}
      />
    )
  }
}