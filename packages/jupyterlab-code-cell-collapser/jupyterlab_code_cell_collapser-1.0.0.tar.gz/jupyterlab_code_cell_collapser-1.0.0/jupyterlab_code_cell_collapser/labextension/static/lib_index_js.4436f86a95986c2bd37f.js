(self["webpackChunk_epi2melabs_jupyterlab_code_cell_collapser"] = self["webpackChunk_epi2melabs_jupyterlab_code_cell_collapser"] || []).push([["lib_index_js"],{

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
 * Helper method
 */
const addCodeCellCollapser = (cell, tracker) => {
    if (cell.model.type === 'code' && !tracker[cell.model.id]) {
        const collapser = new _widget__WEBPACK_IMPORTED_MODULE_1__.CodeCellCollapser(cell);
        tracker[cell.model.id] = collapser;
        cell.inputArea.layout.insertWidget(0, collapser);
    }
};
/**
 * Initialization data for the jupyterlab-code-cell-collapser extension.
 */
const extension = {
    id: 'jupyterlab-code-cell-collapser',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, nbTrack) => {
        nbTrack.currentChanged.connect(() => {
            const notebookCellCollapsers = {};
            const notebookPanel = nbTrack.currentWidget;
            if (notebookPanel === null) {
                return;
            }
            const notebook = nbTrack.currentWidget.content;
            notebookPanel.context.ready.then(async () => {
                // Iterate over all code cells and create a collapser
                // for each that exists
                notebook.widgets.map((c) => {
                    addCodeCellCollapser(c, notebookCellCollapsers);
                });
                nbTrack.activeCellChanged.connect(() => {
                    const cell = notebook.activeCell;
                    if (cell !== null) {
                        addCodeCellCollapser(cell, notebookCellCollapsers);
                    }
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
/* harmony export */   "CodeCellCollapser": () => (/* binding */ CodeCellCollapser)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);



const CELL_INPUT_AREA_COLLAPSED_CLASS = 'jp-Cell-inputAreaCollapsed';
/**
 * isFirstLineComment
 *
 * Note: Helper method to determine whether the cell contains a valid
 * comment on the first line
 *
 * @param cell - The CodeCell parent.
 */
const isFirstLineComment = (cell) => {
    const splitLines = (lines) => lines.split(/\r?\n/);
    const firstLine = splitLines(cell.model.value.text);
    return firstLine[0].startsWith('#');
};
const CollapseButton = ({ onClick, collapsed = false, }) => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { type: "button", onClick: () => onClick(), className: "collapseButton" },
    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: collapsed ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.caretUpIcon : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.caretDownIcon, className: "collapseButton-icon", tag: "span", width: "10px", height: "15px" })));
const CodeCellCollapserComponent = ({ cell, }) => {
    const metadata = cell.model.metadata;
    const [isCollapsible, setIsCollapsible] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(isFirstLineComment(cell));
    const [isCollapsed, setIsCollapsed] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(false);
    const handleSetCollapsed = () => {
        cell.inputArea.toggleClass(CELL_INPUT_AREA_COLLAPSED_CLASS);
        if (!isCollapsed) {
            metadata.set('partialCollapse', true);
        }
        else {
            metadata.delete('partialCollapse');
        }
        setIsCollapsed(!isCollapsed);
    };
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        const initiallyCollapsed = metadata.get('partialCollapse');
        if (initiallyCollapsed) {
            setIsCollapsed(initiallyCollapsed);
            cell.inputArea.addClass(CELL_INPUT_AREA_COLLAPSED_CLASS);
        }
        cell.inputArea.model.contentChanged.connect(() => {
            setIsCollapsible(isFirstLineComment(cell));
        });
    }, []);
    return isCollapsible ?
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement(CollapseButton, { onClick: () => handleSetCollapsed(), collapsed: isCollapsed })
        : react__WEBPACK_IMPORTED_MODULE_2___default().createElement((react__WEBPACK_IMPORTED_MODULE_2___default().Fragment), null);
};
class CodeCellCollapser extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(cell) {
        super();
        /**
         * Constructs a new CodeCellCollapser widget.
         */
        this.cell = null;
        this.cell = cell;
        this.addClass('jp-CodeCellCollapser');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_2___default().createElement(CodeCellCollapserComponent, { cell: this.cell });
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4436f86a95986c2bd37f.js.map