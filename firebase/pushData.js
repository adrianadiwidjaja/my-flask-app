const db = require('./firebase');

/**
 * Pushes a data object to the `data_flow` path in Firebase.
 * @param {Object} payload data that will be written.
 * @returns {Promise<firebase.database.Reference>} a promise resolving when data was pushed.
 */
function pushToDataFlow(payload) {
  return db.ref('data_flow').push(payload);
}
module.exports = pushToDataFlow;
