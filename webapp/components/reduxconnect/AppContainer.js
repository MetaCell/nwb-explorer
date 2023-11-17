import { connect } from "react-redux";
import App from "../App";

const mapStateToProps = state => ({ nwbFileUrl: state.nwbfile.nwbFileUrl });

export default connect(mapStateToProps, null)(App);
