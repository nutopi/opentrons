'use strict'

const path = require('path')
const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const {rules} = require('@opentrons/webpack-config')

const DEV = process.env.NODE_ENV !== 'production'

module.exports = {
  entry: [
    './src/index.js',
  ],

  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
  },

  module: {
    rules: [
      rules.js,
      rules.localCss,
      rules.handlebars,
    ],
  },

  devServer: {
    historyApiFallback: true,
  },

  devtool: DEV ? 'eval-source-map' : 'source-map',

  plugins: [
    new ExtractTextPlugin({
      filename: 'bundle.css',
      disable: DEV,
      ignoreOrder: true,
    }),
    new HtmlWebpackPlugin({
      title: 'Opentrons Labware Designer',
      template: './src/index.hbs',
    }),
  ],
}

if (DEV) {
  // module.exports.entry.unshift(
  //   'react-hot-loader/patch'
  // )

  module.exports.plugins.push(
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.NamedModulesPlugin()
  )
}
