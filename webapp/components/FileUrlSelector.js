import React from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default class FileUrlSelector extends React.Component {
  constructor (props) {
    super(props);
    this.handleClickLoadFile = this.handleClickLoadFile.bind(this);

    this.state = { inputValue: '' };
  }

  componentDidUpdate (prevProps, prevState) {

  }

  handleClickLoadFile () {
    const { loadNWBFile } = this.props;
    loadNWBFile(this.state.inputValue);
  }

  updateInputValue (evt) {
    this.setState({ inputValue: evt.target.value });
  }

  render () {
    return (
      <div>
        <Typography variant="h6" >What file do you wish to load?</Typography>
        <Box display="flex" alignItems="flex-end" justifyContent="space-between" className="input-with-button">
          <TextField
            id="nwb-url-input"
            // helperText="Insert a public url or local absolute path of an NWB file"
            className="input-form-control"
            placeholder="Paste a URL pointing to an NWB v2 file"
            margin="0"
            variant="standard"
            slotProps={{ input: { shrink: true } }}
            onChange={evt => this.updateInputValue(evt)}
          />
          <Button
            color="primary"
            id="load-file-button"
            variant="contained"
            onClick={this.handleClickLoadFile}
            disabled={this.state.inputValue.length <= 5}
          >
            Load NWB file
          </Button>
        </Box>
      </div>
    );
  }
}
