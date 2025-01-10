import React from 'react';
import Button from '@mui/material/Button';
import MuiDialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import Typography from '@mui/material/Typography';
import DialogTitle from '@mui/material/DialogTitle';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid2';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { fontColor } from '../theme';
import logo_nwb_explorer from '../resources/logos/nwb-explorer.png';
import logo_metacell from '../resources/logos/metacell_logo.png';
import logo_osb_colour from '../resources/logos/osblogofull.png';
import { NWBE_WEBSITE } from '../constants';

const styles = {
  paper: {
    backgroundColor: '#4a4a4a',
    textAlign: 'center',
    padding: 2,
    '& .MuiTypography-root': { color: fontColor, },
  },
};

const AboutContent = () => (

  <Paper sx={styles.paper}>
    <Grid container className="p-0">
      <Grid item size={6}>
        <Box mb={1} alignItems="flex-start" display="flex">
          <img width="150" src={logo_nwb_explorer} />
        </Box>
      </Grid>
      <Grid item size={6}>
        <Box mb={1} justifyContent="flex-end" display="flex" alignItems="center">
          <Typography variant='caption' style={{ marginRight: '0.75rem' }}>Powered by</Typography>
          <Link href="http://www.metacell.us" target="_blank">
            <img width="120" src={logo_metacell} />
          </Link>
        </Box>
      </Grid>
    </Grid>

    <Box m={1}>
      <Typography variant="h5">NWB Explorer v0.7.0</Typography>
    </Box>

    <Box m={1}>
      <Typography variant="body2">
        NWB Explorer is a web application that can be used by scientists to read, visualize and explore the content of NWB:N 2 files.
      </Typography>
    </Box>

    <Box m={1} pb={2}>
      <Typography variant="body2">
        Want to know more? Go to our
        {' '}
        <Link href={NWBE_WEBSITE} target="_blank">website</Link>
        .
      </Typography>
    </Box>

    <Box m={1}>
      <Typography variant="body2">
        NWB Explorer is being developed in collaboration with:
      </Typography>
      <Link href="http://www.opensourcebrain.org" target="_blank">
        <img width="200" src={logo_osb_colour} />
      </Link>
    </Box>

  </Paper>

);

export default function Dialog ({ open, title, message, handleClose, }) {
  return (
    <div>
      <MuiDialog
        fullWidth
        maxWidth="sm"
        open={open}
        onClose={handleClose}
      >
        <DialogTitle className="modal-title">{title}</DialogTitle>
        <DialogContent>
          <AboutContent />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary" className="font-16" autoFocus>
            Close
          </Button>
        </DialogActions>
      </MuiDialog>
    </div>
  );
}
