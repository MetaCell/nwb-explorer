/**
 *|--------------------------------------------------
 *| sudo npm install -g eslint babel-eslint
 *|--------------------------------------------------
 */
module.exports = {
  extends: [
    "eslint:recommended",
  ],
  env: {
    browser: true,
    commonjs: true,
    es6: true,
    node: true,
    jquery: true,
    amd: true,
    mocha: true,
    jasmine: true,
    phantomjs: true,
    worker: true,
    jest: true
  },
  parser: "babel-eslint",
  parserOptions: {
    "sourceType": "module", // import export syntax
    "ecmaVersion": 2017 // async await syntax
  },
  rules: { // 0: allow, 1: warning, 2: error
    "no-tabs": 2, // no tabs in code
    "no-empty": 0,
    'no-console': 0,
    "curly": 2,
    "no-global-assign": 0, // allow global variables to be modified
    "no-constant-condition": 0, // allow:    while(true) { ... }
    "no-control-regex": 0, // allow regex
    "no-redeclare": 0, // allow redeclare a variable
    "no-inner-declarations": 0, // allow define functions inside functions
    "indent": ["error", 2, {
      "ObjectExpression": "first",
      "ArrayExpression": "first"
    }], // 2 spaces for indentation and consistent alignment
    "arrow-spacing": 2,
    "no-unused-vars": 0,
    "keyword-spacing": 2,
    "no-useless-escape": 0,
    "brace-style": 2, // enforce open bracket in same line
    "multiline-comment-style": [2, "starred-block"], // enforce commented block style
    "object-curly-newline": [2, { "multiline": true }], // enforce  obj items identation
    "operator-linebreak": [2, "before"], // break operator to new line
    "space-infix-ops": 2, 
    "no-multi-spaces": 2,
    "no-unneeded-ternary": 2,
    "no-multiple-empty-lines": 2,
    "spaced-comment": [2, "always"],
    "arrow-parens": [2, "as-needed"],
    "arrow-body-style": [2, "as-needed"],
    "object-curly-spacing": [2, "always"],
    "template-curly-spacing": [2, "never"],
    "space-before-function-paren": [1, "always"]
  },
  globals: {
    "G": true,
    "root": true,
    "casper": true,
    "message": true,
    "endpoint": true,
    "GEPPETTO": true,
    "gepetto-client": true,
    "Project": true,
    "Instances": true,
    "IPython": true,
    "GEPPETTO_CONFIGURATION": true,
    "MozWebSocket": true,
    "panelComponent": true,
    "Detector": true,
    "THREE": true,
    "VARS": true,
    "Stats": true,
    "geometry": true,
    "aabbMin": true,
    "aabbMax": true,
    "bb": true,
    "ClipboardModal": true,
    "Store": true,
    "olark": true,
    "google": true,
    "path": true,
    "CodeMirror": true,
    "Connectivity": true,
    "π": true,
    "τ": true,
    "halfπ": true,
    "dr": true,
    "Model": true,
    "Plot1": true,
    "PIXI": true,
    "stackViewerRequest": true,
    "_": true,
    "labelsInTV": true,
    "Backbone": true,
    "registeredEvents": true,
    "Handlebars": true,
    "ActiveXObject": true,
    "jstestdriver": true,
    "TestCase": true,
    "EMBEDDED": true,
    "EMBEDDERURL": true,
    "handleRequest": true,
    "_gaq": true,
    "Canvas1": true,
    "clientX": true,
    "clientY": true,
  }
};