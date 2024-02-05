const webpackBaseConfig = require('./webpack.config.js');

const extended = webpackBaseConfig();

extended.devServer = {

  port: 8081,

  static: '/geppetto/build',

  headers: {
    // Set Content-Security-Policy header to allow only self as frame ancestor
    "Content-Security-Policy": "frame-ancestors '*' 'wsl.localhost' 'localhost'"
  },
  proxy: [
    {
      path: '/',
      target: 'http://localhost:8888',
    },
    {
      path: '/org.geppetto.frontend',
      target: 'ws://localhost:8888',
      ws: true,
    },
    {
      path: '/notebooks',
      target: 'http://localhost:8888',
    },
    {
      path: '/api',
      target: 'http://localhost:8888',
    },
    {
      path: '/api/kernels',
      target: 'ws://localhost:8888',
      ws: true,
    },
    {
      path: '/static',
      target: 'http://localhost:8888',
    },
    {
      path: '/custom',
      target: 'http://localhost:8888',
    },

    {
      path: '/nbextensions',
      target: 'http://localhost:8888',
    },
  ],
};

extended.optimization = {
  ...extended.optimization,
  removeAvailableModules: false,
  removeEmptyChunks: false,
};

extended.devtool = 'source-map';

module.exports = extended;
