import { createTheme } from '@mui/material/styles';

const baseTheme = {
  darkMode: true,
  typography: {
    useNextVariants: true,
    suppressDeprecationWarnings: true,
    button: {
      textTransform: 'none',
      fontSize: '14px',
      lineHeight: '24px',
      fontWeight: '500',
      letterSpacing: '0.16px',
      padding: '9px 16px',
    },
  },
  palette: {
    primary: { main: 'rgb(var(--primary-color))' },
    secondary: { main: 'rgb(var(--secondary-color))' },
    error: { main: '#ffffff' },
    mode: 'dark',
    text: { main: "rgb(174, 174, 174)", secondary: '#ffffff' },
  },
  components: {
    MuiInput: {
      styleOverrides: {
        input: {
          outline: 'none !important',
          border: 'none !important',
          boxShadow: 'none !important',
          fontSize: '16px',
        },
        root: { color: 'var(--font-color)' },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: 'var(--font-color)',
          paddingTop: 'calc(var(--gutter) / 2)',
          fontSize: '13px',
        },
        gutters: {
          paddingLeft: 'calc(var(--gutter) * 2)',
          paddingRight: 'calc(var(--gutter) * 2)',
        },
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          color: 'inherit',
          backgroundColor: 'var(--bg-regular)',
          boxShadow: 'none !important',
          borderRadius: '2px !important',
        },
      }
    },
    MuiFormControl: { styleOverrides: { root: { overflow: 'visible' } } },
    MuiBackdrop: { styleOverrides: { root: { zIndex: 9999 } } },
    MuiButton: {
      styleOverrides: {
        contained: {
          color: 'var(--font-color)',
          backgroundColor: 'var(--bg-inputs)',
          borderRadius: '2px',
          textTransform: 'uppercase',
        },
        outlined: {
          borderColor: 'var(--button-outline-color)',
          borderRadius: '16px',
          color: 'var(--button-outline-color)',
          fontSize: '13px',
          lineHeight: '13px',
          fontWeight: '400',
          marginBottom: '9px',
          padding: '8px 15px',
          '&:hover': {
            background: 'rgba(255, 255, 255, 0.1)',
            borderColor: 'var(--button-outline-color)',
          },
        },
        containedSecondary: { color: 'var(--font-color)' },
        containedPrimary: { color: 'var(--font-color)' },
      }
    },
    MuiTypography: {
      styleOverrides: {
        color: '#FFF',
        fontWeight: '400',
        h1: {
          fontSize: '34px',
          lineHeight: '40px',
        },
        h2: {
          fontSize: '20px',
          lineHeight: '32px',
          letterSpacing: '0.5px',
          marginBottom: '41px',
          color: 'rgba(255,255,255,0.3)',
          fontWeight: '400',
        },
        h3: {
          fontSize: '16px',
          lineHeight: '18px',
          marginBottom: 10,
        },
        h4: {
          fontSize: '12px',
          lineHeight: '20px',
          letterSpacing: '0.32px',
          color: 'var(--bg-inputs)',
          textTransform: 'Uppercase',
          margin: '13px 0 11px',
        },
        h6: {
          fontSize: '12px',
          fontWeight: '400',
          lineHeight: '20px',
          marginBottom: '5px',
          color: 'var(--primary-color)',
        },
        body2: {
          fontSize: '14px',
          fontWeight: '400',
          marginBottom: '5px',
        },
        root: { color: 'var(--font-color)' },
      },
    },
    MuiIcon: { styleOverrides: { fontSizeSmall: { fontSize: '10px' } } },
    MuiDialog: { styleOverrides:{ paper: { zIndex: 10000 } } }
  },
};

export default createTheme(baseTheme);
