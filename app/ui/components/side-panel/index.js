// side nav panel container
import React from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'

import {
  PANEL_NAMES,
  PANEL_PROPS_BY_NAME,
  actions as interfaceActions,
  selectors as interfaceSelectors
} from '../../interface'

import SidePanel from './SidePanel'
// TODO (ka 2017-12-5) refactor individual panels in subsequent PRs
// naming and organization refactors to follow
import Connection from '../../containers/Connection'
import UploadProtocol from '../../containers/UploadProtocol'
import ConnectedSetupPanel from '../../containers/ConnectedSetupPanel'

export default connect(mapStateToProps, mapDispatchToProps)(NavPanel)

const PANELS_BY_NAME = {
  connect: Connection,
  upload: UploadProtocol,
  setup: ConnectedSetupPanel
}

NavPanel.propTypes = {
  panel: PropTypes.oneOf(PANEL_NAMES).isRequired,
  isOpen: PropTypes.bool.isRequired,
  close: PropTypes.func.isRequired
}

function NavPanel (props) {
  const {panel, isOpen, close} = props
  const PanelContents = PANELS_BY_NAME[panel]
  const panelProps = PANEL_PROPS_BY_NAME[panel]

  return (
    <SidePanel isOpen={isOpen} close={close} title={panelProps.title}>
      <PanelContents />
    </SidePanel>
  )
}

function mapStateToProps (state) {
  return {
    isOpen: interfaceSelectors.getIsPanelOpen(state),
    panel: interfaceSelectors.getCurrentPanel(state)
  }
}

function mapDispatchToProps (dispatch) {
  return {
    close: () => dispatch(interfaceActions.closePanel())
  }
}
