(self["webpackChunk_epi2melabs_jupyterlab_play_cell_button"] = self["webpackChunk_epi2melabs_jupyterlab_play_cell_button"] || []).push([["lib_index_js"],{

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
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");


/**
 * Initialization data for the jupyterlab-play-cell-button extension.
 */
const extension = {
    id: 'jupyterlab-play-cell-button',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, nbTrack) => {
        nbTrack.currentChanged.connect(() => {
            const notebookPanel = nbTrack.currentWidget;
            const notebook = nbTrack.currentWidget.content;
            notebookPanel.context.ready.then(async () => {
                let currentCell = null;
                let currentCellPlayButton = null;
                nbTrack.activeCellChanged.connect(() => {
                    // Remove the existing play button from
                    // the previously active cell. This may
                    // well introduce bugs down the road and
                    // there is likely a better way to do this
                    if (currentCell) {
                        notebook.widgets.map((c) => {
                            const currentLayout = c.layout;
                            currentLayout.widgets.map(w => {
                                if (w === currentCellPlayButton) {
                                    currentLayout.removeWidget(w);
                                }
                            });
                        });
                    }
                    const cell = notebook.activeCell;
                    const newButton = new _widget__WEBPACK_IMPORTED_MODULE_1__.CellPlayButton(cell, notebookPanel.sessionContext);
                    cell.layout.addWidget(newButton);
                    // Set the current cell and button for future
                    // reference
                    currentCell = cell;
                    currentCellPlayButton = newButton;
                });
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellPlayButton": () => (/* binding */ CellPlayButton)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);




const PlayButton = ({ icon, onClick }) => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("button", { type: "button", onClick: () => onClick(), className: "cellPlayButton" },
    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon.resolveReact, { icon: icon, className: "cellPlayButton-icon", tag: "span", width: "15px", height: "15px" })));
/**
 * makeCancelable
 *
 * Note: Permits a Promise to be cancelled rather than to execute a
 * chained .then callback which is necessary if the component
 * has been unmounted
 *
 * Lifted from the long running discussion here:
 * https://github.com/facebook/react/issues/5465#issuecomment-157888325
 *
 * @param promise - The Promise to make cancellable.
 */
function makeCancelable(promise) {
    let active = true;
    return {
        cancel() { active = false; },
        promise: promise.then(value => active ? value : new Promise(() => { }), reason => active ? reason : new Promise(() => { }))
    };
}
const CodeCellPlayButtonComponent = ({ cell, session, }) => {
    // A hacky way to find out if we're currently running
    // anything, but doesn't matter greatly because the status
    // will soon be updated by the returned kernel future promise
    const [isRunning, setIsRunning] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(!!(cell.promptNode.textContent === '[*]:'));
    const executeCell = async () => {
        _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(cell, session);
        setIsRunning(true);
    };
    const interruptKernel = () => {
        var _a, _b;
        void ((_b = (_a = session.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.interrupt());
    };
    (0,react__WEBPACK_IMPORTED_MODULE_3__.useEffect)(() => {
        const codeCellFuture = cell.outputArea.future;
        if (!codeCellFuture) {
            return;
        }
        const { promise, cancel } = makeCancelable(codeCellFuture.done);
        promise.then(() => {
            setIsRunning(false);
        });
        return () => {
            cancel();
        };
    }, [isRunning]);
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PlayButton, { icon: isRunning ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.stopIcon : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.runIcon, onClick: () => (isRunning ? interruptKernel : executeCell)() }));
};
const MarkdownCellPlayButtonComponent = ({ cell }) => {
    const executeCell = () => {
        cell.rendered = true;
    };
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PlayButton, { icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.runIcon, onClick: () => executeCell() }));
};
class CellPlayButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(cell, session) {
        super();
        /**
         * Constructs a new CellPlayButton widget.
         *
         * Note: Depending on the type of cell encountered
         * tries to render an appropriate play button
         * component.
         */
        this.cell = null;
        this.session = null;
        this.cell = cell;
        this.session = session;
        this.addClass('jp-CellPlayButton');
    }
    render() {
        switch (this.cell.model.type) {
            case 'markdown':
                return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(MarkdownCellPlayButtonComponent, { cell: this.cell });
            case 'code':
                return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(CodeCellPlayButtonComponent, { cell: this.cell, session: this.session });
            default:
                break;
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.aedef83afa12907abe94.js.map