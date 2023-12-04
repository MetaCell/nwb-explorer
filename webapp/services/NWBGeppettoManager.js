

/**
 * Override standard Manager
 *
 */
export async function resolveImportValue (typePath, callback) {
  const params = {};
  params.experimentId = -1;
  params.projectId = Project.getId();
  // replace client naming first occurrence - the server doesn't know about it
  params.path = typePath.replace(`${GEPPETTO.Resources.MODEL_PREFIX_CLIENT}.`, '');

  const requestID = GEPPETTO.MessageSocket.send('resolve_import_value', params, callback);

  GEPPETTO.trigger('spin_logo');
}

