import React from 'react';
import Button from '@material-ui/core/Button';
import MuiDialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import Typography from '@material-ui/core/Typography';
import DialogTitle from '@material-ui/core/DialogTitle';
import { secondaryColor } from '../theme'
import Paper from '@material-ui/core/Paper'
import Box from '@material-ui/core/Box'
import Link from '@material-ui/core/Link'
import logo_nwb_explorer from '../resources/logos/nwb-explorer.png';
import { NWB_WEBSITE } from './constants';

const AboutContent = () => (
  <Paper style={{ backgroundColor: "white", textAlign: 'center' }}>
    <img style={{ width: 150 }} src={logo_nwb_explorer} />
    <Box m={1}>
      <Typography variant="h5" style={{ color: secondaryColor }}>NWB Explorer v0.5.0</Typography>
    </Box>
    
    <Box m={1} >
      <Typography variant="body2" style={{ color: secondaryColor }}>
        NWB Explorer is a web application that can be used by scientists to read, visualize and explore the content of NWB:N 2 files.
      </Typography>
    </Box>

    <Box m={1} pb={2}>
      <Typography variant="body2" style={{ color: secondaryColor }}>
        Want to know more? Go to our <Link href={NWB_WEBSITE} target="_blank">website</Link>.
      </Typography>
    </Box>

    <Box m={1}>
      <Typography variant="body2" style={{ color: secondaryColor }}>
        NWB Explorer is being developed in collaboration with:
      </Typography>
      <Link href="http://www.metacell.us" target="_blank">
        <img style={{ width: 150, padding: "10px" }} src="https://raw.githubusercontent.com/ddelpiano/bucket/master/MetaCellLogoHorizontal300ppi.png"></img>
      </Link>
    </Box>


  </Paper>
    
)

export default function Dialog ({ open, title, message, handleClose }) {
  return (
    <div>
      <MuiDialog
        fullWidth
        maxWidth="sm"
        open={open}
        onClose={handleClose}
      >
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          <AboutContent/>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary" autoFocus>
            Close
          </Button>
        </DialogActions>
      </MuiDialog>
    </div>
  );
}
