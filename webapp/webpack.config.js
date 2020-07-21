var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var MiniCssExtractPlugin = require("mini-css-extract-plugin");
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
var geppetto_base_path = 'node_modules/@geppettoengine/geppetto-client'

var publicPath = path.join(geppettoConfig.contextPath, "geppetto/build/");
console.log("\nThe public path (used by the main bundle when including split bundles) is: " + publicPath);

var isProduction = process.argv.indexOf('-p') >= 0;
console.log("\n Building for a " + ((isProduction) ? "production" : "development") + " environment")

const availableExtensions = [
  { from: path.resolve(__dirname, geppetto_base_path, "static/*"), to: 'static', flatten: true },
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
    admin: path.resolve(__dirname, geppetto_base_path, "js/pages/admin/admin.js"),
  };

  console.log("\nThe Webpack entries are:");
  console.log(entries);
  
  return {
    entry: entries,
    
    optimization: {
      splitChunks: {
        cacheGroups: {
          commons: {
            name: 'common',                   
            minChunks: 2, // Minimum # of chunks which need to contain a module before it's moved into the commons chunk.
            chunks: 'initial', // initial, async or all
            reuseExistingChunk: true, // use existing chunk if available instead of creating new one
            enforce: true // form this chunk irrespective of the size of the chunk
          }
        }
      }
    },
      
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
      new CopyWebpackPlugin(availableExtensions),
      new HtmlWebpackPlugin({
        filename: 'geppetto.vm',
        template: path.resolve(__dirname, geppetto_base_path, 'geppetto-client/js/pages/geppetto/geppetto.ejs'),
        GEPPETTO_CONFIGURATION: geppettoConfig,
        /*
         * chunks: ['main'] Not specifying the chunk since its not possible
         * yet (need to go to Webpack2) to specify UTF-8 as charset without
         * which we have errors
         */
        chunks: []
      }),
      // new HtmlWebpackPlugin({
      //   filename: 'admin.vm',
      //   template: path.resolve(__dirname, geppetto_client_path, 'js/pages/admin/admin.ejs'),
      //   GEPPETTO_CONFIGURATION: geppettoConfig,
      //   /*
      //    * chunks: ['admin'] Not specifying the chunk since its not possible
      //    * yet (need to go to Webpack2) to specify UTF-8 as charset without
      //    * which we have errors
      //    */
      //   chunks: []
      // }),
      // new HtmlWebpackPlugin({
      //   filename: 'dashboard.vm',
      //   template: path.resolve(__dirname, geppetto_client_path, 'js/pages/dashboard/dashboard.ejs'),
      //   GEPPETTO_CONFIGURATION: geppettoConfig,
      //   chunks: []
      // }),
      // new HtmlWebpackPlugin({
      //   filename: '../WEB-INF/web.xml',
      //   template: path.resolve(__dirname, 'WEB-INF/web.ejs'),
      //   GEPPETTO_CONFIGURATION: geppettoConfig,
      //   chunks: []
      // }),
      new webpack.DefinePlugin({ 'process.env': { 'NODE_ENV': JSON.stringify(isProduction ? 'production' : 'development'), } }),
      new MiniCssExtractPlugin({ filename: '[name].css' })
    ],
      
    resolve: {
      alias: {
        root: path.resolve(__dirname),
        '@geppettoengine/geppetto-client': path.resolve(__dirname, geppetto_base_path + '/geppetto-client'),
        '@geppettoengine/geppetto-ui': path.resolve(__dirname, geppetto_base_path + '/geppetto-ui'),
        '@geppettoengine/geppetto-core': path.resolve(__dirname, geppetto_base_path + '/geppetto-core'),
        geppetto: path.resolve(__dirname, geppetto_base_path, 'js/pages/geppetto/GEPPETTO.js'),
        '@geppettoengine/geppetto-client-initialization': path.resolve(__dirname, geppetto_base_path, 'js/pages/geppetto/main'),
        handlebars: 'handlebars/dist/handlebars.js'
      },
      extensions: ['*', '.js', '.json', '.ts', '.tsx', '.jsx'],
    },
  
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: [/ami.min.js/, /node_modules\/(?!(@geppettoengine\/geppetto-client)\/).*/], 
          use: {
            loader: "babel-loader",
            options: { 
              presets: [
                '@babel/preset-env',
                '@babel/preset-react'
              ],
              plugins: [
                "@babel/plugin-syntax-dynamic-import",
                "@babel/plugin-proposal-class-properties"
              ]
            }
          }
        },
        {
          test: /\.tsx?$/,
          loader: "awesome-typescript-loader"
        },
        {
          test: /Dockerfile/,
          loader: 'ignore-loader'
        },
        {
          test: /\.(py|jpeg|svg|gif|css|md|hbs|dcm|gz|xmi|dzi|sh|obj|yml|nii)$/,
          loader: 'ignore-loader'
        },
        {
          test: /\.(png|jpg|eot|ttf|woff|woff2|svg)(\?[a-z0-9=.]+)?$/,
          loader: 'url-loader?limit=100000'
        },
        {
          test: /\.css$/,
          use: [
            { loader: MiniCssExtractPlugin.loader },
            { loader: "css-loader" }
          ]
        },
        {
          test: /\.less$/,
          use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' },
            {
              loader: 'less-loader',
              options: { modifyVars: { url: path.resolve(__dirname, geppettoConfig.themes) } },
            },
          ],
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