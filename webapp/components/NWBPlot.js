import React from 'react';
import PlotComponent from '@geppettoengine/geppetto-ui/plot/PlotComponent';

import ExternalInstance from '@geppettoengine/geppetto-core/model/ExternalInstance';

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
    const { instancePaths, key } = this.props;


    const plots = instancePaths.map(instancePath => ({ 
      x: `${instancePath}.timestamps`,
      y: `${instancePath}.data`,
      lineOptions: { color: this.props.modelSettings[instancePath].color }
    }));
    

    return (
      <PlotComponent
        id={key}
        plots={plots}
        extractLegendName={this.extractLegendName}
      />
    )
  }
}