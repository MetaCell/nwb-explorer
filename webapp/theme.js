import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import lessToJs from "less-vars-to-js";

// Read the less file in as string: using the raw-loader to override the default loader
export const vars = lessToJs(require("!!raw-loader!./css/variables.less"), {
  resolveVariables: true,
  stripPrefix: true,
});

export const {
  primaryColor,
  secondaryColor,
  font,
  fontColor,
  bgLight,
  bgRegular,
  bgDark,
  bgDarker,
  bgDarkest,
  bgInputs,
  gutter,
  radius,
  buttonOutlineColor,
} = vars;

const baseTheme = {
  typography: {
    useNextVariants: true,
    suppressDeprecationWarnings: true,
    button: {
      textTransform: "none",
      fontSize: "14px",
      lineHeight: "24px",
      fontWeight: '500',
      letterSpacing: '0.16px',
      padding: "9px 16px",
    },
  },
  palette: {
    primary: { main: primaryColor },
    secondary: { main: secondaryColor },
    error: { main: "#ffffff" },
    text: { secondary: "white" },
  },
  overrides: {
    MuiInput: {
      input: {
        outline: 'none !important',
        border: 'none !important',
        boxShadow: 'none !important',
        fontSize: '16px',
      },
      root:{ color: fontColor }
    },
    MuiPaper: { root: { color: 'inherit', backgroundColor: bgRegular } },
    MuiFormControl: { root: { overflow: 'visible' } },
    MuiButton: {
      contained: {
        color: fontColor,
        backgroundColor: bgInputs
      },
      outlined: {
        borderColor: buttonOutlineColor,
        borderRadius: '16px',
        color: buttonOutlineColor,
        fontSize: "13px",
        lineHeight: "13px",
        fontWeight: '400',
        marginBottom: '9px'
      },
      containedSecondary: { color: fontColor },
      containedPrimary: { color: fontColor },
    },
    MuiTypography: {
      color: '#FFF',
      fontWeight: '400',
      h1: {
        fontSize: '34px',
        lineHeight: '40px'
      },
      h2: {
        fontSize: '20px',
        lineHeight: '32px',
        letterSpacing: '0.5px',
        marginBottom: '41px',
        color: 'rgba(255,255,255,0.3)',
        fontWeight: '400'
      },
      h3: {
        fontSize: '16px',
        lineHeight: '18px',
        marginBottom: '11px'
      },
      h4: {
        fontSize: '12px',
        lineHeight: '20px',
        letterSpacing: '0.32px',
        color: bgInputs,
        textTransform: 'Uppercase',
        margin: '22px 0 11px',
      },
      h6: {
        fontSize: '12px',
        lineHeight: '20px',
        marginBottom: '5px',
        color: primaryColor
      },

      root: { color: fontColor }
    },

  }
};

export default createMuiTheme(baseTheme);
