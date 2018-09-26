'use strict'

const path = require('path')
// const webpack = require('webpack')

const {rules} = require('@opentrons/webpack-config')

// const DEV = process.env.NODE_ENV !== 'production'

const pathToCli = path.join(__dirname, 'js', 'cli')

module.exports = {
  entry: [
    path.join(pathToCli, 'src', 'index.js'),
  ],

  plugins: [],

  target: 'node',

  output: {
    filename: 'bundle.js',
    path: path.join(pathToCli, 'dist'),
    // NOTE: umd build is for dev convenience, using node REPL.
    // Not intended to be published at this time
    library: 'shared-data-cli',
    libraryTarget: 'umd',
  },

  module: {
    rules: [
      rules.js,
    ],
  },
}
