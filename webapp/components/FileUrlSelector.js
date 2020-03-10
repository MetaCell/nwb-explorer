import React from 'react';


import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';


export default class FileUrlSelector extends React.Component {

  constructor (props) {
    super(props);
    this.handleClickLoadFile = this.handleClickLoadFile.bind(this);

    this.state = { inputValue: '' };
  } 

  
  componentDidUpdate (prevProps, prevState) {
   
  }
  handleClickLoadFile () {
    const { loadNWBFile } = this.props
    loadNWBFile(this.state.inputValue);
  }

  updateInputValue (evt) {
    this.setState({ inputValue: evt.target.value });
  }
  render () {
    

    return (
      <div>
        <h2>What file do you wish to load?</h2>
        <div className="aligned-form-elements-wrapper">
          <TextField
            id="nwb-url-input"
            placeholder="Paste a URL pointing to an NWB v2 file"
            // helperText="Insert a public url or local absolute path of an NWB file"
            className = 'aligned-form-element input'
            variant="outlined"
            onChange={ evt => this.updateInputValue(evt) }
          />
          <Button
            id="load-file-button"
            variant="outlined"
            onClick={this.handleClickLoadFile}
            className = 'aligned-form-element button'
            disabled={this.state.inputValue.length <= 5}
          >Load NWB file</Button>
        </div>
      </div>
    );
  }

}
