import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { AppContainer } from 'react-hot-loader'

import configureStore from './configureStore.js'
import i18n from './localization'
import App from './components/App'
import {selectors as loadFileSelectors} from './load-file'
const store = configureStore()

if (process.env.NODE_ENV === 'production') {
  window.onbeforeunload = (e) => {
    // NOTE: the custom text will be ignored in modern browsers
    return loadFileSelectors.hasUnsavedChanges(store.getState()) ? i18n.t('alert.window.confirm_leave') : undefined
  }
}

const render = (Component) => {
  ReactDOM.render(
    <Provider store={store}>
      <AppContainer>
        <Component />
      </AppContainer>
    </Provider>,
    document.getElementById('root')
  )
}

render(App)

// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('./components/App', () => {
    render(App)
  })
}
