import React from 'react';
import Collapsible from 'react-collapsible';

const Type = require('geppetto-client/js/geppettoModel/model/Type');

export default class Metadata extends React.Component {

  state = { content: [] }

  prettyFormat (string) {
    let output = string.charAt(0).toUpperCase() + string.slice(1);
    return output.replace('_interface_map', '').replace('_', ' ')
  }

  getContent (geppettoInstanceOrType) {

    const content = [];

    if (!geppettoInstanceOrType) {
      return;
    }

    const type = (geppettoInstanceOrType instanceof Type) ? geppettoInstanceOrType : geppettoInstanceOrType.getType();
    if (this.props.showObjectInfo) {
      content.push(
        this.formatCollapsible('Info',
          [
            this.formatField('Name', type.getId()),
            this.formatField('Type', type.getName()),
            this.formatField('Path', this.props.instancePath),
            this.formatField('NWB Explorer support', this.getTypeSupport(type.getName())),
          ]
        )
      );
    }
    

    type.getChildren().forEach(variable => {
      const variableType = variable.getType();
  
      let name = variable.getId();
      const { prettyFormat } = this;
      let metadata;

      if (variableType.getName() == 'Text') {
        let value = variable.getInitialValue().value.text;
        metadata = value;

      } else if (variableType.getChildren && variableType.getChildren()) {
        metadata = variable.getType().getChildren().filter(v => v.getType().getName() == 'Text').map(v => this.formatField(prettyFormat(v.getId()), v.getInitialValue().value.text));
      }

      if (metadata && metadata.length) {
        content.push(
          this.formatCollapsible(name, metadata)
        );
      }

    });

    return content;

  }
  
  getTypeSupport (typeName) {
    if (typeName == 'TimeSeries' || typeName == 'ImageSeries') {
      return 'Metadata and experimental data';
    } else if (typeName === 'Unsupported') {
      return 'Unsupported';
    } else if (typeName.includes('Series')) {
      return 'Partial: metadata and possibly experimental data';
    } else {
      return 'Partial: metadata only';
    }
  }

  formatCollapsible (name, metadata) {
    const { prettyFormat } = this;
    return <Collapsible open={true} trigger={prettyFormat(name)}>
      <div>{metadata}</div>
    </Collapsible>;
  }

  formatField (name, value) {
    return <p key={name}><span className="meta-label">{name}</span>: {value}</p>;
  }

  shouldComponentUpdate (prevProps) {
    return this.props.instancePath != prevProps.instancePath;
  }


  render () {
    const instance = Instances.getInstance(this.props.instancePath);
    const content = this.getContent(instance);
    return (
      <div style={{ marginBottom: '1em' }}>

        {
          content.map((item, key) =>
            <div key={key}>
              {item}
            </div>
          )
        }
      </div>
    );
  }
}