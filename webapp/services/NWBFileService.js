import GeppettoPathService from './GeppettoPathService';
import Utils from '../Utils';
const NWB_FILE_URL_PARAM = 'nwbfile';
// const NWB_FILE_DEFAULT_URL = "https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb";

class NWBFileService {

  constructor () {
    this.nwbfile = undefined;
    this.notebookloaded = false;
  }

  getNWBFileUrl () {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get(NWB_FILE_URL_PARAM)) {
      return urlParams.get(NWB_FILE_URL_PARAM);
    }

    const cookieName = 'nwbloadurl';
    const nwbCookie = document.cookie.split(';').find(cookie => cookie.includes(cookieName))
    if (nwbCookie) {
      const [_, nwbFileUrl] = nwbCookie.replace(/"/g, '').split("=");
      if (nwbFileUrl) {
        document.cookie = `${cookieName}= ; path=/`;
        return nwbFileUrl;
      }
    }
    return null;
  }


  async loadNWBFile () {
    // GEPPETTO.trigger(GEPPETTO.Events.Show_spinner, "Loading NWB file");
    let responseJson = await fetch(GeppettoPathService.serverPath("/api/load/?nwbfile=" + this.nwbfile))
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Something went wrong');
        }
      })
      .catch(error => console.error(error));

    // GEPPETTO.trigger(GEPPETTO.Events.Hide_spinner);

    return responseJson;
  }

  async importValue (instance) {
    GEPPETTO.trigger(GEPPETTO.Events.Show_spinner, "Loading data for " + instance.getPath());
    let newModel = await fetch(GeppettoPathService.serverPath("/api/importvalue/?path=" + instance.getPath()))
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Something went wrong while retrieving ' + instance.getPath());
        }
      })
      .catch(error => console.error(error));
    GEPPETTO.trigger(GEPPETTO.Events.Hide_spinner);
    GEPPETTO.Manager.swapResolvedValue(newModel);
  }

  /**
   * Like importValue but it's not meant to update the model. Just returns the value
   * @param {} instance 
   */
  async retrieveValue (instance) {
    GEPPETTO.trigger(GEPPETTO.Events.Show_spinner, "Loading data for " + instance.getPath());
    let instanceValue = await fetch(GeppettoPathService.serverPath("/api/retrievevalue/?path=" + instance.getPath()))
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Something went wrong while retrieving ' + instance.getPath());
        }
      })
      .catch(error => console.error(error));
    GEPPETTO.trigger(GEPPETTO.Events.Hide_spinner);
    return instanceValue;
  }

  async loadNWBFileInNotebook (nwbFileUrl) {
    return await Utils.evalPythonMessage('main', [nwbFileUrl]);
  }

}

export const nwbFileService = new NWBFileService();

export default nwbFileService;