/**
 * Copyright 2023 Agnostiq Inc.
 *
 * This file is part of Covalent.
 *
 * Licensed under the GNU Affero General Public License 3.0 (the "License").
 * A copy of the License may be obtained with this software package or at
 *
 *      https://www.gnu.org/licenses/agpl-3.0.en.html
 *
 * Use of this file is prohibited except in compliance with the License. Any
 * modifications or derivative works of this file must retain this copyright
 * notice, and modified files must contain a notice indicating that they have
 * been altered from the originals.
 *
 * Covalent is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
 *
 * Relief from the License may be granted by purchasing a commercial license.
 */
import { screen, render } from '@testing-library/react'
import App from '../Executor'
import { BrowserRouter } from 'react-router-dom'
import React from 'react'
import { Provider } from 'react-redux'
import reducers from '../../../redux/reducers'
import { configureStore } from '@reduxjs/toolkit'
import theme from '../../../utils/theme'
import ThemeProvider from '@mui/system/ThemeProvider'

function reduxRender(renderedComponent) {
    const store = configureStore({
        reducer: reducers,
    })

    return render(
        <Provider store={store}>
            <ThemeProvider theme={theme}>
                <BrowserRouter>{renderedComponent}</BrowserRouter>
            </ThemeProvider>
        </Provider>
    )
}

describe('Executor Tab', () => {
    const code = {
        "name": "Simulator",
        "executor": {
            "persist_data": true,
            "qnode_device_import_path": "pennylane.devices.default_qubit:DefaultQubit",
            "qnode_device_shots": null,
            "qnode_device_wires": 4,
            "pennylane_active_return": true,
            "device": "default.qubit",
            "parallel": "thread",
            "workers": 10,
            "shots": 0,
            "name": "Simulator",
            "_backend": {
                "persist_data": true,
                "qnode_device_import_path": "pennylane.devices.default_qubit:DefaultQubit",
                "qnode_device_shots": null,
                "qnode_device_wires": 4,
                "pennylane_active_return": true,
                "device": "default.qubit",
                "num_threads": 10,
                "name": "BaseThreadPoolQExecutor"
            }
        }
    }
    test('executor tab is rendered', () => {
        reduxRender(<App />)
        const linkElement = screen.getByTestId('Executor-grid')
        expect(linkElement).toBeInTheDocument()
    })

    test('checks rendering for executor code block', () => {
        reduxRender(<App code={code} />)
        const linkElement = screen.getByTestId('syntax')
        expect(linkElement).toBeInTheDocument()
    })
})
