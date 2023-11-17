import { connect } from "react-redux";
import _PythonConsole from "../PythonConsole";

export const PythonConsole = connect(
  state => ({ extensionLoaded: state.nwbfile.isLoadedInNotebook }),
  null
)(_PythonConsole);
