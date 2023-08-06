(self["webpackChunk_epi2melabs_jupyterlab_autorun_cells"] = self["webpackChunk_epi2melabs_jupyterlab_autorun_cells"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Extension constants
 */
const AUTORUN_ENABLED_CLASS = 'epi2melabs-autorun-enabled';
const EXT_NAME = 'epi2melabs-autorun';
const AUTORUN = 'autorun';
const MARKDOWN = 'markdown';
const CODE = 'code';
/**
 * Helper method
 */
const toggleAutorun = (tracker) => {
    const cell = tracker.activeCell;
    const metadata = cell.model.metadata;
    if (!!metadata.get(AUTORUN)) {
        cell.model.metadata.set(AUTORUN, false);
        cell.removeClass(AUTORUN_ENABLED_CLASS);
        return;
    }
    cell.model.metadata.set(AUTORUN, true);
    cell.addClass(AUTORUN_ENABLED_CLASS);
};
/**
 * Initialization data for the extension.
 */
const extension = {
    id: EXT_NAME,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    autoStart: true,
    activate: (app, nbTrack) => {
        const command1 = `${EXT_NAME}:toggle_autorun`;
        app.commands.addCommand(command1, {
            label: 'Toggle autorun cell at launch',
            execute: () => {
                toggleAutorun(nbTrack);
            }
        });
        app.contextMenu.addItem({
            command: `${EXT_NAME}:toggle_autorun`,
            selector: '.jp-Cell',
            rank: 0
        });
        nbTrack.currentChanged.connect(() => {
            const nbIDs = [];
            const notebookPanel = nbTrack.currentWidget;
            const notebook = nbTrack.currentWidget.content;
            notebook.model.stateChanged.connect(async () => {
                if (notebook.widgets.length > 1) {
                    const currentId = notebookPanel.id;
                    if (nbIDs.includes(currentId)) {
                        return;
                    }
                    nbIDs.push(notebookPanel.id);
                    notebookPanel.context.ready.then(() => {
                        return notebookPanel.sessionContext.ready;
                    }).then(async () => {
                        notebook.widgets.map((cell) => {
                            const metadata = cell.model.metadata;
                            if (!!metadata.get(AUTORUN)) {
                                cell.addClass(AUTORUN_ENABLED_CLASS);
                                switch (cell.model.type) {
                                    case CODE:
                                        _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell.execute(cell, notebookPanel.sessionContext, {
                                            recordTiming: notebook.notebookConfig.recordTiming
                                        });
                                        break;
                                    case MARKDOWN:
                                        cell.rendered = true;
                                        break;
                                    default:
                                        break;
                                }
                            }
                        });
                    });
                }
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.0543661bfae35f8d7291.js.map