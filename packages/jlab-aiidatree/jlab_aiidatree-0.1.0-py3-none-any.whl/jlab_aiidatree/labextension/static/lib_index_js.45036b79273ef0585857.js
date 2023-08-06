(self["webpackChunkjlab_aiidatree"] = self["webpackChunkjlab_aiidatree"] || []).push([["lib_index_js"],{

/***/ "./lib/consts.js":
/*!***********************!*\
  !*** ./lib/consts.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "connectIcon": () => (/* binding */ connectIcon),
/* harmony export */   "statusUnknownIcon": () => (/* binding */ statusUnknownIcon),
/* harmony export */   "cogIcon": () => (/* binding */ cogIcon),
/* harmony export */   "statusPausedIcon": () => (/* binding */ statusPausedIcon),
/* harmony export */   "homeIcon": () => (/* binding */ homeIcon),
/* harmony export */   "linkExternalIcon": () => (/* binding */ linkExternalIcon),
/* harmony export */   "tagIcon": () => (/* binding */ tagIcon),
/* harmony export */   "databaseIcon": () => (/* binding */ databaseIcon),
/* harmony export */   "fileIcon": () => (/* binding */ fileIcon),
/* harmony export */   "terminalIcon": () => (/* binding */ terminalIcon),
/* harmony export */   "keyIcon": () => (/* binding */ keyIcon),
/* harmony export */   "packageDependentsIcon": () => (/* binding */ packageDependentsIcon),
/* harmony export */   "beakerIcon": () => (/* binding */ beakerIcon),
/* harmony export */   "settingsIcon": () => (/* binding */ settingsIcon),
/* harmony export */   "archiveIcon": () => (/* binding */ archiveIcon),
/* harmony export */   "subFolderIcon": () => (/* binding */ subFolderIcon),
/* harmony export */   "statusKilledIcon": () => (/* binding */ statusKilledIcon),
/* harmony export */   "statusSucceededIcon": () => (/* binding */ statusSucceededIcon),
/* harmony export */   "refreshIcon": () => (/* binding */ refreshIcon),
/* harmony export */   "checkCircleIcon": () => (/* binding */ checkCircleIcon),
/* harmony export */   "statusRunningIcon": () => (/* binding */ statusRunningIcon),
/* harmony export */   "statusExceptedIcon": () => (/* binding */ statusExceptedIcon),
/* harmony export */   "packageDependenciesIcon": () => (/* binding */ packageDependenciesIcon),
/* harmony export */   "repoIcon": () => (/* binding */ repoIcon),
/* harmony export */   "computerIcon": () => (/* binding */ computerIcon),
/* harmony export */   "statusFailedIcon": () => (/* binding */ statusFailedIcon),
/* harmony export */   "filterIcon": () => (/* binding */ filterIcon),
/* harmony export */   "statusCreatedIcon": () => (/* binding */ statusCreatedIcon),
/* harmony export */   "listUnorderedIcon": () => (/* binding */ listUnorderedIcon),
/* harmony export */   "statusWaitingIcon": () => (/* binding */ statusWaitingIcon),
/* harmony export */   "rocketIcon": () => (/* binding */ rocketIcon),
/* harmony export */   "calculatorIcon": () => (/* binding */ calculatorIcon),
/* harmony export */   "graphIcon": () => (/* binding */ graphIcon),
/* harmony export */   "folderIcon": () => (/* binding */ folderIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_light_connect_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/light/connect.svg */ "./style/icons/light/connect.svg");
/* harmony import */ var _style_icons_light_statusUnknown_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/light/statusUnknown.svg */ "./style/icons/light/statusUnknown.svg");
/* harmony import */ var _style_icons_light_cog_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/light/cog.svg */ "./style/icons/light/cog.svg");
/* harmony import */ var _style_icons_light_statusPaused_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/light/statusPaused.svg */ "./style/icons/light/statusPaused.svg");
/* harmony import */ var _style_icons_light_home_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/light/home.svg */ "./style/icons/light/home.svg");
/* harmony import */ var _style_icons_light_link_external_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/icons/light/link-external.svg */ "./style/icons/light/link-external.svg");
/* harmony import */ var _style_icons_light_tag_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/icons/light/tag.svg */ "./style/icons/light/tag.svg");
/* harmony import */ var _style_icons_light_database_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/icons/light/database.svg */ "./style/icons/light/database.svg");
/* harmony import */ var _style_icons_light_file_svg__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/icons/light/file.svg */ "./style/icons/light/file.svg");
/* harmony import */ var _style_icons_light_terminal_svg__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../style/icons/light/terminal.svg */ "./style/icons/light/terminal.svg");
/* harmony import */ var _style_icons_light_key_svg__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../style/icons/light/key.svg */ "./style/icons/light/key.svg");
/* harmony import */ var _style_icons_light_package_dependents_svg__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../style/icons/light/package-dependents.svg */ "./style/icons/light/package-dependents.svg");
/* harmony import */ var _style_icons_light_beaker_svg__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../style/icons/light/beaker.svg */ "./style/icons/light/beaker.svg");
/* harmony import */ var _style_icons_light_settings_svg__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../style/icons/light/settings.svg */ "./style/icons/light/settings.svg");
/* harmony import */ var _style_icons_light_archive_svg__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ../style/icons/light/archive.svg */ "./style/icons/light/archive.svg");
/* harmony import */ var _style_icons_light_sub_folder_svg__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../style/icons/light/sub-folder.svg */ "./style/icons/light/sub-folder.svg");
/* harmony import */ var _style_icons_light_statusKilled_svg__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ../style/icons/light/statusKilled.svg */ "./style/icons/light/statusKilled.svg");
/* harmony import */ var _style_icons_light_statusSucceeded_svg__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ../style/icons/light/statusSucceeded.svg */ "./style/icons/light/statusSucceeded.svg");
/* harmony import */ var _style_icons_light_refresh_svg__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ../style/icons/light/refresh.svg */ "./style/icons/light/refresh.svg");
/* harmony import */ var _style_icons_light_check_circle_svg__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ../style/icons/light/check-circle.svg */ "./style/icons/light/check-circle.svg");
/* harmony import */ var _style_icons_light_statusRunning_svg__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ../style/icons/light/statusRunning.svg */ "./style/icons/light/statusRunning.svg");
/* harmony import */ var _style_icons_light_statusExcepted_svg__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ../style/icons/light/statusExcepted.svg */ "./style/icons/light/statusExcepted.svg");
/* harmony import */ var _style_icons_light_package_dependencies_svg__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ../style/icons/light/package-dependencies.svg */ "./style/icons/light/package-dependencies.svg");
/* harmony import */ var _style_icons_light_repo_svg__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ../style/icons/light/repo.svg */ "./style/icons/light/repo.svg");
/* harmony import */ var _style_icons_light_computer_svg__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ../style/icons/light/computer.svg */ "./style/icons/light/computer.svg");
/* harmony import */ var _style_icons_light_statusFailed_svg__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ../style/icons/light/statusFailed.svg */ "./style/icons/light/statusFailed.svg");
/* harmony import */ var _style_icons_light_filter_svg__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ../style/icons/light/filter.svg */ "./style/icons/light/filter.svg");
/* harmony import */ var _style_icons_light_statusCreated_svg__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! ../style/icons/light/statusCreated.svg */ "./style/icons/light/statusCreated.svg");
/* harmony import */ var _style_icons_light_list_unordered_svg__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! ../style/icons/light/list-unordered.svg */ "./style/icons/light/list-unordered.svg");
/* harmony import */ var _style_icons_light_statusWaiting_svg__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! ../style/icons/light/statusWaiting.svg */ "./style/icons/light/statusWaiting.svg");
/* harmony import */ var _style_icons_light_rocket_svg__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! ../style/icons/light/rocket.svg */ "./style/icons/light/rocket.svg");
/* harmony import */ var _style_icons_light_calculator_svg__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! ../style/icons/light/calculator.svg */ "./style/icons/light/calculator.svg");
/* harmony import */ var _style_icons_light_graph_svg__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! ../style/icons/light/graph.svg */ "./style/icons/light/graph.svg");
/* harmony import */ var _style_icons_light_folder_svg__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! ../style/icons/light/folder.svg */ "./style/icons/light/folder.svg");

const CommandIDs = {
    refresh: 'aiidatree:refresh',
    inspectNode: 'aiidatree:nodeData',
    setContext: 'aiidatree:setContext',
    select: 'aiidatree:select',
    toggle: 'aiidatree:toggle',
    launchThreeJS: 'aiidatree:threejs',
    launchD3: 'aiidatree:d3'
};

const connectIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:connect',
    svgstr: _style_icons_light_connect_svg__WEBPACK_IMPORTED_MODULE_1__.default
});

const statusUnknownIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusUnknown',
    svgstr: _style_icons_light_statusUnknown_svg__WEBPACK_IMPORTED_MODULE_2__.default
});

const cogIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:cog',
    svgstr: _style_icons_light_cog_svg__WEBPACK_IMPORTED_MODULE_3__.default
});

const statusPausedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusPaused',
    svgstr: _style_icons_light_statusPaused_svg__WEBPACK_IMPORTED_MODULE_4__.default
});

const homeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:home',
    svgstr: _style_icons_light_home_svg__WEBPACK_IMPORTED_MODULE_5__.default
});

const linkExternalIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:link-external',
    svgstr: _style_icons_light_link_external_svg__WEBPACK_IMPORTED_MODULE_6__.default
});

const tagIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:tag',
    svgstr: _style_icons_light_tag_svg__WEBPACK_IMPORTED_MODULE_7__.default
});

const databaseIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:database',
    svgstr: _style_icons_light_database_svg__WEBPACK_IMPORTED_MODULE_8__.default
});

const fileIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:file',
    svgstr: _style_icons_light_file_svg__WEBPACK_IMPORTED_MODULE_9__.default
});

const terminalIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:terminal',
    svgstr: _style_icons_light_terminal_svg__WEBPACK_IMPORTED_MODULE_10__.default
});

const keyIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:key',
    svgstr: _style_icons_light_key_svg__WEBPACK_IMPORTED_MODULE_11__.default
});

const packageDependentsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:package-dependents',
    svgstr: _style_icons_light_package_dependents_svg__WEBPACK_IMPORTED_MODULE_12__.default
});

const beakerIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:beaker',
    svgstr: _style_icons_light_beaker_svg__WEBPACK_IMPORTED_MODULE_13__.default
});

const settingsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:settings',
    svgstr: _style_icons_light_settings_svg__WEBPACK_IMPORTED_MODULE_14__.default
});

const archiveIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:archive',
    svgstr: _style_icons_light_archive_svg__WEBPACK_IMPORTED_MODULE_15__.default
});

const subFolderIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:sub-folder',
    svgstr: _style_icons_light_sub_folder_svg__WEBPACK_IMPORTED_MODULE_16__.default
});

const statusKilledIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusKilled',
    svgstr: _style_icons_light_statusKilled_svg__WEBPACK_IMPORTED_MODULE_17__.default
});

const statusSucceededIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusSucceeded',
    svgstr: _style_icons_light_statusSucceeded_svg__WEBPACK_IMPORTED_MODULE_18__.default
});

const refreshIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:refresh',
    svgstr: _style_icons_light_refresh_svg__WEBPACK_IMPORTED_MODULE_19__.default
});

const checkCircleIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:check-circle',
    svgstr: _style_icons_light_check_circle_svg__WEBPACK_IMPORTED_MODULE_20__.default
});

const statusRunningIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusRunning',
    svgstr: _style_icons_light_statusRunning_svg__WEBPACK_IMPORTED_MODULE_21__.default
});

const statusExceptedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusExcepted',
    svgstr: _style_icons_light_statusExcepted_svg__WEBPACK_IMPORTED_MODULE_22__.default
});

const packageDependenciesIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:package-dependencies',
    svgstr: _style_icons_light_package_dependencies_svg__WEBPACK_IMPORTED_MODULE_23__.default
});

const repoIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:repo',
    svgstr: _style_icons_light_repo_svg__WEBPACK_IMPORTED_MODULE_24__.default
});

const computerIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:computer',
    svgstr: _style_icons_light_computer_svg__WEBPACK_IMPORTED_MODULE_25__.default
});

const statusFailedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusFailed',
    svgstr: _style_icons_light_statusFailed_svg__WEBPACK_IMPORTED_MODULE_26__.default
});

const filterIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:filter',
    svgstr: _style_icons_light_filter_svg__WEBPACK_IMPORTED_MODULE_27__.default
});

const statusCreatedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusCreated',
    svgstr: _style_icons_light_statusCreated_svg__WEBPACK_IMPORTED_MODULE_28__.default
});

const listUnorderedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:list-unordered',
    svgstr: _style_icons_light_list_unordered_svg__WEBPACK_IMPORTED_MODULE_29__.default
});

const statusWaitingIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:statusWaiting',
    svgstr: _style_icons_light_statusWaiting_svg__WEBPACK_IMPORTED_MODULE_30__.default
});

const rocketIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:rocket',
    svgstr: _style_icons_light_rocket_svg__WEBPACK_IMPORTED_MODULE_31__.default
});

const calculatorIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:calculator',
    svgstr: _style_icons_light_calculator_svg__WEBPACK_IMPORTED_MODULE_32__.default
});

const graphIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:graph',
    svgstr: _style_icons_light_graph_svg__WEBPACK_IMPORTED_MODULE_33__.default
});

const folderIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'aiidatree:folder',
    svgstr: _style_icons_light_folder_svg__WEBPACK_IMPORTED_MODULE_34__.default
});


/***/ }),

/***/ "./lib/d3graph_widget.js":
/*!*******************************!*\
  !*** ./lib/d3graph_widget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "D3GraphWidget": () => (/* binding */ D3GraphWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(d3__WEBPACK_IMPORTED_MODULE_1__);


class D3GraphWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(id, label) {
        super();
        this.id = id;
        this.title.label = label;
        this.title.closable = true;
        this.addClass('aiidatree-d3graph');
    }
    render(nodes_data, links_data, root) {
        // nodes_data is INodeLink interface with 'name' field equal to pk
        // links_data is INodeLink interface with 'source'/'target' field equal to pk
        // root is root pk
        const width = 500;
        const height = 500;
        //create the SVG, within which to put the force directed graph
        const svg = d3__WEBPACK_IMPORTED_MODULE_1__.select(this.node)
            .append('div')
            .classed('d3-svg-container', true)
            .append('svg')
            .attr('preserveAspectRatio', 'xMinYMin meet')
            .attr('viewBox', `0 0 ${width} ${height}`)
            .classed('d3-svg-content-responsive', true)
            .attr('width', width)
            .attr('height', height);
        //set up the simulation and add nodes
        const simulation = d3__WEBPACK_IMPORTED_MODULE_1__.forceSimulation().nodes(nodes_data);
        //add forces; a charge to each node, and a centring force
        simulation
            .force('charge_force', d3__WEBPACK_IMPORTED_MODULE_1__.forceManyBody())
            .force('center_force', d3__WEBPACK_IMPORTED_MODULE_1__.forceCenter(width / 2, height / 2));
        // Create the link force
        // We need the id accessor to use named sources and targets
        const link_force = d3__WEBPACK_IMPORTED_MODULE_1__.forceLink(links_data)
            .distance(width / 10)
            .id((d) => {
            return d.name;
        });
        //Add a links force to the simulation
        //Specify links  in d3.forceLink argument
        simulation.force('links', link_force);
        // draw links, nodes and labels in correct z-index order
        // draw lines for the links
        const link = svg
            .append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(links_data)
            .enter()
            .append('line')
            .attr('stroke-width', 2)
            .attr('stroke', (d) => {
            return d.direction === 'incoming' ? 'green' : 'blue';
        });
        // draw circles for the nodes
        // attr accepts a static value or a function which passes the node dict (plus index/positional data)
        const node = svg
            .append('g')
            .attr('class', 'nodes')
            .selectAll('circle')
            .data(nodes_data)
            .enter()
            .append('circle')
            .attr('r', 7)
            .attr('fill', d => {
            return d.name === root ? 'red' : 'orange';
        });
        // Draw node labels
        const label = svg
            .append('g')
            .attr('class', 'labels')
            .selectAll('text')
            .data(nodes_data)
            .enter()
            .append('text')
            // .attr("dx", 12)
            // .attr("dy", ".35em")
            .text(d => {
            return d.name;
        });
        // add tick instructions:
        simulation.on('tick', tickActions);
        function tickActions() {
            //update circle positions each tick of the simulation
            node
                .attr('cx', d => {
                return d.x;
            })
                .attr('cy', d => {
                return d.y;
            });
            label
                .attr('x', d => {
                return d.x;
            })
                .attr('y', d => {
                return d.y;
            });
            //update link positions
            //simply tells one end of the line to follow one node around
            //and the other end of the line to follow the other node around
            link
                .attr('x1', (d) => {
                return d.source.x;
            })
                .attr('y1', (d) => {
                return d.source.y;
            })
                .attr('x2', (d) => {
                return d.target.x;
            })
                .attr('y2', (d) => {
                return d.target.y;
            });
        }
    }
}


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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _tree_widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tree_widget */ "./lib/tree_widget.js");



const PLUGIN_ID = 'jlab_aiidatree:settings-aiidatree';
/**
 * Initialization data for the jlab_aiidatree extension.
 */
const extension = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: async (app, resolver, settings) => {
        console.log('JupyterLab extension jlab_aiidatree is activated!');
        // await app.restored  // this was in the tutorial but it hangs
        const loadedSettings = await settings.load(PLUGIN_ID);
        const widget = (0,_tree_widget__WEBPACK_IMPORTED_MODULE_2__.constructTreeWidget)(app, 'jlab_aiidatree', 'left', resolver, loadedSettings);
        await widget.refresh();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/json_widget.js":
/*!****************************!*\
  !*** ./lib/json_widget.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JSONWidget": () => (/* binding */ JSONWidget)
/* harmony export */ });
/* harmony import */ var js_yaml__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-yaml */ "webpack/sharing/consume/default/js-yaml/js-yaml");
/* harmony import */ var js_yaml__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_yaml__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);


class JSONWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor(id, label, caption) {
        super();
        this.id = id;
        this.title.label = label;
        this.title.caption = caption;
        this.title.closable = true;
        this.addClass('aiidatree-yaml');
    }
    render(data) {
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.className = 'language-yaml';
        code.innerText = (0,js_yaml__WEBPACK_IMPORTED_MODULE_0__.dump)(data, { indent: 2 });
        pre.appendChild(code);
        this.node.appendChild(pre);
    }
}
// see: https://github.com/jupyterlab/jupyterlab/blob/master/packages/docmanager-extension/src/index.ts
// // Create a new untitled python file
// const model = await app.commands.execute('docmanager:new-untitled', {
//     type: 'file',
//     ext: 'json'
// });
// // Open the newly created file with the 'Editor'
// return app.commands.execute('docmanager:open', {
//     path: model.path,
//     factory: 'Editor'
// });


/***/ }),

/***/ "./lib/rest.js":
/*!*********************!*\
  !*** ./lib/rest.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI),
/* harmony export */   "queryProcesses": () => (/* binding */ queryProcesses),
/* harmony export */   "queryNode": () => (/* binding */ queryNode),
/* harmony export */   "queryLinks": () => (/* binding */ queryLinks)
/* harmony export */ });
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);



/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'jlab_aiidatree', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function queryProcesses(maxRecords = 1, dbSettings) {
    const dataToSend = Object.assign({ max_records: maxRecords }, dbSettings);
    let reply;
    try {
        reply = await requestAPI('processes', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
    }
    catch (reason) {
        console.warn(`Error on POST /jlab_aiidatree/processes ${dataToSend}.\n${reason}`);
        // TODO deal with errors 
        // (we don't want to crash the program, just because the database is not available)
        return [];
    }
    const output = reply.rows.map(row => lodash__WEBPACK_IMPORTED_MODULE_0__.zipObject(reply.fields, row));
    return output;
}
async function queryNode(pk, dbSettings) {
    const dataToSend = Object.assign({ pk }, dbSettings);
    let reply;
    try {
        reply = await requestAPI('node', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
    }
    catch (reason) {
        console.warn(`Error on POST /jlab_aiidatree/node ${dataToSend}.\n${reason}`);
        // TODO deal with errors
    }
    return reply;
}
async function queryLinks(pk, direction, dbSettings) {
    const dataToSend = Object.assign({ pk, direction }, dbSettings);
    let reply;
    try {
        reply = await requestAPI('links', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
    }
    catch (reason) {
        console.warn(`Error on POST /jlab_aiidatree/links ${dataToSend}.\n${reason}`);
        // TODO deal with errors
        return [];
    }
    const output = reply.rows.map(row => lodash__WEBPACK_IMPORTED_MODULE_0__.zipObject(reply.fields, row));
    return output;
}


/***/ }),

/***/ "./lib/threejs_widget.js":
/*!*******************************!*\
  !*** ./lib/threejs_widget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ThreeJSWidget": () => (/* binding */ ThreeJSWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var three__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! three */ "webpack/sharing/consume/default/three/three");
/* harmony import */ var three__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(three__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var three_examples_jsm_controls_OrbitControls__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! three/examples/jsm/controls/OrbitControls */ "./node_modules/three/examples/jsm/controls/OrbitControls.js");
// adapted from https://github.com/pschatzmann/jupyterlab-viewer-3d



class ThreeJSWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(id, label) {
        super();
        this.scene = new three__WEBPACK_IMPORTED_MODULE_1__.Scene();
        this.renderer = new three__WEBPACK_IMPORTED_MODULE_1__.WebGLRenderer({ antialias: true, alpha: true });
        this.camera = new three__WEBPACK_IMPORTED_MODULE_1__.PerspectiveCamera(40, this.node.clientWidth / this.node.clientHeight, 1, 1000);
        this.controls = new three_examples_jsm_controls_OrbitControls__WEBPACK_IMPORTED_MODULE_2__.OrbitControls(this.camera, this.renderer.domElement);
        this.id = id;
        this.title.label = label;
        this.title.closable = true;
        this.addClass('aiidatree-threejs');
    }
    initialise() {
        this.scene.background = new three__WEBPACK_IMPORTED_MODULE_1__.Color(0x999999);
        this.scene.add(new three__WEBPACK_IMPORTED_MODULE_1__.AmbientLight(0xffffff));
        this.camera.add(new three__WEBPACK_IMPORTED_MODULE_1__.PointLight(0xffffff, 0.8));
        this.camera.up.set(0, 0, 1);
        this.scene.add(this.camera);
        const grid = new three__WEBPACK_IMPORTED_MODULE_1__.GridHelper(200, 20, 0xffffff, 0x555555);
        grid.rotation.x = Math.PI / 2;
        this.scene.add(grid);
        this.controls.enableZoom = true;
        this.controls.enabled = true;
        this.node.appendChild(this.renderer.domElement);
        // handle resizing
        window.addEventListener('resize', event => {
            this.resize();
        }, false);
        // handle mouse events
        this.controls.addEventListener('change', event => {
            this.render();
        });
        this.controls.update();
        // setup width/height
        this.renderer.setPixelRatio(window.devicePixelRatio);
        // const meshes = [this.create_atom({x: 0, y: 0, z: 0}), this.create_atom({x: 0, y: 5, z: 0}), this.create_atom({x: 0, y: 0, z: 5}), this.create_atom({x: 0, y: 5, z: 5})]
        // this.fitCameraToMeshes(meshes, this.camera, this.controls);
        // this.scene.add(...meshes);
        this.resize();
    }
    render() {
        this.renderer.render(this.scene, this.camera);
    }
    resize() {
        this.renderer.setSize(this.node.clientWidth, this.node.clientHeight);
        this.camera.aspect = this.node.clientWidth / this.node.clientHeight;
        this.camera.updateProjectionMatrix();
        this.render();
    }
    create_atom(position, radius = 1, color = 'blue', opacity = 0.9) {
        const geometry = new three__WEBPACK_IMPORTED_MODULE_1__.SphereBufferGeometry(radius, 30, 30);
        const material = new three__WEBPACK_IMPORTED_MODULE_1__.MeshLambertMaterial({
            color,
            transparent: true,
            opacity
        });
        const mesh = new three__WEBPACK_IMPORTED_MODULE_1__.Mesh(geometry, material);
        const { x, y, z } = position;
        mesh.position.set(x, y, z);
        return mesh;
    }
    renderStructureData(data) {
        // TODO handle errors
        const sites = data['attributes']['sites'];
        const meshes = sites.reduce((a, site) => {
            a.push(this.create_atom({
                x: site['position'][0],
                y: site['position'][1],
                z: site['position'][2]
            }));
            return a;
        }, []);
        this.fitCameraToMeshes(meshes, this.camera, this.controls);
        this.scene.add(...meshes);
        this.resize();
    }
    fitCameraToMeshes(meshes, camera, controls) {
        const offset = 1.25;
        const points = meshes.reduce((a, m) => {
            a.push(m.position);
            return a;
        }, []);
        const boundingBox = new three__WEBPACK_IMPORTED_MODULE_1__.Box3();
        // get bounding box of object - this will be used to setup controls and camera
        boundingBox.setFromPoints(points);
        const center = new three__WEBPACK_IMPORTED_MODULE_1__.Vector3();
        boundingBox.getCenter(center);
        const size = new three__WEBPACK_IMPORTED_MODULE_1__.Vector3();
        boundingBox.getSize(size);
        // get the max side of the bounding box (fits to width OR height as needed )
        const maxDim = Math.max(size.x, size.y, size.z) + 1; // TODO find max radius
        const fov = this.camera.fov * (Math.PI / 180);
        let cameraZ = Math.abs((maxDim / 4) * Math.tan(fov * 2));
        cameraZ *= offset; // zoom out a little so that objects don't fill the scree
        camera.position.z = cameraZ;
        const minZ = boundingBox.min.z;
        const cameraToFarEdge = minZ < 0 ? -minZ + cameraZ : cameraZ - minZ;
        camera.far = cameraToFarEdge * 3;
        camera.updateProjectionMatrix();
        // set camera to rotate around center of loaded object
        controls.target = center;
        // prevent camera from zooming out far enough to create far plane cutoff
        controls.maxDistance = cameraToFarEdge * 2;
        controls.saveState();
    }
}


/***/ }),

/***/ "./lib/tree_widget.js":
/*!****************************!*\
  !*** ./lib/tree_widget.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "constructTreeWidget": () => (/* binding */ constructTreeWidget),
/* harmony export */   "AiidaTreeWidget": () => (/* binding */ AiidaTreeWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _consts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./consts */ "./lib/consts.js");
/* harmony import */ var _rest__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./rest */ "./lib/rest.js");
/* harmony import */ var _threejs_widget__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./threejs_widget */ "./lib/threejs_widget.js");
/* harmony import */ var _json_widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./json_widget */ "./lib/json_widget.js");
/* harmony import */ var _d3graph_widget__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./d3graph_widget */ "./lib/d3graph_widget.js");











function constructTreeWidget(app, id, side = 'left', restorer, loadedSettings) {
    const widget = new AiidaTreeWidget(app, id, loadedSettings);
    restorer.add(widget, widget.id);
    app.shell.add(widget, side);
    createCoreCommands(app, widget);
    createItemsContextMenu(app, widget);
    createMainToolbar(app, widget);
    return widget;
}
class AiidaTreeWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(app, id, loadedSettings) {
        super();
        this.id = id;
        this.title.iconClass = 'aiidatree-icon';
        this.title.caption = 'AiiDA Explorer';
        this.title.closable = true;
        this.addClass('jp-aiidatreeWidget');
        this.addClass(id);
        this.refreshSettings(loadedSettings);
        loadedSettings.changed.connect(() => {
            this.refreshSettings(loadedSettings);
        });
        this.commands = app.commands;
        this.toolbar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Toolbar();
        this.toolbar.addClass('aiidatree-toolbar');
        this.toolbar.addClass(id);
        const layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout();
        layout.addWidget(this.toolbar);
        this.layout = layout;
        this.selected_pk = undefined;
        // const label = document.createElement("label");
        // this.node.appendChild(label)
        // label.htmlFor = "selection"
        const select = document.createElement('select');
        select.className = 'aiidatree-process-select';
        select.name = `${this.id}-selection`;
        select.id = select.name;
        const states = [
            'all',
            'created',
            'running',
            'waiting',
            'finished',
            'excepted',
            'killed'
        ];
        for (const state of states) {
            const option = document.createElement('option');
            option.value = state;
            option.innerHTML = state.toUpperCase();
            select.appendChild(option);
        }
        this.node.appendChild(select);
        this.selectProcessState = select;
        select.onchange = async () => {
            await this.refresh();
        };
    }
    refreshSettings(loadedSettings) {
        const keys = ['host', 'port', 'user', 'database', 'password'];
        this.dbSettings = keys.reduce((d, k) => {
            d[k] = loadedSettings.get(k).composite;
            return d;
        }, {});
    }
    async refresh() {
        if (typeof this.processTable !== 'undefined') {
            try {
                this.node.removeChild(this.processTable);
            }
            catch (error) {
                console.warn(error);
            }
        }
        await this.buildProcessesTable();
    }
    buildHTMLTable(headers, classPrefix = 'aiidatree') {
        /**
         * Build a HTML Table
         *
         * @param  {string[]} headers
         * @param  {any} data
         */
        const table = document.createElement('table');
        table.className = `${classPrefix}-head`;
        const thead = table.createTHead();
        const tbody = table.createTBody();
        tbody.id = `${classPrefix}-body`;
        const headRow = document.createElement('tr');
        headers.forEach((el) => {
            const th = document.createElement('th');
            th.className = `${classPrefix}-header`;
            th.appendChild(document.createTextNode(el));
            headRow.appendChild(th);
        });
        headRow.children[headRow.children.length - 1].className += ' modified';
        thead.appendChild(headRow);
        table.appendChild(thead);
        table.appendChild(tbody);
        return { table, tbody };
    }
    buildTableRow(row, id, icon) {
        const tr = document.createElement('tr');
        row.forEach((column, index) => {
            const td = document.createElement('td');
            if (index === 0) {
                td.className = 'aiidatree-first-column';
                icon.element({ container: td, marginRight: '6px', maxHeight: '12px' });
            }
            const content = document.createElement('span');
            content.innerHTML = `${column}`;
            td.appendChild(content);
            tr.appendChild(td);
        });
        // for (const column of row) {
        // }
        tr.className = 'aiidatree-item';
        tr.id = id;
        return tr;
    }
    async buildProcessesTable() {
        let processes = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryProcesses)(100, this.dbSettings);
        processes = (0,lodash__WEBPACK_IMPORTED_MODULE_3__.sortBy)(processes, ['id']);
        const html = this.buildHTMLTable(['PK', 'Label', 'State']);
        for (const process of processes) {
            // TODO should do that filtering at the query level
            if (this.selectProcessState.value === 'all' ||
                process.processState === this.selectProcessState.value) {
                const tr = this.buildTableRow([
                    process.id,
                    process.processLabel,
                    process.processState.toUpperCase()
                ], `${process.id}`, _consts__WEBPACK_IMPORTED_MODULE_6__.rocketIcon);
                html.tbody.appendChild(tr);
                tr.className += ' jp-icon-selectable';
                tr.oncontextmenu = () => {
                    this.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.setContext + ':' + this.id, {
                        pk: process.id
                    });
                };
                tr.onclick = event => {
                    event.stopPropagation();
                    event.preventDefault();
                    this.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.setContext + ':' + this.id, {
                        pk: process.id
                    });
                    this.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.toggle + ':' + this.id, {
                        pk: process.id
                    });
                };
                // can interfere with toggling
                // tr.ondblclick = () => {
                //     this.commands.execute(CommandIDs.inspectNode + ":" + this.id, { pk: process.id })
                // }
            }
        }
        this.processTable = html.table;
        this.node.appendChild(html.table);
    }
}
function createCoreCommands(app, widget) {
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.refresh + ':' + widget.id, {
        execute: args => {
            widget.refresh();
        }
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.setContext + ':' + widget.id, {
        execute: args => {
            if (typeof widget.selected_pk !== 'undefined') {
                const element = widget.node.querySelector(`[id='${widget.selected_pk}']`);
                if (element !== null) {
                    element.className = element.className.replace('selected', '');
                }
            }
            widget.selected_pk = args.pk;
            if (typeof widget.selected_pk !== 'undefined') {
                const element = widget.node.querySelector(`[id='${widget.selected_pk}']`);
                if (element !== null) {
                    element.className += ' selected';
                }
            }
        },
        label: 'Need some Context'
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.select + ':' + widget.id, {
        execute: args => {
            if (typeof widget.selected_pk !== 'undefined') {
                const element = widget.node.querySelector(`[id='${widget.selected_pk}']`);
                if (element !== null) {
                    element.className = element.className.replace('selected', '');
                }
            }
            if (typeof args.pk === 'undefined') {
                return;
            }
            widget.selected_pk = args.pk;
            const element = widget.node.querySelector(`[id='${widget.selected_pk}']`);
            if (element !== null) {
                element.className += ' selected';
            }
        },
        label: 'Select'
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.toggle + ':' + widget.id, {
        execute: async (args) => {
            const pk = args.pk;
            let row_element = widget.node.querySelector(`[id='${pk}']`);
            if (row_element.nextElementSibling &&
                row_element.nextElementSibling.id.startsWith(`${pk}/`)) {
                // child elements already constructed and need to be removed
                const remove_elements = [];
                while (row_element.nextElementSibling &&
                    row_element.nextElementSibling.id.startsWith(`${pk}/`)) {
                    row_element = widget.node.querySelector("[id='" + row_element.nextElementSibling.id + "']");
                    remove_elements.push(row_element);
                }
                for (const element of remove_elements) {
                    element.remove();
                }
            }
            else {
                // child elements need to be constructed
                let next_element;
                const next_elements = [];
                let icon;
                let arrow;
                for (const direction of ['incoming', 'outgoing']) {
                    const links = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryLinks)(pk, direction, widget.dbSettings);
                    for (const link of links) {
                        // Take the last part of the entry point
                        const typeElements = link.nodeType.split('.');
                        const name = typeElements[typeElements.length - 2];
                        icon = getIcon(link.nodeType);
                        arrow = direction === 'incoming' ? '→' : '←';
                        next_element = widget.buildTableRow([link.nodeId, name, arrow], `${pk}/${link.nodeId}`, icon);
                        next_element.className += ` aiidatree-link-item aiidatree-link-${direction} aiidatree-item-${name}`;
                        next_element.oncontextmenu = () => {
                            widget.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.setContext + ':' + widget.id, {
                                pk: link.nodeId
                            });
                        };
                        next_element.onclick = () => {
                            widget.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.setContext + ':' + widget.id, {
                                pk: link.nodeId
                            });
                            widget.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.select + ':' + widget.id, {
                                pk: link.nodeId
                            });
                        };
                        next_elements.push(next_element);
                    }
                }
                row_element.after(...next_elements);
            }
        }
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.inspectNode + ':' + widget.id, {
        execute: async (args) => {
            const pk = typeof args['pk'] === 'undefined'
                ? widget.selected_pk
                : args['pk'];
            const data = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryNode)(pk, widget.dbSettings);
            const inspectWidget = new _json_widget__WEBPACK_IMPORTED_MODULE_7__.JSONWidget(`${widget.id}-pk-${pk}`, `Inspect Node ${pk}`, "Inspect a node's data");
            inspectWidget.render(data);
            app.shell.add(inspectWidget, 'main');
        },
        label: 'Inspect'
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.launchD3 + ':' + widget.id, {
        execute: async (args) => {
            const pk = typeof args['pk'] === 'undefined'
                ? widget.selected_pk
                : args['pk'];
            const d3Widget = new _d3graph_widget__WEBPACK_IMPORTED_MODULE_8__.D3GraphWidget(`${widget.id}-d3-${pk}`, `Graph Node ${pk}`);
            const nodes_data = { pk: { name: pk } };
            const links_data = [];
            // for (const direction of ["incoming", "outgoing"]) {
            const linksIn = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryLinks)(pk, 'incoming', widget.dbSettings);
            for (const link of linksIn) {
                nodes_data[link.nodeId] = Object.assign({ name: link.nodeId }, link);
                links_data.push(Object.assign({ source: pk, target: link.nodeId, direction: 'incoming' }, link));
            }
            const linksOut = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryLinks)(pk, 'outgoing', widget.dbSettings);
            for (const link of linksOut) {
                nodes_data[link.nodeId] = Object.assign({ name: link.nodeId }, link);
                links_data.push(Object.assign({ source: pk, target: link.nodeId, direction: 'outgoing' }, link));
            }
            d3Widget.render((0,lodash__WEBPACK_IMPORTED_MODULE_3__.values)(nodes_data), links_data, pk);
            app.shell.add(d3Widget, 'main');
        },
        label: 'Graph'
    });
    app.commands.addCommand(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.launchThreeJS + ':' + widget.id, {
        execute: async (args) => {
            const pk = typeof args['pk'] === 'undefined'
                ? widget.selected_pk
                : args['pk'];
            const data = await (0,_rest__WEBPACK_IMPORTED_MODULE_5__.queryNode)(pk, widget.dbSettings);
            const threejs_widget = new _threejs_widget__WEBPACK_IMPORTED_MODULE_9__.ThreeJSWidget(`${widget.id}-view-${pk}`, `Visualise Structure ${pk}`);
            app.shell.add(threejs_widget, 'main');
            threejs_widget.initialise();
            threejs_widget.renderStructureData(data);
        },
        label: 'Visualise'
    });
}
function createItemsContextMenu(app, widget) {
    app.contextMenu.addItem({
        command: _consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.inspectNode + ':' + widget.id,
        rank: 3,
        selector: 'div.' + widget.id + ' > table > *> .aiidatree-item'
    });
    app.contextMenu.addItem({
        command: _consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.launchThreeJS + ':' + widget.id,
        rank: 3,
        selector: 'div.' + widget.id + ' > table > *> .aiidatree-item-StructureData'
    });
    app.contextMenu.addItem({
        command: _consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.launchD3 + ':' + widget.id,
        rank: 3,
        selector: 'div.' + widget.id + ' > table > *> .aiidatree-item'
    });
}
function createMainToolbar(app, widget) {
    const refresh = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.refreshIcon,
        onClick: () => {
            app.commands.execute(_consts__WEBPACK_IMPORTED_MODULE_6__.CommandIDs.refresh + ':' + widget.id);
        },
        tooltip: 'Refresh'
    });
    widget.toolbar.addItem('refresh', refresh);
}
const nodeIconMatches = [
    { type: 'data.code', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.terminalIcon },
    { type: 'data.dict', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.listUnorderedIcon },
    { type: 'data.remote', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.linkExternalIcon },
    { type: 'data.folder', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.archiveIcon },
    { type: 'data.structure', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.beakerIcon },
    { type: 'data', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.graphIcon },
    { type: 'process.calculation', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.calculatorIcon },
    { type: 'process', icon: _consts__WEBPACK_IMPORTED_MODULE_6__.rocketIcon }
];
function getIcon(typeString) {
    let finalIcon = _consts__WEBPACK_IMPORTED_MODULE_6__.fileIcon;
    for (const { type, icon } of nodeIconMatches) {
        if (typeString.startsWith(type)) {
            finalIcon = icon;
            break;
        }
    }
    return finalIcon;
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
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
___CSS_LOADER_EXPORT___.push([module.id, "", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

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
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _aiida_icon_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./aiida-icon.svg */ "./style/aiida-icon.svg");
/* harmony import */ var _aiida_icon_svg__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_aiida_icon_svg__WEBPACK_IMPORTED_MODULE_4__);
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__.default);
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default()((_aiida_icon_svg__WEBPACK_IMPORTED_MODULE_4___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ":root {\n    --indent: 1em;\n    --aiidatree-icon-light: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n    --aiidatree-icon-dark: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n    --aiidatree-icon: var(--aiidatree-icon-dark);\n}\n\n[data-jp-theme-light=\"true\"] .aiidatree-icon {\n    --aiidatree-icon: var(--aiidatree-icon-light);\n}\n\n[data-jp-theme-light=\"false\"] .aiidatree-icon {\n    --aiidatree-icon: var(--aiidatree-icon-dark);\n}\n\n.aiidatree-icon {\n    background-image: var(--aiidatree-icon);\n    min-width: 20px;\n    min-height: 20px;\n    background-size: 20px;\n    display: inline-block;\n    vertical-align: middle;\n    background-repeat: no-repeat;\n    background-position: center;\n    margin: auto;\n}\n\n.jp-aiidatreeWidget {\n    background: var(--jp-layout-color1);\n    overflow: auto;\n    color: var(--jp-ui-font-color1);\n    /* This is needed so that all font sizing of children done in ems is\n     * relative to this base size */\n    font-size: var(--jp-ui-font-size1);\n}\n\n.filetree-toolbar {\n    padding: 0px;\n    border-bottom: none;\n    height: auto;\n    margin: var(--jp-toolbar-header-margin);\n    box-shadow: none;\n}\n\n.filetree-toolbar .jp-ToolbarButtonComponent {\n    padding: 0px 16px;\n}\n\n/* AiidaTreeWidget.buildHTMLTable */\n\n.aiidatree-head {\n    width: 100%;\n    border-spacing: 0px;\n    overflow: scroll;\n}\n\n.aiidatree-header {\n    /* Chrome all / Safari all */\n    -webkit-user-select: none;\n    /* Firefox all */\n    -moz-user-select: none;\n    /* IE 10+ */\n    -ms-user-select: none;\n    border: var(--jp-border-width) solid var(--jp-border-color2);\n    border-left: none;\n    font-size: var(--jp-ui-font-size0);\n    font-weight: 600;\n    letter-spacing: 1px;\n    margin: 0px;\n    padding: 8px 12px;\n    text-transform: uppercase;\n    overflow: hidden;\n    white-space: nowrap;\n    /* text-align: left; */\n}\n\n.aiidatree-header.modified {\n    border-right: none;\n}\n\n.aiidatree-first-column {\n    text-align: left;\n}\n\n.aiidatree-item {\n    -webkit-user-select: none;\n    /* Chrome all / Safari all */\n    -moz-user-select: none;\n    /* Firefox all */\n    -ms-user-select: none;\n    /* IE 10+ */\n    text-align: center;\n    padding-top: 2px;\n    overflow: hidden;\n    white-space: nowrap;\n}\n\n.aiidatree-item:hover {\n    cursor: pointer;\n    background-color: var(--jp-input-hover-background);\n}\n\n.aiidatree-item.selected {\n    color: white;\n    background: var(--jp-brand-color1);\n}\n\n.aiidatree-link-item .aiidatree-first-column {\n    padding-left: 12px;\n}\n\n.aiidatree-link-incoming {\n    color: var(--jp-content-font-color1);\n}\n\n.aiidatree-link-outgoing {\n    color: var(--jp-content-font-color2);\n}\n\n.aiidatree-yaml {\n    padding-left: 12px;\n    overflow: scroll;\n}\n\n.aiidatree-process-select {\n    float: right;\n}\n\n.aiidatree-threejs {\n    min-height: 400px;\n    width: 100%;\n}\n\n.d3-svg-container {\n    display: inline-block;\n    position: relative;\n    width: 100%;\n    padding-bottom: 100%;\n    /* aspect ratio */\n    vertical-align: top;\n    overflow: hidden;\n}\n\n.d3-svg-content-responsive {\n    display: inline-block;\n    position: absolute;\n    top: 10px;\n    left: 0;\n}\n\n.d3-svg-container .labels {\n    fill: var(--jp-content-font-color2);\n}\n", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAEA;IACI,aAAa;IACb,+DAA6C;IAC7C,8DAA4C;IAC5C,4CAA4C;AAChD;;AAEA;IACI,6CAA6C;AACjD;;AAEA;IACI,4CAA4C;AAChD;;AAEA;IACI,uCAAuC;IACvC,eAAe;IACf,gBAAgB;IAChB,qBAAqB;IACrB,qBAAqB;IACrB,sBAAsB;IACtB,4BAA4B;IAC5B,2BAA2B;IAC3B,YAAY;AAChB;;AAEA;IACI,mCAAmC;IACnC,cAAc;IACd,+BAA+B;IAC/B;mCAC+B;IAC/B,kCAAkC;AACtC;;AAEA;IACI,YAAY;IACZ,mBAAmB;IACnB,YAAY;IACZ,uCAAuC;IACvC,gBAAgB;AACpB;;AAEA;IACI,iBAAiB;AACrB;;AAEA,mCAAmC;;AAEnC;IACI,WAAW;IACX,mBAAmB;IACnB,gBAAgB;AACpB;;AAEA;IACI,4BAA4B;IAC5B,yBAAyB;IACzB,gBAAgB;IAChB,sBAAsB;IACtB,WAAW;IACX,qBAAqB;IACrB,4DAA4D;IAC5D,iBAAiB;IACjB,kCAAkC;IAClC,gBAAgB;IAChB,mBAAmB;IACnB,WAAW;IACX,iBAAiB;IACjB,yBAAyB;IACzB,gBAAgB;IAChB,mBAAmB;IACnB,sBAAsB;AAC1B;;AAEA;IACI,kBAAkB;AACtB;;AAEA;IACI,gBAAgB;AACpB;;AAEA;IACI,yBAAyB;IACzB,4BAA4B;IAC5B,sBAAsB;IACtB,gBAAgB;IAChB,qBAAqB;IACrB,WAAW;IACX,kBAAkB;IAClB,gBAAgB;IAChB,gBAAgB;IAChB,mBAAmB;AACvB;;AAEA;IACI,eAAe;IACf,kDAAkD;AACtD;;AAEA;IACI,YAAY;IACZ,kCAAkC;AACtC;;AAEA;IACI,kBAAkB;AACtB;;AAEA;IACI,oCAAoC;AACxC;;AAEA;IACI,oCAAoC;AACxC;;AAEA;IACI,kBAAkB;IAClB,gBAAgB;AACpB;;AAEA;IACI,YAAY;AAChB;;AAEA;IACI,iBAAiB;IACjB,WAAW;AACf;;AAEA;IACI,qBAAqB;IACrB,kBAAkB;IAClB,WAAW;IACX,oBAAoB;IACpB,iBAAiB;IACjB,mBAAmB;IACnB,gBAAgB;AACpB;;AAEA;IACI,qBAAqB;IACrB,kBAAkB;IAClB,SAAS;IACT,OAAO;AACX;;AAEA;IACI,mCAAmC;AACvC","sourcesContent":["@import url('base.css');\n\n:root {\n    --indent: 1em;\n    --aiidatree-icon-light: url('aiida-icon.svg');\n    --aiidatree-icon-dark: url('aiida-icon.svg');\n    --aiidatree-icon: var(--aiidatree-icon-dark);\n}\n\n[data-jp-theme-light=\"true\"] .aiidatree-icon {\n    --aiidatree-icon: var(--aiidatree-icon-light);\n}\n\n[data-jp-theme-light=\"false\"] .aiidatree-icon {\n    --aiidatree-icon: var(--aiidatree-icon-dark);\n}\n\n.aiidatree-icon {\n    background-image: var(--aiidatree-icon);\n    min-width: 20px;\n    min-height: 20px;\n    background-size: 20px;\n    display: inline-block;\n    vertical-align: middle;\n    background-repeat: no-repeat;\n    background-position: center;\n    margin: auto;\n}\n\n.jp-aiidatreeWidget {\n    background: var(--jp-layout-color1);\n    overflow: auto;\n    color: var(--jp-ui-font-color1);\n    /* This is needed so that all font sizing of children done in ems is\n     * relative to this base size */\n    font-size: var(--jp-ui-font-size1);\n}\n\n.filetree-toolbar {\n    padding: 0px;\n    border-bottom: none;\n    height: auto;\n    margin: var(--jp-toolbar-header-margin);\n    box-shadow: none;\n}\n\n.filetree-toolbar .jp-ToolbarButtonComponent {\n    padding: 0px 16px;\n}\n\n/* AiidaTreeWidget.buildHTMLTable */\n\n.aiidatree-head {\n    width: 100%;\n    border-spacing: 0px;\n    overflow: scroll;\n}\n\n.aiidatree-header {\n    /* Chrome all / Safari all */\n    -webkit-user-select: none;\n    /* Firefox all */\n    -moz-user-select: none;\n    /* IE 10+ */\n    -ms-user-select: none;\n    border: var(--jp-border-width) solid var(--jp-border-color2);\n    border-left: none;\n    font-size: var(--jp-ui-font-size0);\n    font-weight: 600;\n    letter-spacing: 1px;\n    margin: 0px;\n    padding: 8px 12px;\n    text-transform: uppercase;\n    overflow: hidden;\n    white-space: nowrap;\n    /* text-align: left; */\n}\n\n.aiidatree-header.modified {\n    border-right: none;\n}\n\n.aiidatree-first-column {\n    text-align: left;\n}\n\n.aiidatree-item {\n    -webkit-user-select: none;\n    /* Chrome all / Safari all */\n    -moz-user-select: none;\n    /* Firefox all */\n    -ms-user-select: none;\n    /* IE 10+ */\n    text-align: center;\n    padding-top: 2px;\n    overflow: hidden;\n    white-space: nowrap;\n}\n\n.aiidatree-item:hover {\n    cursor: pointer;\n    background-color: var(--jp-input-hover-background);\n}\n\n.aiidatree-item.selected {\n    color: white;\n    background: var(--jp-brand-color1);\n}\n\n.aiidatree-link-item .aiidatree-first-column {\n    padding-left: 12px;\n}\n\n.aiidatree-link-incoming {\n    color: var(--jp-content-font-color1);\n}\n\n.aiidatree-link-outgoing {\n    color: var(--jp-content-font-color2);\n}\n\n.aiidatree-yaml {\n    padding-left: 12px;\n    overflow: scroll;\n}\n\n.aiidatree-process-select {\n    float: right;\n}\n\n.aiidatree-threejs {\n    min-height: 400px;\n    width: 100%;\n}\n\n.d3-svg-container {\n    display: inline-block;\n    position: relative;\n    width: 100%;\n    padding-bottom: 100%;\n    /* aspect ratio */\n    vertical-align: top;\n    overflow: hidden;\n}\n\n.d3-svg-content-responsive {\n    display: inline-block;\n    position: absolute;\n    top: 10px;\n    left: 0;\n}\n\n.d3-svg-container .labels {\n    fill: var(--jp-content-font-color2);\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/icons/light/archive.svg":
/*!***************************************!*\
  !*** ./style/icons/light/archive.svg ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M1.75 2.5a.25.25 0 00-.25.25v1.5c0 .138.112.25.25.25h12.5a.25.25 0 00.25-.25v-1.5a.25.25 0 00-.25-.25H1.75zM0 2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75v1.5A1.75 1.75 0 0114.25 6H1.75A1.75 1.75 0 010 4.25v-1.5zM1.75 7a.75.75 0 01.75.75v5.5c0 .138.112.25.25.25h10.5a.25.25 0 00.25-.25v-5.5a.75.75 0 111.5 0v5.5A1.75 1.75 0 0113.25 15H2.75A1.75 1.75 0 011 13.25v-5.5A.75.75 0 011.75 7zm4.5 1a.75.75 0 000 1.5h3.5a.75.75 0 100-1.5h-3.5z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/beaker.svg":
/*!**************************************!*\
  !*** ./style/icons/light/beaker.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M5 5.782V2.5h-.25a.75.75 0 010-1.5h6.5a.75.75 0 010 1.5H11v3.282l3.666 5.76C15.619 13.04 14.543 15 12.767 15H3.233c-1.776 0-2.852-1.96-1.899-3.458L5 5.782zM9.5 2.5h-3V6a.75.75 0 01-.117.403L4.73 9h6.54L9.617 6.403A.75.75 0 019.5 6V2.5zm-6.9 9.847L3.775 10.5h8.45l1.175 1.847a.75.75 0 01-.633 1.153H3.233a.75.75 0 01-.633-1.153z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/calculator.svg":
/*!******************************************!*\
  !*** ./style/icons/light/calculator.svg ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>\n<!--Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)-->\n<svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" viewBox=\"0 0 60 60\" style=\"enable-background:new 0 0 60 60\" xml:space=\"preserve\">\n    <path fill=\"#424242\" d=\"M50.586,0H9.414C7.807,0,6.5,1.308,6.5,2.914v54.172C6.5,58.692,7.807,60,9.414,60h41.172c1.607,0,2.914-1.308,2.914-2.914\n\tV2.914C53.5,1.308,52.193,0,50.586,0z M22.5,55h-11V44h11V55z M22.5,42h-11V31h11V42z M22.5,29h-11V18h11V29z M35.5,55h-11V44h11V55\n\tz M35.5,42h-11V31h11V42z M35.5,29h-11V18h11V29z M48.5,55h-11V31h11V55z M48.5,29h-11V18h11V29z M48.5,15h-37V5h37V15z\"/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n    <g/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/check-circle.svg":
/*!********************************************!*\
  !*** ./style/icons/light/check-circle.svg ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM0 8a8 8 0 1116 0A8 8 0 010 8zm11.78-1.72a.75.75 0 00-1.06-1.06L6.75 9.19 5.28 7.72a.75.75 0 00-1.06 1.06l2 2a.75.75 0 001.06 0l4.5-4.5z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/cog.svg":
/*!***********************************!*\
  !*** ./style/icons/light/cog.svg ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<mask id=\"path-1-inside-1\" fill=\"white\">\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M9.41155 1L9.89605 3.42252L11.9516 2.05214L13.9479 4.04837L12.5775 6.10396L15 6.58846V9.41156L12.5775 9.89606L13.9479 11.9516L11.9516 13.9479L9.89606 12.5775L9.41155 15H6.58845L6.10395 12.5775L4.04838 13.9479L2.05214 11.9516L3.42253 9.89606L1 9.41156V6.58846L3.42252 6.10396L2.05214 4.04839L4.04837 2.05215L6.10395 3.42254L6.58845 1.00002L9.41155 1ZM11.6369 6.94069L11.3207 6.17737L12.6547 4.17642L11.8236 3.3453L9.82263 4.67927L9.05931 4.36311L8.58769 2.00496L7.41231 2.00497L6.94069 4.36313L6.17737 4.67928L4.17642 3.34532L3.34531 4.17643L4.67928 6.17739L4.36309 6.94069L2.00495 7.41232V8.5877L4.36309 9.05932L4.67929 9.82263L3.34531 11.8236L4.17643 12.6547L6.17738 11.3207L6.94068 11.6369L7.41231 13.9951H8.58769L9.05931 11.6369L9.82263 11.3207L11.8236 12.6547L12.6547 11.8236L11.3207 9.82262L11.6369 9.05932L13.995 8.5877V7.41232L11.6369 6.94069ZM9 8C9 8.55228 8.55228 9 8 9C7.44772 9 7 8.55228 7 8C7 7.44772 7.44772 7 8 7C8.55228 7 9 7.44772 9 8ZM10 8C10 9.10457 9.10457 10 8 10C6.89543 10 6 9.10457 6 8C6 6.89543 6.89543 6 8 6C9.10457 6 10 6.89543 10 8Z\"/>\n</mask>\n<path d=\"M9.89605 3.42252L8.91547 3.61864L9.20831 5.08286L10.4507 4.25457L9.89605 3.42252ZM9.41155 1L10.3921 0.803887L10.2314 -6.19888e-06L9.41154 0L9.41155 1ZM11.9516 2.05214L12.6587 1.34503L12.079 0.765344L11.3969 1.22009L11.9516 2.05214ZM13.9479 4.04837L14.7799 4.60307L15.2347 3.92095L14.655 3.34126L13.9479 4.04837ZM12.5775 6.10396L11.7454 5.54925L10.9171 6.79169L12.3814 7.08454L12.5775 6.10396ZM15 6.58846H16V5.76866L15.1961 5.60788L15 6.58846ZM15 9.41156L15.1961 10.3921L16 10.2314V9.41156H15ZM12.5775 9.89606L12.3814 8.91548L10.9172 9.20832L11.7454 10.4508L12.5775 9.89606ZM13.9479 11.9516L14.655 12.6587L15.2347 12.079L14.7799 11.3969L13.9479 11.9516ZM11.9516 13.9479L11.3969 14.7799L12.0791 15.2346L12.6587 14.655L11.9516 13.9479ZM9.89606 12.5775L10.4508 11.7454L9.20832 10.9171L8.91548 12.3814L9.89606 12.5775ZM9.41155 15V16H10.2314L10.3921 15.1961L9.41155 15ZM6.58845 15L5.60787 15.1961L5.76865 16H6.58845V15ZM6.10395 12.5775L7.08453 12.3814L6.79168 10.9172L5.54925 11.7454L6.10395 12.5775ZM4.04838 13.9479L3.34127 14.655L3.92096 15.2347L4.60308 14.7799L4.04838 13.9479ZM2.05214 11.9516L1.22009 11.3969L0.765349 12.0791L1.34504 12.6587L2.05214 11.9516ZM3.42253 9.89606L4.25458 10.4508L5.08287 9.20833L3.61865 8.91548L3.42253 9.89606ZM1 9.41156H0V10.2314L0.803884 10.3921L1 9.41156ZM1 6.58846L0.803884 5.60788L0 5.76866V6.58846H1ZM3.42252 6.10396L3.61864 7.08454L5.08286 6.79169L4.25457 5.54926L3.42252 6.10396ZM2.05214 4.04839L1.34503 3.34128L0.765344 3.92097L1.22009 4.60309L2.05214 4.04839ZM4.04837 2.05215L4.60307 1.2201L3.92096 0.765359L3.34127 1.34505L4.04837 2.05215ZM6.10395 3.42254L5.54925 4.25459L6.79169 5.08288L7.08453 3.61865L6.10395 3.42254ZM6.58845 1.00002L6.58844 2.14577e-05L5.76864 2.77162e-05L5.60787 0.803908L6.58845 1.00002ZM11.3207 6.17737L10.4887 5.62267L10.1926 6.06685L10.3968 6.56005L11.3207 6.17737ZM11.6369 6.94069L10.713 7.32337L10.9173 7.81658L11.4408 7.92127L11.6369 6.94069ZM12.6547 4.17642L13.4867 4.73112L13.9415 4.049L13.3618 3.46931L12.6547 4.17642ZM11.8236 3.3453L12.5307 2.6382L11.951 2.05851L11.2689 2.51325L11.8236 3.3453ZM9.82263 4.67927L9.43997 5.60316L9.93316 5.80743L10.3773 5.51132L9.82263 4.67927ZM9.05931 4.36311L8.07873 4.55923L8.18343 5.08272L8.67665 5.287L9.05931 4.36311ZM8.58769 2.00496L9.56827 1.80884L9.40749 1.00495L8.58768 1.00496L8.58769 2.00496ZM7.41231 2.00497L7.41231 1.00497L6.59251 1.00497L6.43173 1.80885L7.41231 2.00497ZM6.94069 4.36313L7.32335 5.28702L7.81658 5.08273L7.92127 4.55924L6.94069 4.36313ZM6.17737 4.67928L5.62267 5.51133L6.06684 5.80745L6.56003 5.60317L6.17737 4.67928ZM4.17642 3.34532L4.73112 2.51327L4.049 2.05852L3.46932 2.63821L4.17642 3.34532ZM3.34531 4.17643L2.6382 3.46933L2.05851 4.04902L2.51326 4.73113L3.34531 4.17643ZM4.67928 6.17739L5.60315 6.56009L5.80746 6.06688L5.51133 5.62269L4.67928 6.17739ZM4.36309 6.94069L4.55921 7.92128L5.08267 7.81658L5.28697 7.32339L4.36309 6.94069ZM2.00495 7.41232L1.80884 6.43174L1.00495 6.59252V7.41232H2.00495ZM2.00495 8.5877H1.00495V9.4075L1.80884 9.56828L2.00495 8.5877ZM4.36309 9.05932L5.28696 8.67662L5.08266 8.18343L4.55921 8.07874L4.36309 9.05932ZM4.67929 9.82263L5.51134 10.3773L5.80747 9.93314L5.60316 9.43993L4.67929 9.82263ZM3.34531 11.8236L2.51326 11.2689L2.05852 11.951L2.63821 12.5307L3.34531 11.8236ZM4.17643 12.6547L3.46932 13.3618L4.04901 13.9415L4.73113 13.4868L4.17643 12.6547ZM6.17738 11.3207L6.56007 10.3969L6.06686 10.1926L5.62268 10.4887L6.17738 11.3207ZM6.94068 11.6369L7.92126 11.4408L7.81657 10.9173L7.32337 10.713L6.94068 11.6369ZM7.41231 13.9951L6.43173 14.1912L6.59251 14.9951H7.41231V13.9951ZM8.58769 13.9951V14.9951H9.40749L9.56827 14.1912L8.58769 13.9951ZM9.05931 11.6369L8.67661 10.713L8.18342 10.9173L8.07873 11.4408L9.05931 11.6369ZM9.82263 11.3207L10.3773 10.4887L9.93313 10.1925L9.43992 10.3968L9.82263 11.3207ZM11.8236 12.6547L11.2689 13.4867L11.951 13.9415L12.5307 13.3618L11.8236 12.6547ZM12.6547 11.8236L13.3618 12.5307L13.9415 11.951L13.4868 11.2689L12.6547 11.8236ZM11.3207 9.82262L10.3969 9.43994L10.1926 9.93315L10.4887 10.3773L11.3207 9.82262ZM11.6369 9.05932L11.4408 8.07874L10.9173 8.18344L10.713 8.67664L11.6369 9.05932ZM13.995 8.5877L14.1912 9.56828L14.995 9.4075V8.5877H13.995ZM13.995 7.41232H14.995V6.59252L14.1912 6.43174L13.995 7.41232ZM10.8766 3.22641L10.3921 0.803887L8.43097 1.19611L8.91547 3.61864L10.8766 3.22641ZM11.3969 1.22009L9.34135 2.59047L10.4507 4.25457L12.5063 2.88419L11.3969 1.22009ZM14.655 3.34126L12.6587 1.34503L11.2445 2.75925L13.2408 4.75548L14.655 3.34126ZM13.4095 6.65866L14.7799 4.60307L13.1158 3.49367L11.7454 5.54925L13.4095 6.65866ZM15.1961 5.60788L12.7736 5.12337L12.3814 7.08454L14.8039 7.56904L15.1961 5.60788ZM16 9.41156V6.58846H14V9.41156H16ZM12.7736 10.8766L15.1961 10.3921L14.8039 8.43098L12.3814 8.91548L12.7736 10.8766ZM14.7799 11.3969L13.4095 9.34136L11.7454 10.4508L13.1158 12.5063L14.7799 11.3969ZM12.6587 14.655L14.655 12.6587L13.2408 11.2445L11.2445 13.2407L12.6587 14.655ZM9.34136 13.4095L11.3969 14.7799L12.5063 13.1158L10.4508 11.7454L9.34136 13.4095ZM10.3921 15.1961L10.8766 12.7736L8.91548 12.3814L8.43097 14.8039L10.3921 15.1961ZM6.58845 16H9.41155V14H6.58845V16ZM5.12337 12.7736L5.60787 15.1961L7.56903 14.8039L7.08453 12.3814L5.12337 12.7736ZM4.60308 14.7799L6.65865 13.4095L5.54925 11.7454L3.49368 13.1158L4.60308 14.7799ZM1.34504 12.6587L3.34127 14.655L4.75549 13.2408L2.75925 11.2445L1.34504 12.6587ZM2.59048 9.34136L1.22009 11.3969L2.88419 12.5063L4.25458 10.4508L2.59048 9.34136ZM0.803884 10.3921L3.22641 10.8766L3.61865 8.91548L1.19612 8.43098L0.803884 10.3921ZM0 6.58846V9.41156H2V6.58846H0ZM3.22641 5.12338L0.803884 5.60788L1.19612 7.56904L3.61864 7.08454L3.22641 5.12338ZM1.22009 4.60309L2.59047 6.65866L4.25457 5.54926L2.88419 3.49368L1.22009 4.60309ZM3.34127 1.34505L1.34503 3.34128L2.75925 4.75549L4.75548 2.75926L3.34127 1.34505ZM6.65865 2.59049L4.60307 1.2201L3.49367 2.8842L5.54925 4.25459L6.65865 2.59049ZM5.60787 0.803908L5.12337 3.22642L7.08453 3.61865L7.56903 1.19613L5.60787 0.803908ZM9.41154 0L6.58844 2.14577e-05L6.58846 2.00002L9.41156 2L9.41154 0ZM10.3968 6.56005L10.713 7.32337L12.5608 6.55801L12.2446 5.79469L10.3968 6.56005ZM11.8226 3.62172L10.4887 5.62267L12.1528 6.73207L13.4867 4.73112L11.8226 3.62172ZM11.1165 4.05241L11.9476 4.88353L13.3618 3.46931L12.5307 2.6382L11.1165 4.05241ZM10.3773 5.51132L12.3783 4.17735L11.2689 2.51325L9.26793 3.84722L10.3773 5.51132ZM8.67665 5.287L9.43997 5.60316L10.2053 3.75538L9.44197 3.43922L8.67665 5.287ZM7.60711 2.20107L8.07873 4.55923L10.0399 4.167L9.56827 1.80884L7.60711 2.20107ZM7.41232 3.00497L8.5877 3.00496L8.58768 1.00496L7.41231 1.00497L7.41232 3.00497ZM7.92127 4.55924L8.3929 2.20108L6.43173 1.80885L5.96011 4.16702L7.92127 4.55924ZM6.56003 5.60317L7.32335 5.28702L6.55803 3.43924L5.79471 3.75539L6.56003 5.60317ZM3.62172 4.17737L5.62267 5.51133L6.73207 3.84723L4.73112 2.51327L3.62172 4.17737ZM4.05241 4.88354L4.88353 4.05243L3.46932 2.63821L2.6382 3.46933L4.05241 4.88354ZM5.51133 5.62269L4.17736 3.62173L2.51326 4.73113L3.84723 6.73209L5.51133 5.62269ZM5.28697 7.32339L5.60315 6.56009L3.75541 5.79469L3.43922 6.558L5.28697 7.32339ZM2.20107 8.3929L4.55921 7.92128L4.16698 5.96011L1.80884 6.43174L2.20107 8.3929ZM3.00495 8.5877V7.41232H1.00495V8.5877H3.00495ZM4.55921 8.07874L2.20107 7.60712L1.80884 9.56828L4.16698 10.0399L4.55921 8.07874ZM5.60316 9.43993L5.28696 8.67662L3.43922 9.44203L3.75542 10.2053L5.60316 9.43993ZM4.17736 12.3783L5.51134 10.3773L3.84724 9.26793L2.51326 11.2689L4.17736 12.3783ZM4.88353 11.9476L4.05242 11.1165L2.63821 12.5307L3.46932 13.3618L4.88353 11.9476ZM5.62268 10.4887L3.62173 11.8227L4.73113 13.4868L6.73208 12.1528L5.62268 10.4887ZM7.32337 10.713L6.56007 10.3969L5.7947 12.2446L6.558 12.5608L7.32337 10.713ZM8.39289 13.7989L7.92126 11.4408L5.9601 11.833L6.43173 14.1912L8.39289 13.7989ZM8.58769 12.9951H7.41231V14.9951H8.58769V12.9951ZM8.07873 11.4408L7.60711 13.7989L9.56827 14.1912L10.0399 11.833L8.07873 11.4408ZM9.43992 10.3968L8.67661 10.713L9.44202 12.5608L10.2053 12.2446L9.43992 10.3968ZM12.3783 11.8226L10.3773 10.4887L9.26793 12.1528L11.2689 13.4867L12.3783 11.8226ZM11.9476 11.1165L11.1165 11.9476L12.5307 13.3618L13.3618 12.5307L11.9476 11.1165ZM10.4887 10.3773L11.8227 12.3783L13.4868 11.2689L12.1528 9.26792L10.4887 10.3773ZM10.713 8.67664L10.3969 9.43994L12.2446 10.2053L12.5608 9.442L10.713 8.67664ZM13.7989 7.60712L11.4408 8.07874L11.833 10.0399L14.1912 9.56828L13.7989 7.60712ZM12.995 7.41232V8.5877H14.995V7.41232H12.995ZM11.4408 7.92127L13.7989 8.3929L14.1912 6.43174L11.833 5.96011L11.4408 7.92127ZM8 10C9.10457 10 10 9.10457 10 8H8V10ZM6 8C6 9.10457 6.89543 10 8 10V8H6ZM8 6C6.89543 6 6 6.89543 6 8H8V6ZM10 8C10 6.89543 9.10457 6 8 6V8H10ZM8 11C9.65685 11 11 9.65685 11 8H9C9 8.55228 8.55228 9 8 9V11ZM5 8C5 9.65685 6.34315 11 8 11V9C7.44772 9 7 8.55228 7 8H5ZM8 5C6.34315 5 5 6.34315 5 8H7C7 7.44772 7.44772 7 8 7V5ZM11 8C11 6.34315 9.65685 5 8 5V7C8.55228 7 9 7.44772 9 8H11Z\" fill=\"#424242\" mask=\"url(#path-1-inside-1)\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/computer.svg":
/*!****************************************!*\
  !*** ./style/icons/light/computer.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M15 2H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h5.34c-.25.61-.86 1.39-2.34 2h8c-1.48-.61-2.09-1.39-2.34-2H15c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1zm0 9H1V3h14v8z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/connect.svg":
/*!***************************************!*\
  !*** ./style/icons/light/connect.svg ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M10.625 3.625V6.6875C10.625 7.06576 10.5589 7.42806 10.4268 7.77441C10.2946 8.11621 10.11 8.42155 9.87305 8.69043C9.64062 8.95931 9.36263 9.1849 9.03906 9.36719C8.72005 9.54492 8.3737 9.66113 8 9.71582V15H7.125V9.71582C6.74674 9.66113 6.39811 9.54492 6.0791 9.36719C5.76009 9.1849 5.4821 8.95931 5.24512 8.69043C5.0127 8.42155 4.8304 8.11621 4.69824 7.77441C4.56608 7.42806 4.5 7.06576 4.5 6.6875V3.625H5.375V1H6.25V3.625H8.875V1H9.75V3.625H10.625ZM9.75 4.5H5.375V6.6875C5.375 6.98828 5.43197 7.27311 5.5459 7.54199C5.65983 7.80632 5.81478 8.03874 6.01074 8.23926C6.21126 8.43522 6.44368 8.59017 6.70801 8.7041C6.97689 8.81803 7.26172 8.875 7.5625 8.875C7.86328 8.875 8.14583 8.81803 8.41016 8.7041C8.67448 8.59017 8.90462 8.43522 9.10059 8.23926C9.30111 8.03874 9.45833 7.80632 9.57227 7.54199C9.69076 7.27311 9.75 6.98828 9.75 6.6875V4.5Z\" fill=\"#424242\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/database.svg":
/*!****************************************!*\
  !*** ./style/icons/light/database.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M2.5 3.5c0-.133.058-.318.282-.55.227-.237.592-.484 1.1-.708C4.899 1.795 6.354 1.5 8 1.5c1.647 0 3.102.295 4.117.742.51.224.874.47 1.101.707.224.233.282.418.282.551 0 .133-.058.318-.282.55-.227.237-.592.484-1.1.708C11.101 5.205 9.646 5.5 8 5.5c-1.647 0-3.102-.295-4.117-.742-.51-.224-.874-.47-1.101-.707-.224-.233-.282-.418-.282-.551zM1 3.5c0-.626.292-1.165.7-1.59.406-.422.956-.767 1.579-1.041C4.525.32 6.195 0 8 0c1.805 0 3.475.32 4.722.869.622.274 1.172.62 1.578 1.04.408.426.7.965.7 1.591v9c0 .626-.292 1.165-.7 1.59-.406.422-.956.767-1.579 1.041C11.476 15.68 9.806 16 8 16c-1.805 0-3.475-.32-4.721-.869-.623-.274-1.173-.62-1.579-1.04-.408-.426-.7-.965-.7-1.591v-9zM2.5 8V5.724c.241.15.503.286.779.407C4.525 6.68 6.195 7 8 7c1.805 0 3.475-.32 4.722-.869.275-.121.537-.257.778-.407V8c0 .133-.058.318-.282.55-.227.237-.592.484-1.1.708C11.101 9.705 9.646 10 8 10c-1.647 0-3.102-.295-4.117-.742-.51-.224-.874-.47-1.101-.707C2.558 8.318 2.5 8.133 2.5 8zm0 2.225V12.5c0 .133.058.318.282.55.227.237.592.484 1.1.708 1.016.447 2.471.742 4.118.742 1.647 0 3.102-.295 4.117-.742.51-.224.874-.47 1.101-.707.224-.233.282-.418.282-.551v-2.275c-.241.15-.503.285-.778.406-1.247.549-2.917.869-4.722.869-1.805 0-3.475-.32-4.721-.869a6.236 6.236 0 01-.779-.406z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/file.svg":
/*!************************************!*\
  !*** ./style/icons/light/file.svg ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 12 16\" width=\"12\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M6 5H2V4h4v1zM2 8h7V7H2v1zm0 2h7V9H2v1zm0 2h7v-1H2v1zm10-7.5V14c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1h7.5L12 4.5zM11 5L8 2H1v12h10V5z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/filter.svg":
/*!**************************************!*\
  !*** ./style/icons/light/filter.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\"><style>.icon-canvas-transparent{opacity:0;fill:#f6f6f6}.icon-vs-out{fill:#f6f6f6}.icon-vs-bg{fill:#424242}.icon-vs-fg{fill:#f0eff1}</style><path class=\"icon-canvas-transparent\" d=\"M16 16H0V0h16v16z\" id=\"canvas\"/><path class=\"icon-vs-out\" d=\"M0 0v3.043l5 6V16h6V9.043l5-6V0H0z\" id=\"outline\" style=\"display: none;\"/><path class=\"icon-vs-fg\" d=\"M7 14h2V8.319l5-6V2H2v.319l5 6V14z\" id=\"iconFg\" style=\"display: none;\"/><path class=\"icon-vs-bg\" d=\"M10 15H6V8.681l-5-6V1h14v1.681l-5 6V15zm-3-1h2V8.319l5-6V2H2v.319l5 6V14z\" id=\"iconBg\"/></svg>\n");

/***/ }),

/***/ "./style/icons/light/folder.svg":
/*!**************************************!*\
  !*** ./style/icons/light/folder.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 14 16\" width=\"14\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M13 4H7V3c0-.66-.31-1-1-1H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1zM6 4H1V3h5v1z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/graph.svg":
/*!*************************************!*\
  !*** ./style/icons/light/graph.svg ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M1.5 1.75a.75.75 0 00-1.5 0v12.5c0 .414.336.75.75.75h14.5a.75.75 0 000-1.5H1.5V1.75zm14.28 2.53a.75.75 0 00-1.06-1.06L10 7.94 7.53 5.47a.75.75 0 00-1.06 0L3.22 8.72a.75.75 0 001.06 1.06L7 7.06l2.47 2.47a.75.75 0 001.06 0l5.25-5.25z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/home.svg":
/*!************************************!*\
  !*** ./style/icons/light/home.svg ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M8.156 1.835a.25.25 0 00-.312 0l-5.25 4.2a.25.25 0 00-.094.196v7.019c0 .138.112.25.25.25H5.5V8.25a.75.75 0 01.75-.75h3.5a.75.75 0 01.75.75v5.25h2.75a.25.25 0 00.25-.25V6.23a.25.25 0 00-.094-.195l-5.25-4.2zM6.906.664a1.75 1.75 0 012.187 0l5.25 4.2c.415.332.657.835.657 1.367v7.019A1.75 1.75 0 0113.25 15h-3.5a.75.75 0 01-.75-.75V9H7v5.25a.75.75 0 01-.75.75h-3.5A1.75 1.75 0 011 13.25V6.23c0-.531.242-1.034.657-1.366l5.25-4.2h-.001z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/key.svg":
/*!***********************************!*\
  !*** ./style/icons/light/key.svg ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 14 16\" width=\"14\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M12.83 2.17C12.08 1.42 11.14 1.03 10 1c-1.13.03-2.08.42-2.83 1.17S6.04 3.86 6.01 5c0 .3.03.59.09.89L0 12v1l1 1h2l1-1v-1h1v-1h1v-1h2l1.09-1.11c.3.08.59.11.91.11 1.14-.03 2.08-.42 2.83-1.17S13.97 6.14 14 5c-.03-1.14-.42-2.08-1.17-2.83zM11 5.38c-.77 0-1.38-.61-1.38-1.38 0-.77.61-1.38 1.38-1.38.77 0 1.38.61 1.38 1.38 0 .77-.61 1.38-1.38 1.38z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/link-external.svg":
/*!*********************************************!*\
  !*** ./style/icons/light/link-external.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M10.604 1h4.146a.25.25 0 01.25.25v4.146a.25.25 0 01-.427.177L13.03 4.03 9.28 7.78a.75.75 0 01-1.06-1.06l3.75-3.75-1.543-1.543A.25.25 0 0110.604 1zM3.75 2A1.75 1.75 0 002 3.75v8.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 12.25v-3.5a.75.75 0 00-1.5 0v3.5a.25.25 0 01-.25.25h-8.5a.25.25 0 01-.25-.25v-8.5a.25.25 0 01.25-.25h3.5a.75.75 0 000-1.5h-3.5z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/list-unordered.svg":
/*!**********************************************!*\
  !*** ./style/icons/light/list-unordered.svg ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 12 16\" width=\"12\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M2 13c0 .59 0 1-.59 1H.59C0 14 0 13.59 0 13c0-.59 0-1 .59-1h.81c.59 0 .59.41.59 1H2zm2.59-9h6.81c.59 0 .59-.41.59-1 0-.59 0-1-.59-1H4.59C4 2 4 2.41 4 3c0 .59 0 1 .59 1zM1.41 7H.59C0 7 0 7.41 0 8c0 .59 0 1 .59 1h.81c.59 0 .59-.41.59-1 0-.59 0-1-.59-1h.01zm0-5H.59C0 2 0 2.41 0 3c0 .59 0 1 .59 1h.81c.59 0 .59-.41.59-1 0-.59 0-1-.59-1h.01zm10 5H4.59C4 7 4 7.41 4 8c0 .59 0 1 .59 1h6.81c.59 0 .59-.41.59-1 0-.59 0-1-.59-1h.01zm0 5H4.59C4 12 4 12.41 4 13c0 .59 0 1 .59 1h6.81c.59 0 .59-.41.59-1 0-.59 0-1-.59-1h.01z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/package-dependencies.svg":
/*!****************************************************!*\
  !*** ./style/icons/light/package-dependencies.svg ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M6.122.392a1.75 1.75 0 011.756 0l5.25 3.045c.54.313.872.89.872 1.514V7.25a.75.75 0 01-1.5 0V5.677L7.75 8.432v6.384a1 1 0 01-1.502.865L.872 12.563A1.75 1.75 0 010 11.049V4.951c0-.624.332-1.2.872-1.514L6.122.392zM7.125 1.69l4.63 2.685L7 7.133 2.245 4.375l4.63-2.685a.25.25 0 01.25 0zM1.5 11.049V5.677l4.75 2.755v5.516l-4.625-2.683a.25.25 0 01-.125-.216zm11.672-.282a.75.75 0 10-1.087-1.034l-2.378 2.5a.75.75 0 000 1.034l2.378 2.5a.75.75 0 101.087-1.034L11.999 13.5h3.251a.75.75 0 000-1.5h-3.251l1.173-1.233z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/package-dependents.svg":
/*!**************************************************!*\
  !*** ./style/icons/light/package-dependents.svg ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M6.122.392a1.75 1.75 0 011.756 0l5.25 3.045c.54.313.872.89.872 1.514V7.25a.75.75 0 01-1.5 0V5.677L7.75 8.432v6.384a1 1 0 01-1.502.865L.872 12.563A1.75 1.75 0 010 11.049V4.951c0-.624.332-1.2.872-1.514L6.122.392zM7.125 1.69l4.63 2.685L7 7.133 2.245 4.375l4.63-2.685a.25.25 0 01.25 0zM1.5 11.049V5.677l4.75 2.755v5.516l-4.625-2.683a.25.25 0 01-.125-.216zm10.828 3.684a.75.75 0 101.087 1.034l2.378-2.5a.75.75 0 000-1.034l-2.378-2.5a.75.75 0 00-1.087 1.034L13.501 12H10.25a.75.75 0 000 1.5h3.251l-1.173 1.233z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/refresh.svg":
/*!***************************************!*\
  !*** ./style/icons/light/refresh.svg ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M5.56253 2.51577C3.46348 3.4501 2 5.55414 2 7.99999C2 11.3137 4.68629 14 8 14C11.3137 14 14 11.3137 14 7.99999C14 5.32519 12.2497 3.05919 9.83199 2.28482L9.52968 3.23832C11.5429 3.88454 13 5.7721 13 7.99999C13 10.7614 10.7614 13 8 13C5.23858 13 3 10.7614 3 7.99999C3 6.31104 3.83742 4.81767 5.11969 3.91245L5.56253 2.51577Z\" fill=\"#424242\"/>\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M5 3H2V2H5.5L6 2.5V6H5V3Z\" fill=\"#424242\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/repo.svg":
/*!************************************!*\
  !*** ./style/icons/light/repo.svg ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/rocket.svg":
/*!**************************************!*\
  !*** ./style/icons/light/rocket.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M12.17 3.83c-.27-.27-.47-.55-.63-.88-.16-.31-.27-.66-.34-1.02-.58.33-1.16.7-1.73 1.13-.58.44-1.14.94-1.69 1.48-.7.7-1.33 1.81-1.78 2.45H3L0 10h3l2-2c-.34.77-1.02 2.98-1 3l1 1c.02.02 2.23-.64 3-1l-2 2v3l3-3v-3c.64-.45 1.75-1.09 2.45-1.78.55-.55 1.05-1.13 1.47-1.7.44-.58.81-1.16 1.14-1.72-.36-.08-.7-.19-1.03-.34a3.39 3.39 0 01-.86-.63zM16 0s-.09.38-.3 1.06c-.2.7-.55 1.58-1.06 2.66-.7-.08-1.27-.33-1.66-.72-.39-.39-.63-.94-.7-1.64C13.36.84 14.23.48 14.92.28 15.62.08 16 0 16 0z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/settings.svg":
/*!****************************************!*\
  !*** ./style/icons/light/settings.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M4 7H3V2h1v5zm-1 7h1v-3H3v3zm5 0h1V8H8v6zm5 0h1v-2h-1v2zm1-12h-1v6h1V2zM9 2H8v2h1V2zM5 8H2c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1zm5-3H7c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1zm5 4h-3c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusCreated.svg":
/*!*********************************************!*\
  !*** ./style/icons/light/statusCreated.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M13.25 2.5H2.75a.25.25 0 00-.25.25v10.5c0 .138.112.25.25.25h10.5a.25.25 0 00.25-.25V2.75a.25.25 0 00-.25-.25zM2.75 1h10.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0113.25 15H2.75A1.75 1.75 0 011 13.25V2.75C1 1.784 1.784 1 2.75 1zM8 4a.75.75 0 01.75.75v2.5h2.5a.75.75 0 010 1.5h-2.5v2.5a.75.75 0 01-1.5 0v-2.5h-2.5a.75.75 0 010-1.5h2.5v-2.5A.75.75 0 018 4z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusExcepted.svg":
/*!**********************************************!*\
  !*** ./style/icons/light/statusExcepted.svg ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M8.45337 2.02828C9.80698 2.16246 11.0755 2.76898 12.042 3.74809C13.15 4.87311 13.776 6.4012 13.7782 7.99826C13.7786 9.39013 13.3035 10.7372 12.4367 11.8101C11.5701 12.8828 10.3662 13.6147 9.03197 13.8847C7.69789 14.1547 6.31229 13.9472 5.1104 13.296C3.90817 12.6446 2.96232 11.5884 2.4374 10.3044C1.91238 9.02005 1.84212 7.58981 2.23908 6.25829C2.63599 4.92697 3.47438 3.77978 4.60779 3.00985C5.74086 2.24014 7.09976 1.8941 8.45337 2.02828ZM8.55201 1.03316C10.1398 1.19055 11.6248 1.90184 12.7539 3.04585C14.0479 4.35938 14.7758 6.14013 14.7782 7.99764C14.7787 9.61695 14.2261 11.1864 13.2145 12.4385C12.2029 13.6907 10.7949 14.5482 9.23035 14.8648C7.66577 15.1815 6.04142 14.9378 4.63401 14.1752C3.2266 13.4127 2.12319 12.1784 1.51176 10.6828C0.900328 9.18708 0.818694 7.52251 1.28076 5.97259C1.74283 4.42268 2.72002 3.08331 4.04587 2.18265C5.37171 1.28199 6.96419 0.875761 8.55201 1.03316ZM5.44326 5L7.88173 7.47506L10.3202 5L11.0169 5.70711L8.57839 8.18217L11.0165 10.6569L10.3198 11.364L7.88173 8.88927L5.44362 11.364L4.74697 10.6569L7.18508 8.18217L4.7466 5.70711L5.44326 5Z\" fill=\"#A1260D\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusFailed.svg":
/*!********************************************!*\
  !*** ./style/icons/light/statusFailed.svg ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M8.44 1H7.56L1 13.26L1.44 14H14.54L14.98 13.26L8.44 1ZM2.28 13L8 2.28L13.7 13H2.28ZM7.5 6H8.5V10H7.5V6ZM7.5 11H8.5V12H7.5V11Z\" fill=\"#FFCC00\"/>\n<path d=\"M8.44 1H7.56L1 13.26L1.44 14H14.54L14.98 13.26L8.44 1ZM2.28 13L8 2.28L13.7 13H2.28ZM7.5 6H8.5V10H7.5V6ZM7.5 11H8.5V12H7.5V11Z\" fill=\"#DDB100\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusKilled.svg":
/*!********************************************!*\
  !*** ./style/icons/light/statusKilled.svg ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<rect x=\"3.5\" y=\"3.5\" width=\"9\" height=\"9\" stroke=\"#A1260D\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusPaused.svg":
/*!********************************************!*\
  !*** ./style/icons/light/statusPaused.svg ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<rect x=\"5\" y=\"3\" width=\"1\" height=\"10\" fill=\"#007ACC\"/>\n<rect x=\"10\" y=\"3\" width=\"1\" height=\"10\" fill=\"#007ACC\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusRunning.svg":
/*!*********************************************!*\
  !*** ./style/icons/light/statusRunning.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M4 2V14.4805L12.9146 8.24024L4 2ZM11.1809 8.24024L4.995 12.5684V3.91209L11.1809 8.24024Z\" fill=\"#388A34\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusSucceeded.svg":
/*!***********************************************!*\
  !*** ./style/icons/light/statusSucceeded.svg ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M14.3516 4.35156L6 12.7109L1.64844 8.35156L2.35156 7.64844L6 11.2891L13.6484 3.64844L14.3516 4.35156Z\" fill=\"#388A34\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusUnknown.svg":
/*!*********************************************!*\
  !*** ./style/icons/light/statusUnknown.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm9 3a1 1 0 11-2 0 1 1 0 012 0zM6.92 6.085c.081-.16.19-.299.34-.398.145-.097.371-.187.74-.187.28 0 .553.087.738.225A.613.613 0 019 6.25c0 .177-.04.264-.077.318a.956.956 0 01-.277.245c-.076.051-.158.1-.258.161l-.007.004a7.728 7.728 0 00-.313.195 2.416 2.416 0 00-.692.661.75.75 0 001.248.832.956.956 0 01.276-.245 6.3 6.3 0 01.26-.16l.006-.004c.093-.057.204-.123.313-.195.222-.149.487-.355.692-.662.214-.32.329-.702.329-1.15 0-.76-.36-1.348-.863-1.725A2.76 2.76 0 008 4c-.631 0-1.155.16-1.572.438-.413.276-.68.638-.849.977a.75.75 0 101.342.67z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/statusWaiting.svg":
/*!*********************************************!*\
  !*** ./style/icons/light/statusWaiting.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16 16\" width=\"16\" height=\"16\">\n    <path fill=\"#388A34\" fill-rule=\"evenodd\" d=\"M2.75 1a.75.75 0 000 1.5h.75v1.25a4.75 4.75 0 001.9 3.8l.333.25c.134.1.134.3 0 .4l-.333.25a4.75 4.75 0 00-1.9 3.8v1.25h-.75a.75.75 0 000 1.5h10.5a.75.75 0 000-1.5h-.75v-1.25a4.75 4.75 0 00-1.9-3.8l-.333-.25a.25.25 0 010-.4l.333-.25a4.75 4.75 0 001.9-3.8V2.5h.75a.75.75 0 000-1.5H2.75zM11 2.5H5v1.25a3.25 3.25 0 001.3 2.6l.333.25c.934.7.934 2.1 0 2.8l-.333.25a3.25 3.25 0 00-1.3 2.6v1.25h6v-1.25a3.25 3.25 0 00-1.3-2.6l-.333-.25a1.75 1.75 0 010-2.8l.333-.25a3.25 3.25 0 001.3-2.6V2.5z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/sub-folder.svg":
/*!******************************************!*\
  !*** ./style/icons/light/sub-folder.svg ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 14 16\" width=\"14\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M10 7H4v7h9c.55 0 1-.45 1-1V8h-4V7zM9 9H5V8h4v1zm4-5H7V3c0-.66-.31-1-1-1H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h2V7c0-.55.45-1 1-1h6c.55 0 1 .45 1 1h3V5c0-.55-.45-1-1-1zM6 4H1V3h5v1z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/tag.svg":
/*!***********************************!*\
  !*** ./style/icons/light/tag.svg ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 15 16\" width=\"15\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M7.73 1.73C7.26 1.26 6.62 1 5.96 1H3.5C2.13 1 1 2.13 1 3.5v2.47c0 .66.27 1.3.73 1.77l6.06 6.06c.39.39 1.02.39 1.41 0l4.59-4.59a.996.996 0 000-1.41L7.73 1.73zM2.38 7.09c-.31-.3-.47-.7-.47-1.13V3.5c0-.88.72-1.59 1.59-1.59h2.47c.42 0 .83.16 1.13.47l6.14 6.13-4.73 4.73-6.13-6.15zM3.01 3h2v2H3V3h.01z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/icons/light/terminal.svg":
/*!****************************************!*\
  !*** ./style/icons/light/terminal.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 14 16\" width=\"14\" height=\"16\">\n    <path fill=\"#424242\" fill-rule=\"evenodd\" d=\"M7 10h4v1H7v-1zm-3 1l3-3-3-3-.75.75L5.5 8l-2.25 2.25L4 11zm10-8v10c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V3c0-.55.45-1 1-1h12c.55 0 1 .45 1 1zm-1 0H1v10h12V3z\"/>\n</svg>\n");

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

/***/ "./style/aiida-icon.svg":
/*!******************************!*\
  !*** ./style/aiida-icon.svg ***!
  \******************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg' preserveAspectRatio='xMidYMid meet'%3E %3C!-- created using https://editor.method.ac --%3E %3Cg%3E %3Ctitle%3Ebackground%3C/title%3E %3Crect fill='none' id='canvas_background' height='402' width='582' y='-1' x='-1'/%3E %3C/g%3E %3Cg%3E %3Ctitle%3ELayer 1%3C/title%3E %3Cg id='svg_1' fill='%23000000' transform='translate(0, 200) scale(0.1, -0.1)'%3E %3Cpath fill='%2384D3DB' id='svg_2' d='m1370,1021c-75,-21 -101,-34 -161,-80c-68,-52 -135,-151 -153,-223l-6,-28l150,0l150,0l0,60c0,33 4,60 9,60c5,0 43,-20 85,-45c42,-24 106,-61 143,-81c81,-45 143,-83 143,-88c0,-3 -24,-18 -52,-33c-71,-39 -116,-65 -225,-129c-51,-30 -94,-54 -97,-54c-3,0 -6,29 -6,65l0,65l-151,0c-166,0 -152,6 -133,-61c14,-50 82,-145 135,-189c87,-72 151,-94 279,-95c88,0 115,4 163,23c119,48 224,166 261,291c30,102 13,250 -36,323c-10,14 -18,31 -18,36c0,16 -127,130 -168,151c-49,24 -158,51 -208,50c-21,0 -68,-8 -104,-18z'/%3E %3C/g%3E %3Cg id='svg_4' fill='%23000000' transform='rotate(-120, 102.445, 55.7986) translate(0, 200) scale(0.1, -0.1)'%3E %3Cpath fill='%23FFB27C' id='svg_3' d='m910,1861c-75,-21 -101,-34 -161,-80c-68,-52 -135,-151 -153,-223l-6,-28l150,0l150,0l0,60c0,33 4,60 9,60c5,0 43,-20 85,-45c42,-24 106,-61 143,-81c81,-45 143,-83 143,-88c0,-3 -24,-18 -52,-33c-71,-39 -116,-65 -225,-129c-51,-30 -94,-54 -97,-54c-3,0 -6,29 -6,65l0,65l-151,0c-166,0 -152,6 -133,-61c14,-50 82,-145 135,-189c87,-72 151,-94 279,-95c88,0 115,4 163,23c119,48 224,166 261,291c30,102 13,250 -36,323c-10,14 -18,31 -18,36c0,16 -127,130 -168,151c-49,24 -158,51 -208,50c-21,0 -68,-8 -104,-18z'/%3E %3C/g%3E %3Cg id='svg_6' fill='%23000000' transform='rotate(120, 56.4445, 139.799) translate(0, 200) scale(0.1, -0.1)'%3E %3Cpath fill='%238CD79F' id='svg_5' d='m450,1021c-75,-21 -101,-34 -161,-80c-68,-52 -135,-151 -153,-223l-6,-28l150,0l150,0l0,60c0,33 4,60 9,60c5,0 43,-20 85,-45c42,-24 106,-61 143,-81c81,-45 143,-83 143,-88c0,-3 -24,-18 -52,-33c-71,-39 -116,-65 -225,-129c-51,-30 -94,-54 -97,-54c-3,0 -6,29 -6,65l0,65l-151,0c-166,0 -152,6 -133,-61c14,-50 82,-145 135,-189c87,-72 151,-94 279,-95c88,0 115,4 163,23c119,48 224,166 261,291c30,102 13,250 -36,323c-10,14 -18,31 -18,36c0,16 -127,130 -168,151c-49,24 -158,51 -208,50c-21,0 -68,-8 -104,-18z'/%3E %3C/g%3E %3C/g%3E %3C/svg%3E"

/***/ })

}]);
//# sourceMappingURL=lib_index_js.45036b79273ef0585857.js.map