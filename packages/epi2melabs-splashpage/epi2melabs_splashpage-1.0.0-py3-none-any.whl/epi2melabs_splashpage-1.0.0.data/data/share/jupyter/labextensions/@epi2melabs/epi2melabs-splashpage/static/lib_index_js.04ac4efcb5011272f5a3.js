(self["webpackChunk_epi2melabs_epi2melabs_splashpage"] = self["webpackChunk_epi2melabs_epi2melabs_splashpage"] || []).push([["lib_index_js"],{

/***/ "./lib/asset.js":
/*!**********************!*\
  !*** ./lib/asset.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "logoSVG": () => (/* binding */ logoSVG),
/* harmony export */   "labsLogoIcon": () => (/* binding */ labsLogoIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const logoSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="148" height="198" viewBox="0 0 148 198">
    <defs>
      <filter id="Rectangle_1" x="0" y="0" width="148" height="68" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur"/>
        <feComposite in="SourceGraphic"/>
      </filter>
      <filter id="Rectangle_2" x="0" y="130" width="148" height="68" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur-2"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur-2"/>
        <feComposite in="SourceGraphic"/>
      </filter>
      <filter id="Rectangle_3" x="0" y="65" width="73" height="68" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur-3"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur-3"/>
        <feComposite in="SourceGraphic"/>
      </filter>
    </defs>
    <g id="Component_1_2" data-name="Component 1 – 2" transform="translate(9 6)">
      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">
        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="130" height="50" rx="5" transform="translate(9 6)" fill="#08bbb2"/>
      </g>
      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">
        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="130" height="50" rx="5" transform="translate(9 136)" fill="#0179a4"/>
      </g>
      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">
        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="55" height="50" rx="5" transform="translate(9 71)" fill="#fccb10"/>
      </g>
    </g>
  </svg>
`;
const logoSVGSmall = `
  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="42" height="51" viewBox="0 0 42 51">
    <defs>
        <filter id="Rectangle_1" x="0" y="0" width="42" height="27" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur"/>
        <feComposite in="SourceGraphic"/>
        </filter>
        <filter id="Rectangle_2" x="0" y="24" width="42" height="27" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur-2"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur-2"/>
        <feComposite in="SourceGraphic"/>
        </filter>
        <filter id="Rectangle_3" x="0" y="12" width="28" height="27" filterUnits="userSpaceOnUse">
        <feOffset dy="3" input="SourceAlpha"/>
        <feGaussianBlur stdDeviation="3" result="blur-3"/>
        <feFlood flood-opacity="0.098"/>
        <feComposite operator="in" in2="blur-3"/>
        <feComposite in="SourceGraphic"/>
        </filter>
    </defs>
    <g id="Component_2_1" data-name="Component 2 – 1" transform="translate(9 6)">
        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">
        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="24" height="9" rx="1" transform="translate(9 6)" fill="#08bbb2"/>
        </g>
        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">
        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="24" height="9" rx="1" transform="translate(9 30)" fill="#0179a4"/>
        </g>
        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">
        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="10" height="9" rx="1" transform="translate(9 18)" fill="#fccb10"/>
        </g>
    </g>
  </svg>
`;
const labsLogoIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: 'ui-components:labs', svgstr: logoSVGSmall });


/***/ }),

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
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./types */ "./lib/types.js");
/* harmony import */ var _asset__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./asset */ "./lib/asset.js");








const PLUGIN_ID = '@epi2melabs/epi2melabs-splashpage:settings';
const COMMAND = 'create-epi2me-labs-splashpage';
const CATEGORY = 'EPI2ME Labs';
const createLauncherWidget = async (sections, shell, docTrack, setting) => {
    // Build the widget and add it to the main area
    const content = new _widget__WEBPACK_IMPORTED_MODULE_5__.Epi2melabsLauncherWidget(setting, docTrack, sections);
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.MainAreaWidget({ content });
    widget.title.label = 'EPI2ME Labs';
    shell.add(widget, 'main');
};
const extension = {
    id: PLUGIN_ID,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    autoStart: true,
    activate: (app, docTrack, launcher, settings) => {
        const { commands, shell } = app;
        Promise.all([app.restored, settings.load(PLUGIN_ID)])
            .then(([, setting]) => {
            // Specify the sections to be shown
            const workdirPath = setting.get('working_dir').composite;
            const templatePath = setting.get('template_dir').composite;
            const sections = [
                {
                    name: 'Recent notebooks',
                    tooltip: `Displays notebooks in the ${workdirPath} directory`,
                    path: workdirPath,
                    icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.runIcon,
                    action: _types__WEBPACK_IMPORTED_MODULE_6__.NotebookAction.open
                },
                {
                    name: 'EPI2ME Labs Templates',
                    tooltip: 'Click on a template to copy it and get started',
                    path: templatePath,
                    icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.copyIcon,
                    action: _types__WEBPACK_IMPORTED_MODULE_6__.NotebookAction.clone
                }
            ];
            createLauncherWidget(sections, shell, docTrack, setting);
            commands.addCommand(COMMAND, {
                caption: 'Create an EPI2ME Labs launcher',
                label: 'EPI2ME Labs',
                icon: args => (args['isPalette'] ? null : _asset__WEBPACK_IMPORTED_MODULE_7__.labsLogoIcon),
                execute: () => {
                    createLauncherWidget(sections, shell, docTrack, setting);
                }
            });
            if (launcher) {
                launcher.add({
                    command: COMMAND,
                    category: CATEGORY
                });
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/lib.js":
/*!********************!*\
  !*** ./lib/lib.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "actionCallbacks": () => (/* binding */ actionCallbacks),
/* harmony export */   "getNestedFiles": () => (/* binding */ getNestedFiles),
/* harmony export */   "getNotebooks": () => (/* binding */ getNotebooks)
/* harmony export */ });
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./types */ "./lib/types.js");

const IPYNB = '.ipynb';
const actionCallbacks = {
    [_types__WEBPACK_IMPORTED_MODULE_0__.NotebookAction.clone]: async (e, docTrack, settings) => {
        await docTrack.copy(e, settings.get('working_dir').composite).then(e => {
            docTrack.open(e.path);
        });
    },
    [_types__WEBPACK_IMPORTED_MODULE_0__.NotebookAction.open]: (e, docTrack) => {
        docTrack.open(e);
    }
};
const getNestedFiles = async (path, docTrack) => {
    return (await Promise.all((await docTrack.services.contents.get(path))
        .content
        .map((Item) => {
        return Item.type === 'directory'
            ? getNestedFiles(Item.path, docTrack)
            : Item;
    }))).flat(Infinity);
};
const getNotebooks = async (path, docTrack) => {
    return (await getNestedFiles(path, docTrack))
        .filter((Item) => Item.path.endsWith(IPYNB))
        .map((Item) => ({
        name: Item.name,
        path: Item.path,
        last_modified: Item.last_modified
    }));
};


/***/ }),

/***/ "./lib/types.js":
/*!**********************!*\
  !*** ./lib/types.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NotebookAction": () => (/* binding */ NotebookAction)
/* harmony export */ });
var NotebookAction;
(function (NotebookAction) {
    NotebookAction["open"] = "open";
    NotebookAction["clone"] = "clone";
})(NotebookAction || (NotebookAction = {}));


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LabsLogo": () => (/* binding */ LabsLogo),
/* harmony export */   "Epi2melabsLauncherWidget": () => (/* binding */ Epi2melabsLauncherWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lib__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./lib */ "./lib/lib.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _asset__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./asset */ "./lib/asset.js");
/* harmony import */ var moment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! moment */ "webpack/sharing/consume/default/moment/moment");
/* harmony import */ var moment__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(moment__WEBPACK_IMPORTED_MODULE_3__);






const LabsLogo = () => {
    const logoSVGBlob = new Blob([_asset__WEBPACK_IMPORTED_MODULE_4__.logoSVG], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(logoSVGBlob);
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "labsLogo" },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("img", { src: url, alt: "The EPI2ME Labs logo" })));
};
const LauncherHeader = ({}) => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialsLauncherHeader" },
    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabsLogo, null),
    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h1", null, "Welcome to EPI2ME Labs"),
    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null, "EPI2ME Labs maintains a growing collection of notebooks on a range of topics from basic quality control to genome assembly. These are free and open to use by anyone. Browse the list below and get started.")));
const LauncherFooter = ({}) => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialsLauncherFooter" },
    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null,
        "@2008 - ",
        moment__WEBPACK_IMPORTED_MODULE_3___default()().year(),
        " Oxford Nanopore Technologies. All rights reserved")));
const LauncherTooltip = ({ tooltip }) => {
    const [isVisible, setIsVisible] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(false);
    const handleToggleVisible = () => {
        setIsVisible(!isVisible);
    };
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { className: "launcherTooltip", onClick: handleToggleVisible, onMouseEnter: handleToggleVisible, onMouseLeave: handleToggleVisible },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcherTooltipIcon" }, "?"),
        isVisible ? (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null, tooltip)) : ('')));
};
const LauncherNotebookListItem = ({ TrackedNotebook, action, icon, }) => {
    const { name, path, last_modified } = TrackedNotebook;
    const handleExtractName = () => {
        return name.split('_').join(' ').split('.ipynb').join('');
    };
    const handleFormatUpdated = () => {
        return moment__WEBPACK_IMPORTED_MODULE_3___default()(last_modified).format("MMMM Do YYYY, h:mm:ss a");
    };
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { onClick: () => action() },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.notebookIcon, className: "tutorialIcon", tag: "span", width: "100%", height: "100%" })),
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialDetails" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h3", null, handleExtractName()),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null,
                "Path: ",
                path),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null,
                "Last modified: ",
                handleFormatUpdated())),
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialButton" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: icon, className: "tutorialButtonIcon", tag: "span", width: "20px", height: "20px" }))));
};
const LauncherNotebookList = ({ TrackedNotebookList, docTrack, setting }) => {
    const { path, name, icon, tooltip, action } = TrackedNotebookList;
    const [notebooks, setNotebooks] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)([]);
    const handleUpdateSections = async () => {
        setNotebooks(await (0,_lib__WEBPACK_IMPORTED_MODULE_5__.getNotebooks)(path, docTrack));
    };
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        handleUpdateSections();
        const slotHandleUpdateSections = (e) => {
            handleUpdateSections();
        };
        const fileSignal = docTrack.services.contents.fileChanged;
        fileSignal.connect(slotHandleUpdateSections);
        return () => {
            fileSignal.disconnect(slotHandleUpdateSections);
        };
    }, []);
    if (notebooks.length === 0) {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement((react__WEBPACK_IMPORTED_MODULE_2___default().Fragment), null));
    }
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialsLauncherList" },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialsLauncherListHeader" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", null, name),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("ul", { className: "tutorialsLauncherListHeaderToolbar" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LauncherTooltip, { tooltip: tooltip })))),
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("ul", { className: "tutorialsLauncherListGrid" }, notebooks.map(Item => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", { key: `notebookItem-${Item.path}` },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LauncherNotebookListItem, { TrackedNotebook: Item, action: () => _lib__WEBPACK_IMPORTED_MODULE_5__.actionCallbacks[action](Item.path, docTrack, setting), icon: icon })))))));
};
class Epi2melabsLauncherWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(setting, docTrack, sections) {
        super();
        this.docTrack = docTrack;
        this.sections = sections;
        this.setting = setting;
        this.addClass('jp-ReactWidget');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "tutorialsLauncher" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LauncherHeader, null),
            this.sections.map(Item => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LauncherNotebookList, { key: `notebook-${Item.name}`, TrackedNotebookList: Item, docTrack: this.docTrack, setting: this.setting }))),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LauncherFooter, null)));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.04ac4efcb5011272f5a3.js.map