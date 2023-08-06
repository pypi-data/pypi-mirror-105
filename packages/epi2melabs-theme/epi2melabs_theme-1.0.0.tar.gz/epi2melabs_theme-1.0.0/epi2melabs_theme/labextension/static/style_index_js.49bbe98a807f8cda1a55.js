(self["webpackChunk_epi2melabs_epi2melabs_theme"] = self["webpackChunk_epi2melabs_epi2melabs_theme"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/index.js!./style/custom.css":
/*!*************************************************************!*\
  !*** ./node_modules/css-loader/index.js!./style/custom.css ***!
  \*************************************************************/
/***/ ((module, exports, __webpack_require__) => {

exports = module.exports = __webpack_require__(/*! ../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.id, ".lm-Widget .jp-OutputArea-output {\n    background: #F4F4F4;\n    padding-top: 5px;\n    padding-bottom: 5px;\n}", ""]);

// exports


/***/ }),

/***/ "./node_modules/css-loader/index.js!./style/index.css":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/index.js!./style/index.css ***!
  \************************************************************/
/***/ ((module, exports, __webpack_require__) => {

exports = module.exports = __webpack_require__(/*! ../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports
exports.i(__webpack_require__(/*! -!../node_modules/css-loader/index.js!./variables.css */ "./node_modules/css-loader/index.js!./style/variables.css"), "");
exports.i(__webpack_require__(/*! -!../node_modules/css-loader/index.js!./custom.css */ "./node_modules/css-loader/index.js!./style/custom.css"), "");

// module
exports.push([module.id, "/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n/* Set the default typography for monospace elements */\ntt,\ncode,\nkbd,\nsamp,\npre {\n  font-family: var(--jp-code-font-family);\n  font-size: var(--jp-code-font-size);\n  line-height: var(--jp-code-line-height);\n}\n", ""]);

// exports


/***/ }),

/***/ "./node_modules/css-loader/index.js!./style/variables.css":
/*!****************************************************************!*\
  !*** ./node_modules/css-loader/index.js!./style/variables.css ***!
  \****************************************************************/
/***/ ((module, exports, __webpack_require__) => {

exports = module.exports = __webpack_require__(/*! ../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.id, "/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n/*\n * The following CSS variables define the main, public API for styling JupyterLab.\n * These variables should be used by all plugins wherever possible. In other\n * words, plugins should not define custom colors, sizes, etc unless absolutely\n * necessary. This enables users to change the visual theme of JupyterLab\n * by changing these variables.\n *\n * Many variables appear in an ordered sequence (0,1,2,3). These sequences\n * are designed to work well together, so for example, `--jp-border-color1` should\n * be used with `--jp-layout-color1`. The numbers have the following meanings:\n *\n * 0: super-primary, reserved for special emphasis\n * 1: primary, most important under normal situations\n * 2: secondary, next most important under normal situations\n * 3: tertiary, next most important under normal situations\n *\n * Throughout JupyterLab, we are mostly following principles from Google's\n * Material Design when selecting colors. We are not, however, following\n * all of MD as it is not optimized for dense, information rich UIs.\n */\n :root {\n  /* light to dark for light theme\n   * dark to light for dark theme */\n  /* dark to light for light theme\n   * light to dark for dark theme */\n  --epi2melabs-turquoise: #69BCB8;\n  --epi2melabs-yellow: #FECE63;\n  --epi2melabs-blue: #007BA6;\n  --epi2melabs-darkblue: #0E588B;\n  --epi2melabs-darkgrey: #333333;\n\n  --base16-green0: #32532b;\n  --base16-green1: #436e39;\n  --base16-green-extra: #63a455;\n  --base16-green2: #538947;\n  --base16-blue0: #4b8aa1;\n  --base16-blue1: #609eb5;\n  --base16-blue2: #7cafc2;\n  --base16-red0: #702e2b;\n  --base16-red1: #8e3a37;\n  --base16-red-extra: #be5b57;\n  --base16-red2: #ab4642;\n  --base16-purple0: #66416b;\n  --base16-purple1: #7e5185;\n  --base16-purple2: #96609e;\n  --base16-aqua0: #2f515d;\n  --base16-aqua1: #3d6878;\n  --base16-aqua-extra: #5b96ab;\n  --base16-aqua2: #4b8093;\n  --base16-foreground-light: #383838;\n  --base16-gray: #bbbbbb;\n  --base16-gray-dark: #e4e4e4;\n  --base16-yellow0: #ae6b06;\n  --base16-yellow1: #d58307;\n  --base16-yellow-extra: #f8ab35;\n  --base16-yellow2: #f79a0e;\n  --base16-orange0: #ae6b06;\n  --base16-orange1: #d58307;\n  --base16-orange-extra: #f8ab35;\n  --base16-orange2: #f79a0e;\n  --jp-layout-color0: #f8f8f8;\n  --jp-layout-color1: #eeeeee;\n  --jp-layout-color2: #e4e4e4;\n  --jp-layout-color3: #cfcfcf;\n  --jp-layout-color4: #a6a6a6;\n  --jp-layout-color5: #929292;\n  --jp-layout-color6: #7e7e7e;\n  --jp-inverse-layout-color0: #383838;\n  --jp-inverse-layout-color1: #4c4c4c;\n  --jp-inverse-layout-color2: #616161;\n  --jp-inverse-layout-color3: #757575;\n  --jp-inverse-layout-color4: #8a8a8a;\n  --jp-inverse-layout-color5: #9e9e9e;\n  --jp-editor-selected-focused-background: var(--jp-layout-color0);\n  --jp-editor-cursor-color: var(--jp-inverse-layout-color0);\n  /* Elevation\n   *\n   * We style box-shadows using Material Design's idea of elevation. These particular numbers are taken from here:\n   *\n   * https://github.com/material-components/material-components-web\n   * https://material-components-web.appspot.com/elevation.html\n   */\n  /* The dark theme shadows need a bit of work, but this will probably also require work on the core layout\n   * colors used in the theme as well. */\n  --jp-shadow-base-lightness: 32;\n  --jp-shadow-umbra-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.2\n  );\n  --jp-shadow-penumbra-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.14\n  );\n  --jp-shadow-ambient-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.12\n  );\n  --jp-elevation-z0: none;\n  --jp-elevation-z1: 0px 2px 1px -1px var(--jp-shadow-umbra-color),\n    0px 1px 1px 0px var(--jp-shadow-penumbra-color),\n    0px 1px 3px 0px var(--jp-shadow-ambient-color);\n  --jp-elevation-z2: 0px 3px 1px -2px var(--jp-shadow-umbra-color),\n    0px 2px 2px 0px var(--jp-shadow-penumbra-color),\n    0px 1px 5px 0px var(--jp-shadow-ambient-color);\n  --jp-elevation-z4: 0px 2px 4px -1px var(--jp-shadow-umbra-color),\n    0px 4px 5px 0px var(--jp-shadow-penumbra-color),\n    0px 1px 10px 0px var(--jp-shadow-ambient-color);\n  --jp-elevation-z6: 0px 3px 5px -1px var(--jp-shadow-umbra-color),\n    0px 6px 10px 0px var(--jp-shadow-penumbra-color),\n    0px 1px 18px 0px var(--jp-shadow-ambient-color);\n  --jp-elevation-z8: 0px 5px 5px -3px var(--jp-shadow-umbra-color),\n    0px 8px 10px 1px var(--jp-shadow-penumbra-color),\n    0px 3px 14px 2px var(--jp-shadow-ambient-color);\n  --jp-elevation-z12: 0px 7px 8px -4px var(--jp-shadow-umbra-color),\n    0px 12px 17px 2px var(--jp-shadow-penumbra-color),\n    0px 5px 22px 4px var(--jp-shadow-ambient-color);\n  --jp-elevation-z16: 0px 8px 10px -5px var(--jp-shadow-umbra-color),\n    0px 16px 24px 2px var(--jp-shadow-penumbra-color),\n    0px 6px 30px 5px var(--jp-shadow-ambient-color);\n  --jp-elevation-z20: 0px 10px 13px -6px var(--jp-shadow-umbra-color),\n    0px 20px 31px 3px var(--jp-shadow-penumbra-color),\n    0px 8px 38px 7px var(--jp-shadow-ambient-color);\n  --jp-elevation-z24: 0px 11px 15px -7px var(--jp-shadow-umbra-color),\n    0px 24px 38px 3px var(--jp-shadow-penumbra-color),\n    0px 9px 46px 8px var(--jp-shadow-ambient-color);\n  /* Borders\n   *\n   * The following variables, specify the visual styling of borders in JupyterLab.\n   */\n  --jp-border-width: 1px;\n  --jp-border-color0: var(--jp-layout-color1);\n  --jp-border-color1: var(--jp-layout-color2);\n  --jp-border-color2: var(--jp-layout-color3);\n  --jp-border-color3: var(--jp-layout-color5);\n  --jp-border-radius: 2px;\n  /* UI Fonts\n   *\n   * The UI font CSS variables are used for the typography all of the JupyterLab\n   * user interface elements that are not directly user generated content.\n   *\n   * The font sizing here is done assuming that the body font size of --jp-ui-font-size1\n   * is applied to a parent element. When children elements, such as headings, are sized\n   * in em all things will be computed relative to that body size.\n   */\n  --jp-ui-font-scale-factor: 1.2;\n  --jp-ui-font-size0: 0.83333em;\n  --jp-ui-font-size1: 13px;\n  /* Base font size */\n  --jp-ui-font-size2: 1.2em;\n  --jp-ui-font-size3: 1.44em;\n  --jp-ui-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica,\n    Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';\n  /*\n   * Use these font colors against the corresponding main layout colors.\n   * In a light theme, these go from dark to light.\n   */\n  /* Darkening colors */\n  --jp-ui-font-color0: var(--jp-inverse-layout-color0);\n  --jp-ui-font-color1: var(--jp-inverse-layout-color1);\n  --jp-ui-font-color2: var(--jp-inverse-layout-color3);\n  --jp-ui-font-color3: var(--jp-inverse-layout-color5);\n  /*\n   * Use these against the brand/accent/warn/error colors.\n   * These will typically go from light to darker, in both a dark and light theme.\n   */\n  --jp-ui-inverse-font-color0: var(--base16-gray);\n  --jp-ui-inverse-font-color1: var(--base16-gray-dark);\n  --jp-ui-inverse-font-color2: var(--jp-layout-color6);\n  --jp-ui-inverse-font-color3: var(--jp-layout-color5);\n  /* Content Fonts\n   *\n   * Content font variables are used for typography of user generated content.\n   *\n   * The font sizing here is done assuming that the body font size of --jp-content-font-size1\n   * is applied to a parent element. When children elements, such as headings, are sized\n   * in em all things will be computed relative to that body size.\n   */\n  --jp-content-line-height: 1.6;\n  --jp-content-font-scale-factor: 1.2;\n  --jp-content-font-size0: 0.83333em;\n  --jp-content-font-size1: 14px;\n  /* Base font size */\n  --jp-content-font-size2: 1.2em;\n  --jp-content-font-size3: 1.44em;\n  --jp-content-font-size4: 1.728em;\n  --jp-content-font-size5: 2.0736em;\n  /* This gives a magnification of about 125% in presentation mode over normal. */\n  --jp-content-presentation-font-size1: 17px;\n  --jp-content-heading-line-height: 1;\n  --jp-content-heading-margin-top: 1.2em;\n  --jp-content-heading-margin-bottom: 0.8em;\n  --jp-content-heading-font-weight: 500;\n  /* Shades of the default font color */\n  --jp-content-font-color0: var(--jp-inverse-layout-color0);\n  --jp-content-font-color1: var(--jp-inverse-layout-color1);\n  --jp-content-font-color2: var(--jp-inverse-layout-color3);\n  --jp-content-font-color3: var(--jp-inverse-layout-color5);\n  --jp-content-link-color: var(--epi2melabs-blue);\n  --jp-content-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',\n    Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',\n    'Segoe UI Symbol';\n  /*\n   * Code Fonts\n   *\n   * Code font variables are used for typography of code and other monospaces content.\n   */\n   --jp-code-font-size: 13px;\n   --jp-code-line-height: 1.3077; /* 17px for 13px base */\n   --jp-code-padding: 5px; /* 5px for 13px base, codemirror highlighting needs integer px value */\n   --jp-code-font-family-default: Menlo, Consolas, 'DejaVu Sans Mono', monospace;\n   --jp-code-font-family: var(--jp-code-font-family-default);\n \n   /* This gives a magnification of about 125% in presentation mode over normal. */\n   --jp-code-presentation-font-size: 16px;\n \n   /* may need to tweak cursor width if you change font size */\n   --jp-code-cursor-width0: 1.4px;\n   --jp-code-cursor-width1: 2px;\n   --jp-code-cursor-width2: 4px;\n  /* Layout\n   *\n   * The following are the main layout colors use in JupyterLab. In a light\n   * theme these would go from light to dark.\n   */\n  /* Brand/accent */\n  --jp-brand-color0: var(--epi2melabs-blue);\n  --jp-brand-color1: var(--epi2melabs-blue);\n  --jp-brand-color2: var(--base16-aqua1);\n  --jp-brand-color3: var(--base16-aqua0);\n  --jp-accent-color0: var(--base16-green2);\n  --jp-accent-color1: var(--base16-green-extra);\n  --jp-accent-color2: var(--base16-green1);\n  --jp-accent-color3: var(--base16-green0);\n  /* State colors (warn, error, success, info) */\n  --jp-warn-color0: var(--epi2melabs-blue);\n  --jp-warn-color1: var(--epi2melabs-yellow);\n  --jp-warn-color2: var(--base16-orange1);\n  --jp-warn-color3: var(--base16-orange0);\n  --jp-error-color0: var(--base16-red2);\n  --jp-error-color1: var(--base16-red-extra);\n  --jp-error-color2: var(--base16-red1);\n  --jp-error-color3: var(--base16-red0);\n  --jp-success-color0: var(--base16-green2);\n  --jp-success-color1: var(--base16-green-extra);\n  --jp-success-color2: var(--base16-green1);\n  --jp-success-color3: var(--base16-green0);\n  --jp-info-color0: var(--base16-aqua2);\n  --jp-info-color1: var(--base16-aqua-extra);\n  --jp-info-color2: var(--base16-aqua1);\n  --jp-info-color3: var(--base16-aqua0);\n  /* Cell specific styles */\n  --jp-cell-padding: 5px;\n  --jp-cell-collapser-width: 8px;\n  --jp-cell-collapser-min-height: 20px;\n  --jp-cell-collapser-not-active-hover-opacity: 0.6;\n  --jp-cell-editor-background: var(--jp-layout-color1);\n  --jp-cell-editor-border-color: var(--base16-gray-dark);\n  --jp-cell-editor-active-border-color: var(--epi2melabs-blue);\n  --jp-cell-editor-box-shadow: inset 0 0 1px var(--base16-gray-dark);\n  --jp-cell-editor-active-background: var(--jp-layout-color1);\n  --jp-cell-editor-active-whiteborder-color: var(--base16-gray);\n  --jp-cell-prompt-width: 64px;\n  --jp-cell-prompt-font-family: 'Source Code Pro', monospace;\n  --jp-cell-prompt-letter-spacing: 0px;\n  --jp-cell-prompt-opacity: 1;\n  --jp-cell-prompt-not-active-opacity: 1;\n  --jp-cell-prompt-not-active-font-color: var(--base16-gray);\n  --jp-cell-inprompt-font-color: var(--epi2melabs-darkgrey);\n  --jp-cell-outprompt-font-color: var(--base16-yellow-extra);\n  /* Notebook specific styles */\n  --jp-notebook-padding: 10px;\n  --jp-notebook-select-background: var(--jp-layout-color2);\n  --jp-notebook-multiselected-color: rgba(181, 118, 20, 0.24);\n  /* The scroll padding is calculated to fill enough space at the bottom of the\n   *notebook to show one single-line cell (with appropriate padding) at the top\n   *when the notebook is scrolled all the way to the bottom. We also subtract one\n   *pixel so that no scrollbar appears if we have just one single-line cell in the\n   *notebook. This padding is to enable a 'scroll past end' feature in a notebook.\n   */\n  --jp-notebook-scroll-padding: calc(\n    100% - var(--jp-code-font-size) * var(--jp-code-line-height) -\n      var(--jp-code-padding) - var(--jp-cell-padding) - 1px\n  );\n  /* Rendermime styles */\n  --jp-rendermime-error-background: var(--jp-layout-color0);\n  --jp-rendermime-table-row-background: var(--jp-layout-color1);\n  --jp-rendermime-table-row-hover-background: rgba(3, 169, 244, 0.2);\n  /* Dialog specific styles */\n  --jp-dialog-background: rgba(0, 0, 0, 0.6);\n  /* Console specific styles */\n  --jp-console-padding: 10px;\n  /* Toolbar specific styles */\n  --jp-toolbar-border-color: var(--jp-border-color2);\n  --jp-toolbar-micro-height: 8px;\n  --jp-toolbar-background: var(--jp-layout-color1);\n  --jp-toolbar-box-shadow: 0px 0px 2px 0px rgba(0, 0, 0, 0.8);\n  --jp-toolbar-header-margin: 4px 4px 0px 4px;\n  --jp-toolbar-active-background: var(--jp-layout-color0);\n  /* Input field styles */\n  --jp-input-box-shadow: inset 0 0 1px var(--base16-orange0);\n  --jp-input-active-background: var(--jp-layout-color0);\n  --jp-input-hover-background: var(--jp-layout-color2);\n  --jp-input-background: var(--jp-layout-color2);\n  --jp-input-border-color: var(--epi2melabs-blue);\n  --jp-input-active-border-color: var(--jp-brand-color1);\n  /* General editor styles */\n  --jp-editor-selected-background: var(--jp-layout-color2);\n  /* Code mirror specific styles */\n  --jp-mirror-editor-keyword-color: var(--epi2melabs-darkblue);\n  --jp-mirror-editor-atom-color: var(--base16-red2);\n  --jp-mirror-editor-number-color: var(--base16-blue1);\n  --jp-mirror-editor-def-color: var(--base16-purple2);\n  --jp-mirror-editor-variable-color: var(--base16-foreground-light);\n  --jp-mirror-editor-variable-2-color: var(--base16-blue2);\n  --jp-mirror-editor-variable-3-color: var(--base16-gray);\n  --jp-mirror-editor-punctuation-color: var(--base16-orange2);\n  --jp-mirror-editor-property-color: var(--base16-purple2);\n  --jp-mirror-editor-operator-color: var(--base16-foreground-light);\n  --jp-mirror-editor-comment-color: var(--jp-inverse-layout-color4);\n  --jp-mirror-editor-string-color: var(--epi2melabs-blue);\n  --jp-mirror-editor-string-2-color: var(--base16-green1);\n  --jp-mirror-editor-meta-color: var(--base16-yellow1);\n  --jp-mirror-editor-qualifier-color: var(--base16-green1);\n  --jp-mirror-editor-builtin-color: var(--base16-orange2);\n  --jp-mirror-editor-bracket-color: var(--base16-foreground-light);\n  --jp-mirror-editor-tag-color: var(--base16-aqua1);\n  --jp-mirror-editor-attribute-color: var(--base16-blue1);\n  --jp-mirror-editor-header-color: var(--base16-blue1);\n  --jp-mirror-editor-quote-color: var(--base16-green1);\n  --jp-mirror-editor-link-color: var(--base16-orange0);\n  --jp-mirror-editor-error-color: var(--base16-red2);\n  --jp-mirror-editor-hr-color: var(--base16-gray);\n  /* Vega extension styles */\n  --jp-vega-background: var(--jp-layout-color6);\n  /* Sidebar-related styles */\n  --jp-sidebar-min-width: 180px;\n  /* Search-related styles */\n  --jp-search-toggle-off-opacity: 0.5;\n  --jp-search-toggle-hover-opacity: 0.75;\n  --jp-search-toggle-on-opacity: 1;\n  /* scrollbar related styles. Supports every browser except Edge.\n   * On Firefox, only the color settings are respected.\n   */\n  --jp-scrollbar-background-color: var(--jp-layout-color0);\n  --jp-scrollbar-endpad: 3px;\n  /* the minimum gap between the thumb and the ends of a scrollbar */\n  --jp-scrollbar-thumb-color: 213, 196, 161;\n  /* need to specify thumb color as an RGB triplet */\n  --jp-scrollbar-thumb-margin: 5px;\n  /* the space in between the sides of the thumb and the track */\n  --jp-scrollbar-thumb-radius: 9px;\n  /* set to a large-ish value for rounded endcaps on the thumb */ }", ""]);

// exports


/***/ }),

/***/ "./node_modules/css-loader/lib/css-base.js":
/*!*************************************************!*\
  !*** ./node_modules/css-loader/lib/css-base.js ***!
  \*************************************************/
/***/ ((module) => {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
module.exports = function(useSourceMap) {
	var list = [];

	// return the list of modules as css string
	list.toString = function toString() {
		return this.map(function (item) {
			var content = cssWithMappingToString(item, useSourceMap);
			if(item[2]) {
				return "@media " + item[2] + "{" + content + "}";
			} else {
				return content;
			}
		}).join("");
	};

	// import a list of modules into the list
	list.i = function(modules, mediaQuery) {
		if(typeof modules === "string")
			modules = [[null, modules, ""]];
		var alreadyImportedModules = {};
		for(var i = 0; i < this.length; i++) {
			var id = this[i][0];
			if(typeof id === "number")
				alreadyImportedModules[id] = true;
		}
		for(i = 0; i < modules.length; i++) {
			var item = modules[i];
			// skip already imported module
			// this implementation is not 100% perfect for weird media query combinations
			//  when a module is imported multiple times with different media queries.
			//  I hope this will never occur (Hey this way we have smaller bundles)
			if(typeof item[0] !== "number" || !alreadyImportedModules[item[0]]) {
				if(mediaQuery && !item[2]) {
					item[2] = mediaQuery;
				} else if(mediaQuery) {
					item[2] = "(" + item[2] + ") and (" + mediaQuery + ")";
				}
				list.push(item);
			}
		}
	};
	return list;
};

function cssWithMappingToString(item, useSourceMap) {
	var content = item[1] || '';
	var cssMapping = item[3];
	if (!cssMapping) {
		return content;
	}

	if (useSourceMap && typeof btoa === 'function') {
		var sourceMapping = toComment(cssMapping);
		var sourceURLs = cssMapping.sources.map(function (source) {
			return '/*# sourceURL=' + cssMapping.sourceRoot + source + ' */'
		});

		return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
	}

	return [content].join('\n');
}

// Adapted from convert-source-map (MIT)
function toComment(sourceMap) {
	// eslint-disable-next-line no-undef
	var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
	var data = 'sourceMappingURL=data:application/json;charset=utf-8;base64,' + base64;

	return '/*# ' + data + ' */';
}


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
/* harmony import */ var _node_modules_css_loader_index_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/index.js!./index.css */ "./node_modules/css-loader/index.js!./style/index.css");
/* harmony import */ var _node_modules_css_loader_index_js_index_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_index_js_index_css__WEBPACK_IMPORTED_MODULE_1__);

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()((_node_modules_css_loader_index_js_index_css__WEBPACK_IMPORTED_MODULE_1___default()), options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((_node_modules_css_loader_index_js_index_css__WEBPACK_IMPORTED_MODULE_1___default().locals) || {});

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

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
//# sourceMappingURL=style_index_js.49bbe98a807f8cda1a55.js.map