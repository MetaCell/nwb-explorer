import React from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import Alert from "@material-ui/lab/Alert";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";

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
