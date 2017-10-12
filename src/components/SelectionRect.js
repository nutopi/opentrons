import React from 'react'
import PropTypes from 'prop-types'

class SelectionRect extends React.Component {
  constructor (props) {
    super(props)
    this.state = { positions: null }

    this.handleMouseDown = this.handleMouseDown.bind(this)
    this.handleDrag = this.handleDrag.bind(this)
    this.handleMouseUp = this.handleMouseUp.bind(this)
  }

  renderRect ({xStart, yStart, xDynamic, yDynamic}) {
    return <div
      style={{
        position: 'fixed',
        zIndex: 1000,
        borderRadius: 0,
        left: Math.min(xStart, xDynamic) + 'px',
        top: Math.min(yStart, yDynamic) + 'px',
        width: Math.abs(xDynamic - xStart) + 'px',
        height: Math.abs(yDynamic - yStart) + 'px',
        backgroundColor: 'rgba(0, 0, 255, 0.5)' // <- TODO: use css for colors
      }}
      onMouseMove={e => console.log('mousemove', e.clientX, e.clientY)}
    />
  }

  getRect ({xStart, yStart, xDynamic, yDynamic}) {
    // convert internal rect position to more generic form
    return {
      x0: Math.min(xStart, xDynamic),
      x1: Math.max(xStart, xDynamic),
      y0: Math.min(yStart, yDynamic),
      y1: Math.max(yStart, yDynamic)
    }
  }

  handleMouseDown (e) {
    window.addEventListener('mousemove', this.handleDrag)
    window.addEventListener('mouseup', this.handleMouseUp)
    this.setState({ positions: {xStart: e.clientX, xDynamic: e.clientX, yStart: e.clientY, yDynamic: e.clientY} })
  }

  handleDrag (e) {
    this.setState({ positions: {...this.state.positions, xDynamic: e.clientX, yDynamic: e.clientY} })

    this.props.onSelectionMove &&
      this.props.onSelectionMove(this.getRect(this.state.positions))
  }

  handleMouseUp (e) {
    window.removeEventListener('mousemove', this.handleDrag)
    window.removeEventListener('mouseup', this.handleMouseUp)

    // call onSelectionDone callback with {x0, x1, y0, y1} of selection rectangle
    this.props.onSelectionDone &&
      this.props.onSelectionDone(this.getRect(this.state.positions))
    // then clear the rectangle
    this.setState({ positions: null })
  }

  render () {
    const { children } = this.props
    return (
      <div onMouseDown={this.handleMouseDown}>
        {this.state.positions && this.renderRect(this.state.positions)}
        {children}
      </div>
    )
  }
}

SelectionRect.propTypes = {
  onSelectionMove: PropTypes.func,
  onSelectionDone: PropTypes.func,
  children: PropTypes.element
}

export default SelectionRect
