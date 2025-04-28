const firebase = require('firebase/app');
require('firebase/database');

// You can populate this config with your real project settings after cloning.
// They can also be provided via environment variables for security.
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || '<api-key>',
  authDomain: process.env.FIREBASE_AUTH_DOMAIN || '<project-id>.firebaseapp.com',
  databaseURL: process.env.FIREBASE_DATABASE_URL || 'https://<project-id>.firebaseio.com',
  projectId: process.env.FIREBASE_PROJECT_ID || '<project-id>',
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET || '<project-id>.appspot.com',
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID || '<sender-id>',
  appId: process.env.FIREBASE_APP_ID || '<app-id>'
};

const app = firebase.initializeApp(firebaseConfig);
const db = app.database();

module.exports = db;
