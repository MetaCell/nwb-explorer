import React from 'react';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';


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
        <Typography variant="h6" className="input-label">What file do you wish to load?</Typography>
        <Box display="flex" alignItems="flex-end" justifyContent="space-between" className="input-with-button">
          <TextField
            id="nwb-url-input"
            placeholder="Paste a URL pointing to an NWB v2 file"
            // helperText="Insert a public url or local absolute path of an NWB file"
            className = 'input-form-control'
            placeholder="Paste an URL pointing to an NWB v2 file"
            margin="0"
            InputLabelProps={
              { shrink: true }
            }
            onChange={ evt => this.updateInputValue(evt) }
          />
          <Button
            color="primary"
            id="load-file-button"
            variant="contained"
            onClick={this.handleClickLoadFile}
            disabled={this.state.inputValue.length <= 5}
          >LOAD NWB FILE</Button>
        </Box>
      </div>
    );
  }

}
