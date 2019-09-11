function pathjoin (...paths) {
  return paths.join('/').replace('//', '/')
}

function getBasePath (fullPath) {
  return pathjoin(...fullPath.split('/').slice(0, -1));
}

const contextPath = GEPPETTO_CONFIGURATION.contextPath;
const basePath = getBasePath(window.location.pathname);
const baseUrl = getBasePath(window.location.href);

function staticPath (applicationPath) {
  return pathjoin(basePath, contextPath, applicationPath);
}

function serverPath (applicationPath) {
  return pathjoin(basePath, applicationPath);
}

const GeppettoPathService = {
  staticPath: staticPath,
  serverPath: serverPath
}

export default GeppettoPathService;
