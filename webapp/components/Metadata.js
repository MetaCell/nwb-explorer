import React from 'react';
import Collapsible from 'react-collapsible';
import Linkify from 'react-linkify';
const Type = require('@geppettoengine/geppetto-core/model/Type');

export default class Metadata extends React.Component {

  state = { content: [] }

  prettyLabel (string) {

    let output = string.charAt(0).toUpperCase() + string.slice(1);
    return output.replace('_interface_map', '').replace('_', ' ')
  }

  prettyContent (string) {
    
    return <Linkify>{string}</Linkify>;
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
      const { prettyLabel } = this;
      let metadata;

      if (variableType.getName() == 'Text') {
        let value = variable.getInitialValue().value.text;

        metadata = this.prettyContent(value);

      } else if (variableType.getName() == 'HTML') {
        metadata = <span dangerouslySetInnerHTML={{ __html: variable.getInitialValue().value.html }}></span>;
      } else if (variableType.getName() == 'URL') {
        if (variable.getInitialValue().value.url.includes("http")){
          metadata = <a target='_blank' title="Download file" href={ variable.getInitialValue().value.url }>{ variable.getInitialValue().value.url.split('/').slice(-1) }</a>
        } else {
          metadata = <span>{ variable.getInitialValue().value.url.split('//').slice(-1) }</span>
        }
        
      } else if (variableType.getChildren && variableType.getChildren()) {
        metadata = variable.getType().getChildren().filter(v => v.getType().getName() == 'Text').map(v => this.formatField(prettyLabel(v.getId()), this.prettyContent(v.getInitialValue().value.text)));
      } else if (variableType.getName() == 'Simple Array') {
        metadata = variable.getInitialValue().value.elements.join(',');
        console.log('Array:', metadata);
      } else {
        console.debug('Unsupported variable', variable)
      }

      if (metadata && (metadata.length || metadata.type)) {
        content.push(
          this.formatCollapsible(name, metadata)
        );
      }

    });

    return content;

  }

  getTypeSupport (typeName) {
    if (typeName == 'TimeSeries' || typeName == 'ImageSeries') {
      return 'metadata and experimental data';
    } else if (typeName === 'Unsupported') {
      return 'Unsupported';
    } else if (typeName.includes('Series')) {
      return 'partial - metadata and possibly experimental data';
    } else {
      return 'partial - metadata only';
    }
  }

  formatCollapsible (name, metadata) {
    const { prettyLabel } = this;
    return <Collapsible open={true} trigger={prettyLabel(name)}>
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