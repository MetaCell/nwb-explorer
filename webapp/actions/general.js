export const RAISE_ERROR = 'RAISE_ERROR';
export const RECOVER_FROM_ERROR = 'RECOVER_FROM_ERROR';
export const WAIT_DATA = 'WAIT_DATA';


export const raiseError = error => ({ 
  error,
  type: RAISE_ERROR 
})

export const waitData = (message, offAction) => ({ type: WAIT_DATA, data: { message: message, offAction: offAction } })