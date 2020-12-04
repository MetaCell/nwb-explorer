import Manager from '@geppettoengine/geppetto-client/common/Manager';
import nwbService from './NWBFileService';
/**
 * Override standard Manager
 *
 */
class NWBGeppettoManager extends Manager{

  constructor () {
    super();
  }
  

  // /**
  //  * Resolve import type
  //  *
  //  * @param typePath
  //  */
  // resolveImportType (typePaths, callback) {
  //   throw "operation not supported on NWB Manager";
  // }


  /**
   *
   * @param typePath
   * @param callback
   */
  async resolveImportValue (typePath, callback) {
    var params = {};
    params["experimentId"] = -1;
    params["projectId"] = Project.getId();
    // replace client naming first occurrence - the server doesn't know about it
    params["path"] = typePath.replace(GEPPETTO.Resources.MODEL_PREFIX_CLIENT + ".", '');

    var requestID = GEPPETTO.MessageSocket.send("resolve_import_value", params, callback);

    GEPPETTO.trigger('spin_logo');
  }

  
  /**
   *
   * @param payload
   */
  loadExperiment (experimentId, recordedVariables, setParameters) {
    throw "operation not supported on NWB Manager";
  }

  /**
   *
   * @param experiment
   * @returns {*}
   */
  createExperiment (experiment) {
    throw "operation not supported on NWB Manager";
  }

  /**
   * Creates experiment batch on project model
   *
   * @param experiments
   */
  createExperimentBatch (experiments) {
    throw "operation not supported on NWB Manager";
  }

  /**
   *
   * @param data
   */
  deleteExperiment (data) {
    throw "operation not supported on NWB Manager";
  }

  updateExperimentsStatus (experimentsStatus) {
    throw "operation not supported on NWB Manager";
  }


}

export const nwbManager = new NWBGeppettoManager();

export default nwbManager;