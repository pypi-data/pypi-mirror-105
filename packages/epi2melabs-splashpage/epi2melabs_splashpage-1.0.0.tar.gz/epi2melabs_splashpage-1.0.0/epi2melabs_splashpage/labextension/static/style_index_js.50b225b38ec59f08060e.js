(self["webpackChunk_epi2melabs_epi2melabs_splashpage"] = self["webpackChunk_epi2melabs_epi2melabs_splashpage"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/* Reset */\n.tutorialsLauncher * {\n    font-family: Arial, Helvetica, sans-serif;\n    box-sizing: border-box;\n    padding: 0;\n    margin: 0;\n}\n\n/* Type */\n.tutorialsLauncher h1 {\n    font-weight: 600;\n    font-size: 48px;\n}\n\n.tutorialsLauncher h2 {\n    font-weight: 500;\n    font-size: 28px;\n}\n\n.tutorialsLauncher h3 {\n    font-weight: 500;\n    font-size: 18px;\n}\n\n/* Layout */\n.tutorialsLauncher {\n    height: 100%;\n    width: 100%;\n    overflow: scroll;\n    background-color: #f6f6f6;\n}\n\n\n/* Header */\n.tutorialsLauncherHeader {\n    padding: 150px 50px;\n    display: flex;\n    align-items: center;\n    flex-direction: column;\n    background: linear-gradient(to bottom, #06bbb2 0%, #0079a4 100%);\n}\n\n.tutorialsLauncherHeader h1 {\n    padding: 25px 0;\n    color: white;\n    text-align: center;\n}\n\n.tutorialsLauncherHeader p {\n    max-width: 800px;\n    text-align: center;\n    font-size: 16px;\n    line-height: 1.7em;\n    color: white;\n}\n\n.tutorialsLauncherHeader img {\n    width: 75px;\n}\n\n/* Tutorials */\n.tutorialsLauncherList {\n    padding: 50px 50px 0 50px;\n    display: flex;\n    align-items: center;\n    flex-direction: column;\n}\n\n.tutorialsLauncherListHeader {\n    width: 100%;\n    padding: 0 0 15px 0;\n    display: flex;\n    justify-content: space-between;\n    border-bottom: 1px solid lightgray;\n}\n\n.tutorialsLauncherListHeaderToolbar {\n   display: flex;\n   align-items: flex-end; \n}\n\n.tutorialsLauncherListHeaderToolbar li {\n    list-style: none;\n}\n\n.tutorialsLauncherListGrid {\n    width: 100%;\n    padding: 50px 0 0 0;\n    margin: 0;\n    display: grid;\n    grid-template-rows: minmax(min-content, max-content);\n    grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));\n    grid-column-gap: 20px;\n    grid-row-gap: 0;\n}\n\n.tutorialsLauncherListGrid li {\n    width: 100%;\n    margin: 0 0 25px 0;\n    list-style: none;\n}\n\n.tutorialsLauncherListGrid li button {\n    width: 100%;\n    padding: 25px;\n    display: flex;\n    border-radius: 5px;\n    background-color: white;\n    outline: none;\n    border: none;\n    cursor: pointer;\n    transition: 0.2s ease-in-out all;\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.08);\n}\n\n.tutorialsLauncherListGrid li button:hover {\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.15); \n}\n\n.tutorialsLauncherListGrid li .tutorialIcon {\n    height: 100%;\n    width: 50px;\n    padding-right: 15px;\n    display: block;\n}\n\n.tutorialsLauncherListGrid li .tutorialDetails {\n    display: flex;\n    flex-direction: column;\n    align-items: flex-start;\n}\n\n.tutorialsLauncherListGrid li .tutorialDetails>div {\n    display: flex;\n}\n\n.tutorialsLauncherListGrid li h3 {\n    text-transform: capitalize;\n    text-align: left;\n}\n\n.tutorialsLauncherListGrid li p {\n    padding: 7.5px 0 0 0;\n    color: darkgray;\n    text-align: left;\n}\n\n.tutorialsLauncherListGrid li .tutorialButton {\n    margin-left: auto;\n    border: 0;\n    border-radius: 3px;\n    cursor: pointer;\n    background-color: rgba(0,0,0,0.05);\n}\n\n.tutorialsLauncherListGrid li .tutorialButton:hover {\n    background-color: rgba(0,0,0,0.1);\n}\n\n.tutorialsLauncherListGrid li .tutorialButton .tutorialButtonIcon {\n    height: 100%;\n    padding: 5px;\n    display: flex;\n}\n\n\n/* Footer */\n.tutorialsLauncherFooter {\n    width: 100%;\n    padding: 25px;\n    text-align: center;\n    box-sizing: border-box;\n}\n\n\n/* Tooltip */\n.launcherTooltip {\n    position: relative;\n    outline: none;\n    border: none;\n    cursor: pointer;\n    background-color: transparent;\n    font: inherit;\n}\n\n.launcherTooltipIcon {\n    padding: 2px 6px;\n    border-radius: 5px;\n    font-weight: bold;\n    color: black;\n    background-color: rgba(0,0,0,0.05);\n}\n\n.launcherTooltip p {\n    width: 200px;\n    padding: 15px;\n    position: absolute;\n    border-radius: 5px;\n    top: 25px;\n    right: 0;\n    color: white;\n    background-color: black;\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.5);\n}", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA,UAAU;AACV;IACI,yCAAyC;IACzC,sBAAsB;IACtB,UAAU;IACV,SAAS;AACb;;AAEA,SAAS;AACT;IACI,gBAAgB;IAChB,eAAe;AACnB;;AAEA;IACI,gBAAgB;IAChB,eAAe;AACnB;;AAEA;IACI,gBAAgB;IAChB,eAAe;AACnB;;AAEA,WAAW;AACX;IACI,YAAY;IACZ,WAAW;IACX,gBAAgB;IAChB,yBAAyB;AAC7B;;;AAGA,WAAW;AACX;IACI,mBAAmB;IACnB,aAAa;IACb,mBAAmB;IACnB,sBAAsB;IACtB,gEAAgE;AACpE;;AAEA;IACI,eAAe;IACf,YAAY;IACZ,kBAAkB;AACtB;;AAEA;IACI,gBAAgB;IAChB,kBAAkB;IAClB,eAAe;IACf,kBAAkB;IAClB,YAAY;AAChB;;AAEA;IACI,WAAW;AACf;;AAEA,cAAc;AACd;IACI,yBAAyB;IACzB,aAAa;IACb,mBAAmB;IACnB,sBAAsB;AAC1B;;AAEA;IACI,WAAW;IACX,mBAAmB;IACnB,aAAa;IACb,8BAA8B;IAC9B,kCAAkC;AACtC;;AAEA;GACG,aAAa;GACb,qBAAqB;AACxB;;AAEA;IACI,gBAAgB;AACpB;;AAEA;IACI,WAAW;IACX,mBAAmB;IACnB,SAAS;IACT,aAAa;IACb,oDAAoD;IACpD,2DAA2D;IAC3D,qBAAqB;IACrB,eAAe;AACnB;;AAEA;IACI,WAAW;IACX,kBAAkB;IAClB,gBAAgB;AACpB;;AAEA;IACI,WAAW;IACX,aAAa;IACb,aAAa;IACb,kBAAkB;IAClB,uBAAuB;IACvB,aAAa;IACb,YAAY;IACZ,eAAe;IACf,gCAAgC;IAChC,6CAA6C;AACjD;;AAEA;IACI,6CAA6C;AACjD;;AAEA;IACI,YAAY;IACZ,WAAW;IACX,mBAAmB;IACnB,cAAc;AAClB;;AAEA;IACI,aAAa;IACb,sBAAsB;IACtB,uBAAuB;AAC3B;;AAEA;IACI,aAAa;AACjB;;AAEA;IACI,0BAA0B;IAC1B,gBAAgB;AACpB;;AAEA;IACI,oBAAoB;IACpB,eAAe;IACf,gBAAgB;AACpB;;AAEA;IACI,iBAAiB;IACjB,SAAS;IACT,kBAAkB;IAClB,eAAe;IACf,kCAAkC;AACtC;;AAEA;IACI,iCAAiC;AACrC;;AAEA;IACI,YAAY;IACZ,YAAY;IACZ,aAAa;AACjB;;;AAGA,WAAW;AACX;IACI,WAAW;IACX,aAAa;IACb,kBAAkB;IAClB,sBAAsB;AAC1B;;;AAGA,YAAY;AACZ;IACI,kBAAkB;IAClB,aAAa;IACb,YAAY;IACZ,eAAe;IACf,6BAA6B;IAC7B,aAAa;AACjB;;AAEA;IACI,gBAAgB;IAChB,kBAAkB;IAClB,iBAAiB;IACjB,YAAY;IACZ,kCAAkC;AACtC;;AAEA;IACI,YAAY;IACZ,aAAa;IACb,kBAAkB;IAClB,kBAAkB;IAClB,SAAS;IACT,QAAQ;IACR,YAAY;IACZ,uBAAuB;IACvB,4CAA4C;AAChD","sourcesContent":["/* Reset */\n.tutorialsLauncher * {\n    font-family: Arial, Helvetica, sans-serif;\n    box-sizing: border-box;\n    padding: 0;\n    margin: 0;\n}\n\n/* Type */\n.tutorialsLauncher h1 {\n    font-weight: 600;\n    font-size: 48px;\n}\n\n.tutorialsLauncher h2 {\n    font-weight: 500;\n    font-size: 28px;\n}\n\n.tutorialsLauncher h3 {\n    font-weight: 500;\n    font-size: 18px;\n}\n\n/* Layout */\n.tutorialsLauncher {\n    height: 100%;\n    width: 100%;\n    overflow: scroll;\n    background-color: #f6f6f6;\n}\n\n\n/* Header */\n.tutorialsLauncherHeader {\n    padding: 150px 50px;\n    display: flex;\n    align-items: center;\n    flex-direction: column;\n    background: linear-gradient(to bottom, #06bbb2 0%, #0079a4 100%);\n}\n\n.tutorialsLauncherHeader h1 {\n    padding: 25px 0;\n    color: white;\n    text-align: center;\n}\n\n.tutorialsLauncherHeader p {\n    max-width: 800px;\n    text-align: center;\n    font-size: 16px;\n    line-height: 1.7em;\n    color: white;\n}\n\n.tutorialsLauncherHeader img {\n    width: 75px;\n}\n\n/* Tutorials */\n.tutorialsLauncherList {\n    padding: 50px 50px 0 50px;\n    display: flex;\n    align-items: center;\n    flex-direction: column;\n}\n\n.tutorialsLauncherListHeader {\n    width: 100%;\n    padding: 0 0 15px 0;\n    display: flex;\n    justify-content: space-between;\n    border-bottom: 1px solid lightgray;\n}\n\n.tutorialsLauncherListHeaderToolbar {\n   display: flex;\n   align-items: flex-end; \n}\n\n.tutorialsLauncherListHeaderToolbar li {\n    list-style: none;\n}\n\n.tutorialsLauncherListGrid {\n    width: 100%;\n    padding: 50px 0 0 0;\n    margin: 0;\n    display: grid;\n    grid-template-rows: minmax(min-content, max-content);\n    grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));\n    grid-column-gap: 20px;\n    grid-row-gap: 0;\n}\n\n.tutorialsLauncherListGrid li {\n    width: 100%;\n    margin: 0 0 25px 0;\n    list-style: none;\n}\n\n.tutorialsLauncherListGrid li button {\n    width: 100%;\n    padding: 25px;\n    display: flex;\n    border-radius: 5px;\n    background-color: white;\n    outline: none;\n    border: none;\n    cursor: pointer;\n    transition: 0.2s ease-in-out all;\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.08);\n}\n\n.tutorialsLauncherListGrid li button:hover {\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.15); \n}\n\n.tutorialsLauncherListGrid li .tutorialIcon {\n    height: 100%;\n    width: 50px;\n    padding-right: 15px;\n    display: block;\n}\n\n.tutorialsLauncherListGrid li .tutorialDetails {\n    display: flex;\n    flex-direction: column;\n    align-items: flex-start;\n}\n\n.tutorialsLauncherListGrid li .tutorialDetails>div {\n    display: flex;\n}\n\n.tutorialsLauncherListGrid li h3 {\n    text-transform: capitalize;\n    text-align: left;\n}\n\n.tutorialsLauncherListGrid li p {\n    padding: 7.5px 0 0 0;\n    color: darkgray;\n    text-align: left;\n}\n\n.tutorialsLauncherListGrid li .tutorialButton {\n    margin-left: auto;\n    border: 0;\n    border-radius: 3px;\n    cursor: pointer;\n    background-color: rgba(0,0,0,0.05);\n}\n\n.tutorialsLauncherListGrid li .tutorialButton:hover {\n    background-color: rgba(0,0,0,0.1);\n}\n\n.tutorialsLauncherListGrid li .tutorialButton .tutorialButtonIcon {\n    height: 100%;\n    padding: 5px;\n    display: flex;\n}\n\n\n/* Footer */\n.tutorialsLauncherFooter {\n    width: 100%;\n    padding: 25px;\n    text-align: center;\n    box-sizing: border-box;\n}\n\n\n/* Tooltip */\n.launcherTooltip {\n    position: relative;\n    outline: none;\n    border: none;\n    cursor: pointer;\n    background-color: transparent;\n    font: inherit;\n}\n\n.launcherTooltipIcon {\n    padding: 2px 6px;\n    border-radius: 5px;\n    font-weight: bold;\n    color: black;\n    background-color: rgba(0,0,0,0.05);\n}\n\n.launcherTooltip p {\n    width: 200px;\n    padding: 15px;\n    position: absolute;\n    border-radius: 5px;\n    top: 25px;\n    right: 0;\n    color: white;\n    background-color: black;\n    box-shadow: 0 6px 15px rgba(36, 37, 38, 0.5);\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _index_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index.css */ "./style/index.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.50b225b38ec59f08060e.js.map