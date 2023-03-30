export const RAISE_ERROR = 'RAISE_ERROR';
export const RECOVER_FROM_ERROR = 'RECOVER_FROM_ERROR';
export const WAIT_DATA = 'WAIT_DATA';
export const OPEN_DIALOG = 'OPEN_DIALOG';
export const CLOSE_DIALOG = 'CLOSE_DIALOG';

export const openDialog = payload => ({ type: OPEN_DIALOG, payload });

export const closeDialog = { type: CLOSE_DIALOG };

export const raiseError = error => ({
  error,
  type: RAISE_ERROR,
});

export const waitData = (message, offAction) => ({ type: WAIT_DATA, data: { message, offAction } });
