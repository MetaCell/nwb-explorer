const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
/*
 *var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
 * <%=htmlWebpackPlugin.options.GEPPETTO_CONFIGURATION._webapp_folder%>
 */
let geppettoConfig;
try {
  geppettoConfig = require('./GeppettoConfiguration.json');
  console.log('\nLoaded Geppetto config from file');
} catch (e) {
  // Failed to load config file
  console.error('\nFailed to load Geppetto Configuration');
}
const geppettoClientPath = 'node_modules/@metacell/geppetto-meta-client';
const geppettoCorePath = 'node_modules/@metacell/geppetto-meta-core';
const geppettoUIPath = 'node_modules/@metacell/geppetto-meta-ui';

const publicPath = path.join(geppettoConfig.contextPath, 'geppetto/build/');
console.log(`\nThe public path (used by the main bundle when including split bundles) is: ${publicPath}`);

const isProduction = process.argv.indexOf('-p') >= 0;
console.log(`\n Building for a ${(isProduction) ? 'production' : 'development'} environment`);

const availableExtensions = [
  {
    from: path.resolve(__dirname, geppettoClientPath, 'style/fonts/*'),
    to: 'static/fonts',
    flatten: true,
  },
  {
    from: path.resolve(__dirname, geppettoClientPath, 'style/css/font-awesome.min.css'),
    to: 'static/css',
  },
  {
    from: path.resolve(__dirname, geppettoClientPath, 'style/css/gpt-icons.css'),
    to: 'static/css',
  },
  {
    from: path.resolve(__dirname, geppettoClientPath, 'static/*'),
    to: 'static',
    flatten: true,
  },
  {
    from: path.resolve(__dirname, geppettoCorePath, 'static/*'),
    to: 'static',
    flatten: true,
  },
  {
    from: path.resolve(__dirname, geppettoUIPath, 'static/*'),
    to: 'static',
    flatten: true,
  },
  {
    from: path.resolve(__dirname, 'images/*'),
    to: '',
    flatten: true,
  },
  {
    from: path.resolve(__dirname, 'static'),
    to: 'static',
  },
];

module.exports = function (env) {
  // geppettoConfig._webapp_folder
  if (env != undefined) {
    console.log(env);
    if (env.contextPath) {
      geppettoConfig.contextPath = env.contextPath;
    }
    if (env.useSsl) {
      geppettoConfig.useSsl = JSON.parse(env.useSsl);
    }
    if (env.noTest) {
      geppettoConfig.noTest = JSON.parse(env.noTest);
    }
    if (env.embedded) {
      geppettoConfig.embedded = JSON.parse(env.embedded);
    }
    if (env.embedderURL) {
      geppettoConfig.embedderURL = env.embedderURL;
    }
  }

  console.log('Geppetto configuration \n');
  console.log(JSON.stringify(geppettoConfig, null, 2), '\n');

  const entries = { main: path.resolve(__dirname, 'Main.js'), };

  console.log('\nThe Webpack entries are:');
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
            enforce: true, // form this chunk irrespective of the size of the chunk
          },
        },
      },
    },

    output: {
      path: path.resolve(__dirname, 'build'),
      filename: '[name].bundle.js',
      publicPath,
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
        template: path.resolve(__dirname, 'geppetto.ejs'),
        GEPPETTO_CONFIGURATION: geppettoConfig,
        /*
         * chunks: ['main'] Not specifying the chunk since its not possible
         * yet (need to go to Webpack2) to specify UTF-8 as charset without
         * which we have errors
         */
        chunks: [],
      }),

      new webpack.DefinePlugin({ 'process.env': { NODE_ENV: JSON.stringify(isProduction ? 'production' : 'development') } }),
      new MiniCssExtractPlugin({ filename: '[name].css' }),
    ],

    resolve: {
      alias: {
        root: path.resolve(__dirname),
        'geppetto-client': path.resolve(__dirname, geppettoClientPath),
        'geppetto-core': path.resolve(__dirname, geppettoCorePath),
        'geppetto-ui': path.resolve(__dirname, geppettoUIPath),
        geppetto: path.resolve(__dirname, geppettoClientPath, 'pages/geppetto/GEPPETTO.js'),
        'geppetto-client-initialization': path.resolve(__dirname, geppettoClientPath, 'pages/geppetto/main.js'),
        handlebars: 'handlebars/dist/handlebars.js',
      },
      extensions: ['*', '.js', '.json', '.ts', '.tsx', '.jsx'],
    },

    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                '@babel/preset-env',
                '@babel/preset-react',
              ],
              plugins: [
                '@babel/plugin-syntax-dynamic-import',
                '@babel/plugin-proposal-class-properties',
              ],
            },
          },
        },
        {
          test: /\.tsx?$/,
          loader: 'awesome-typescript-loader',
        },
        {
          test: /Dockerfile/,
          loader: 'ignore-loader',
        },
        {
          test: /\.(py|jpeg|svg|gif|css|md|hbs|dcm|gz|xmi|dzi|sh|obj|yml|nii)$/,
          loader: 'ignore-loader',
        },
        {
          test: /\.(png|jpg|eot|ttf|woff|woff2|svg)(\?[a-z0-9=.]+)?$/,
          loader: 'url-loader?limit=100000',
        },
        {
          test: /\.css$/,
          use: [
            { loader: MiniCssExtractPlugin.loader },
            { loader: 'css-loader' },
          ],
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
          loader: 'raw-loader',
        },
      ],
    },
    node: {
      fs: 'empty',
      child_process: 'empty',
      module: 'empty',
    },
  };
};
