import Ajv from 'ajv'
import exampleLabware1 from './example.json'
import exampleLabware2 from './example2.json'
import labwareSchema from '../../../labware-json-schema/labware-schema.json'
import omit from 'lodash/omit'
import range from 'lodash/range'
import {createRegularLabware} from '../index.js'

jest.mock('../assignId', () => jest.fn(() => 'mock-id'))

const ajv = new Ajv({
  allErrors: true,
  jsonPointers: true,
})

const validate = ajv.compile(labwareSchema)

describe('createLabware', () => {
  let labware1
  let labware2
  let well1
  let well2

  beforeEach(() => {
    well1 = omit(exampleLabware1.wells.A1, ['x', 'y', 'z'])
    well2 = omit(exampleLabware2.wells.A1, ['x', 'y', 'z'])

    labware1 = createRegularLabware({
      metadata: exampleLabware1.metadata,
      parameters: exampleLabware1.parameters,
      dimensions: exampleLabware1.dimensions,
      grid: [1, 2],
      spacing: [10, 10],
      well: well1,
      vendor: exampleLabware1.vendor,
    })

    labware2 = createRegularLabware({
      metadata: exampleLabware2.metadata,
      parameters: exampleLabware2.parameters,
      dimensions: exampleLabware2.dimensions,
      grid: [3, 2],
      spacing: [9, 9],
      well: well2,
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('snapshot tests', () => {
    expect(labware1).toMatchSnapshot()
    expect(labware2).toMatchSnapshot()
  })

  test('generated labware passes schema', () => {
    const valid = validate(exampleLabware1)
    const validationErrors = validate.errors

    expect(validationErrors).toBe(null)
    expect(valid).toBe(true)
  })

  test('id is from assignId', () => {
    expect(labware1.otId).toBe('mock-id')
    expect(labware2.otId).toBe('mock-id')
  })

  test('ordering generates as expected', () => {
    expect(exampleLabware2.ordering).toEqual(labware2.ordering)
  })

  test('well XYZ generates correctly', () => {
    const spacing = [11.8, 12.1]
    const grid = [8, 12]

    const labware3 = createRegularLabware({
      metadata: exampleLabware2.metadata,
      paramenters: exampleLabware2.parameters,
      dimensions: exampleLabware2.dimensions,
      grid,
      spacing,
      well: well2,
    })

    const expectedXByCol = range(0, grid[1] * spacing[1], spacing[1])
    const expectedYByRow = range(0, grid[0] * spacing[0], spacing[0]).reverse()

    labware3.ordering.forEach((column, cIndex) => {
      column.forEach((wellName, rIndex) => {
        const well = labware3.wells[wellName]
        expect(well.x).toBeCloseTo(expectedXByCol[cIndex], 2)
        expect(well.y).toBeCloseTo(expectedYByRow[rIndex], 2)
        expect(well.z).toBeCloseTo(0, 2)
      })
    })
  })
})
