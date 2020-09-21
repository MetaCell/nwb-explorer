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
} = vars;

const baseTheme = {
  typography: {
    useNextVariants: true,
    suppressDeprecationWarnings: true,
    button: {
      textTransform: "none",
      fontSize: "1.0rem",
    },
  },
  palette: {
    primary: { main: primaryColor },
    secondary: { main: secondaryColor },
    error: { main: "#ffffff" },
    text: { secondary: "white" },
  },
  overrides: { MuiIcon: { root: { fontSize: "2.5rem" } } },
};

export default createMuiTheme(baseTheme);
