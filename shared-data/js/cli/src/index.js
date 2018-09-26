// @flow
import getLabware from '../../getLabware'

// This is a simple proof-of-concept example
// try `node shared-data/js/cli/dist/bundle.js 96-flat`
const labwareName = process.argv[2]

console.log(getLabware(labwareName))

// exports as a convenience for node REPL use in development
export {
  getLabware,
}
