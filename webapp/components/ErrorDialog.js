import React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import Alert from '@mui/material/Alert';
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";

export default ({ error, startRecoveryFromError }) => {
  let title = "An error occurred";

  return error ? (
    <Dialog open maxWidth="sm">
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Alert severity="error">{error}</Alert>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => startRecoveryFromError()}
          color="secondary"
          autoFocus
          variant="contained"
        >
          Ok
        </Button>
      </DialogActions>
    </Dialog> 
  ) : null
};
