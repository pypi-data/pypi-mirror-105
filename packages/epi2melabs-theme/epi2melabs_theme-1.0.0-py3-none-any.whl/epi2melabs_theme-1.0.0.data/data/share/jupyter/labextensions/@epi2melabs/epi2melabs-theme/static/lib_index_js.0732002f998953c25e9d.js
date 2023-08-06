(self["webpackChunk_epi2melabs_epi2melabs_theme"] = self["webpackChunk_epi2melabs_epi2melabs_theme"] || []).push([["lib_index_js"],{

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
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * A plugin for Oxford Nanopore Technologies/epi2melabs-theme
 */
const plugin = {
    id: '@epi2melabs/epi2melabs-theme:plugin',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    activate: function (app, manager) {
        const style = '@epi2melabs/epi2melabs-theme/index.css';
        manager.register({
            name: 'epi2melabs-theme',
            isLight: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0732002f998953c25e9d.js.map