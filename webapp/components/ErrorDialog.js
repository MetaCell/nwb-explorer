import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Collapsible from 'react-collapsible';

import { NWB_FILE_NOT_FOUND_ERROR, MODULE_NOT_FOUND_ERROR, NAME_ERROR } from './constants'

export default ({ error, startRecoveryFromError }) => {
  let title, message
  
  if (error) {
    const { ename, evalue } = error  
    switch (ename) {
    case NWB_FILE_NOT_FOUND_ERROR:
      title = "Wrong URL?"
      message = `Unable to find: '${eval(evalue)}'`
      break;
    
    case MODULE_NOT_FOUND_ERROR:
      title = "Missing module"
      message = evalue
      break;

    case NAME_ERROR:
      title = "Name Error"
      message = evalue
      break

    default:
      title = "Houston we have a problem..."
      message = evalue
      break;
    }
  }
  
  return (error 
    ? <Dialog
      open={true}
      disableBackdropClick
      disableEscapeKeyDown
      maxWidth="sm"
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <pre dangerouslySetInnerHTML={{ __html: IPython.utils.fixConsole(message) }}/>
        <Collapsible 
          style={{ marginTop: '15px' }} 
          open={false} 
          trigger="Details"
          triggerStyle={{ color: "grey" }}
        >
          <pre dangerouslySetInnerHTML={{ __html: IPython.utils.fixConsole(error.traceback) }}/>
        </Collapsible>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => startRecoveryFromError()} color="secondary" autoFocus variant="contained" >Ok</Button>
      </DialogActions>
    </Dialog>
    : <div/>
  )
}