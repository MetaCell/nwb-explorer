var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
/*
 *var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
 * <%=htmlWebpackPlugin.options.GEPPETTO_CONFIGURATION._webapp_folder%>
 */
var geppettoConfig;
try {
  geppettoConfig = require('./GeppettoConfiguration.json');
  console.log('\nLoaded Geppetto config from file');
} catch (e) {
  // Failed to load config file
  console.error('\nFailed to load Geppetto Configuration')
}
var geppetto_client_path = 'node_modules/@geppettoengine/geppetto-client'

var publicPath = path.join(geppettoConfig.contextPath, "geppetto/build/");
// var publicPath = ((geppettoConfig.contextPath == '/') ? '' : geppettoConfig.contextPath + "/") + "geppetto/build/";


console.log("\nThe public path (used by the main bundle when including split bundles) is: " + publicPath);

var isProduction = process.argv.indexOf('-p') >= 0;
console.log("\n Building for a " + ((isProduction) ? "production" : "development") + " environment")

const availableExtensions = [
  { from: path.resolve(__dirname, geppetto_client_path, "static/*"), to: 'static', flatten: true },
];

module.exports = function (env){
  // geppettoConfig._webapp_folder
  if (env != undefined){
    console.log(env);
    if (env.contextPath){
      geppettoConfig.contextPath = env.contextPath;
    }
    if (env.useSsl){
      geppettoConfig.useSsl = JSON.parse(env.useSsl);
    }
    if (env.noTest){
      geppettoConfig.noTest = JSON.parse(env.noTest);
    }
    if (env.embedded){
      geppettoConfig.embedded = JSON.parse(env.embedded);
    }
    if (env.embedderURL){
      geppettoConfig.embedderURL = env.embedderURL;
    }
  }

  console.log('Geppetto configuration \n');
  console.log(JSON.stringify(geppettoConfig, null, 2), '\n');
  
  var entries = {
    main: path.resolve(__dirname, "Main.js"),
    admin: path.resolve(__dirname, geppetto_client_path, "js/pages/admin/admin.js"),
  };

  console.log("\nThe Webpack entries are:");
  console.log(entries);
  
  return {
    entry: entries,
    
    output: {
      path: path.resolve(__dirname, 'build'),
      filename: '[name].bundle.js',
      publicPath: publicPath
    },
    plugins: [
      /*
       * new BundleAnalyzerPlugin({
       *     analyzerMode: 'static'
       * }),
       */
      new webpack.optimize.CommonsChunkPlugin(['common']),
      new CopyWebpackPlugin(availableExtensions),
      new HtmlWebpackPlugin({
        filename: 'geppetto.vm',
        template: path.resolve(__dirname, geppetto_client_path, 'js/pages/geppetto/geppetto.ejs'),
        GEPPETTO_CONFIGURATION: geppettoConfig,
        /*
         * chunks: ['main'] Not specifying the chunk since its not possible
         * yet (need to go to Webpack2) to specify UTF-8 as charset without
         * which we have errors
         */
        chunks: []
      }),
      /*
       * new HtmlWebpackPlugin({
       *   filename: 'admin.vm',
       *   template: path.resolve(__dirname, geppetto_client_path, 'js/pages/admin/admin.ejs'),
       *   GEPPETTO_CONFIGURATION: geppettoConfig,
       *   
       *    * chunks: ['admin'] Not specifying the chunk since its not possible
       *    * yet (need to go to Webpack2) to specify UTF-8 as charset without
       *    * which we have errors
       *    
       *   chunks: []
       * }),
       * new HtmlWebpackPlugin({
       *   filename: 'dashboard.vm',
       *   template: path.resolve(__dirname, geppetto_client_path, 'js/pages/dashboard/dashboard.ejs'),
       *   GEPPETTO_CONFIGURATION: geppettoConfig,
       *   chunks: []
       * }),
       *
       * new HtmlWebpackPlugin({
       *   filename: '../WEB-INF/web.xml',
       *   template: path.resolve(__dirname, 'WEB-INF/web.ejs'),
       *   GEPPETTO_CONFIGURATION: geppettoConfig,
       *   chunks: []
       * }),
       */
      new webpack.DefinePlugin({ 'process.env': { 'NODE_ENV': JSON.stringify(isProduction ? 'production' : 'development'), } }),
      new ExtractTextPlugin("[name].css"),
    ],
      
    resolve: {
      alias: {
        root: path.resolve(__dirname),
        'geppetto-client': path.resolve(__dirname, geppetto_client_path),
        geppetto: path.resolve(__dirname, geppetto_client_path, 'js/pages/geppetto/GEPPETTO.js'),
        'geppetto-client-initialization': path.resolve(__dirname, geppetto_client_path, 'js/pages/geppetto/main'),
        handlebars: 'handlebars/dist/handlebars.js'
  
      },
      extensions: ['*', '.js', '.json', '.ts', '.tsx', '.jsx'],
    },
  
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: [/ami.min.js/, /node_modules\/(?!(@geppettoengine\/geppetto-client)\/).*/], 
          loader: 'babel-loader',
          query: { presets: [['babel-preset-env', { "modules": false }], 'stage-2', 'react'] }
        },
        // All files with a '.ts' or '.tsx' extension will be handled by 'awesome-typescript-loader'.
        {
          test: /\.tsx?$/,
          loader: "awesome-typescript-loader"
        },
        {
          test: /Dockerfile/,
          loader: 'ignore-loader'
        },
        {
          test: /\.(py|svg|gif|css|md|hbs|dcm|gz|xmi|dzi|sh|obj|yml|nii)$/,
          loader: 'ignore-loader'
        },
        {
          test: /\.(jpg|png|eot|ttf|woff|woff2|svg)(\?[a-z0-9=.]+)?$/,
          loader: 'url-loader?limit=100000'
        },
        {
                  
          test: /\.css$/,
          use: ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: "css-loader"
          })
                    
        },
        {
          test: /\.less$/,
          loader: 'style-loader!css-loader!less-loader?{"modifyVars":{"url":"\'' + path.resolve(__dirname, geppettoConfig.themes) + '\'"}}'
        },
        {
          test: /\.html$/,
          loader: 'raw-loader'
        }
      ]
    },
    node: {
      fs: 'empty',
      child_process: 'empty',
      module: 'empty'
    }
  }
};
