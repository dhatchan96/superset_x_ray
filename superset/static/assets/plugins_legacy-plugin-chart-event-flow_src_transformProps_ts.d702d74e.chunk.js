"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(globalThis["webpackChunksuperset"] = globalThis["webpackChunksuperset"] || []).push([["plugins_legacy-plugin-chart-event-flow_src_transformProps_ts"],{

/***/ "./plugins/legacy-plugin-chart-event-flow/src/transformProps.ts":
/*!**********************************************************************!*\
  !*** ./plugins/legacy-plugin-chart-event-flow/src/transformProps.ts ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ transformProps)\n/* harmony export */ });\n/* harmony import */ var _data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @data-ui/event-flow */ \"./node_modules/@data-ui/event-flow/build/index.js\");\n/* harmony import */ var _data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__);\n/* module decorator */ module = __webpack_require__.hmd(module);\n(function () {var enterModule = typeof reactHotLoaderGlobal !== 'undefined' ? reactHotLoaderGlobal.enterModule : undefined;enterModule && enterModule(module);})();var __signature__ = typeof reactHotLoaderGlobal !== 'undefined' ? reactHotLoaderGlobal.default.signature : function (a) {return a;};\nfunction transformProps(chartProps) {\n  const { formData, queriesData, width, height } = chartProps;\n  const { allColumnsX, entity, minLeafNodeEventCount } = formData;\n  const { data } = queriesData[0];\n  const hasData = data && data.length > 0;\n  if (hasData) {\n    const userKey = entity;\n    const eventNameKey = allColumnsX;\n    // map from the Superset form fields to <EventFlow />'s expected data keys\n    const accessorFunctions = {\n      [_data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__.ENTITY_ID]: (datum) => String(datum[userKey]),\n      [_data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__.EVENT_NAME]: (datum) => datum[eventNameKey],\n      [_data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__.TS]: (datum) =>\n      // eslint-disable-next-line no-underscore-dangle\n      datum.__timestamp || datum.__timestamp === 0 ?\n      // eslint-disable-next-line no-underscore-dangle\n      new Date(datum.__timestamp) :\n      null\n    };\n    const cleanData = (0,_data_ui_event_flow__WEBPACK_IMPORTED_MODULE_0__.cleanEvents)(data, accessorFunctions);\n    return {\n      data: cleanData,\n      height,\n      initialMinEventCount: minLeafNodeEventCount,\n      width\n    };\n  }\n  return { data: null, height, width };\n};(function () {var reactHotLoader = typeof reactHotLoaderGlobal !== 'undefined' ? reactHotLoaderGlobal.default : undefined;if (!reactHotLoader) {return;}reactHotLoader.register(transformProps, \"transformProps\", \"D:\\\\CodeKata\\\\superset\\\\superset-frontend\\\\plugins\\\\legacy-plugin-chart-event-flow\\\\src\\\\transformProps.ts\");})();;(function () {var leaveModule = typeof reactHotLoaderGlobal !== 'undefined' ? reactHotLoaderGlobal.leaveModule : undefined;leaveModule && leaveModule(module);})();//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9wbHVnaW5zL2xlZ2FjeS1wbHVnaW4tY2hhcnQtZXZlbnQtZmxvdy9zcmMvdHJhbnNmb3JtUHJvcHMudHMiLCJtYXBwaW5ncyI6Ijs7Ozs7OztBQW1CQTtBQWVBO0FBQ0E7QUFFQTtBQUNBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBRUE7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBR0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL3N1cGVyc2V0Ly4vcGx1Z2lucy9sZWdhY3ktcGx1Z2luLWNoYXJ0LWV2ZW50LWZsb3cvc3JjL3RyYW5zZm9ybVByb3BzLnRzPzQ0MjIiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXHJcbiAqIExpY2Vuc2VkIHRvIHRoZSBBcGFjaGUgU29mdHdhcmUgRm91bmRhdGlvbiAoQVNGKSB1bmRlciBvbmVcclxuICogb3IgbW9yZSBjb250cmlidXRvciBsaWNlbnNlIGFncmVlbWVudHMuICBTZWUgdGhlIE5PVElDRSBmaWxlXHJcbiAqIGRpc3RyaWJ1dGVkIHdpdGggdGhpcyB3b3JrIGZvciBhZGRpdGlvbmFsIGluZm9ybWF0aW9uXHJcbiAqIHJlZ2FyZGluZyBjb3B5cmlnaHQgb3duZXJzaGlwLiAgVGhlIEFTRiBsaWNlbnNlcyB0aGlzIGZpbGVcclxuICogdG8geW91IHVuZGVyIHRoZSBBcGFjaGUgTGljZW5zZSwgVmVyc2lvbiAyLjAgKHRoZVxyXG4gKiBcIkxpY2Vuc2VcIik7IHlvdSBtYXkgbm90IHVzZSB0aGlzIGZpbGUgZXhjZXB0IGluIGNvbXBsaWFuY2VcclxuICogd2l0aCB0aGUgTGljZW5zZS4gIFlvdSBtYXkgb2J0YWluIGEgY29weSBvZiB0aGUgTGljZW5zZSBhdFxyXG4gKlxyXG4gKiAgIGh0dHA6Ly93d3cuYXBhY2hlLm9yZy9saWNlbnNlcy9MSUNFTlNFLTIuMFxyXG4gKlxyXG4gKiBVbmxlc3MgcmVxdWlyZWQgYnkgYXBwbGljYWJsZSBsYXcgb3IgYWdyZWVkIHRvIGluIHdyaXRpbmcsXHJcbiAqIHNvZnR3YXJlIGRpc3RyaWJ1dGVkIHVuZGVyIHRoZSBMaWNlbnNlIGlzIGRpc3RyaWJ1dGVkIG9uIGFuXHJcbiAqIFwiQVMgSVNcIiBCQVNJUywgV0lUSE9VVCBXQVJSQU5USUVTIE9SIENPTkRJVElPTlMgT0YgQU5ZXHJcbiAqIEtJTkQsIGVpdGhlciBleHByZXNzIG9yIGltcGxpZWQuICBTZWUgdGhlIExpY2Vuc2UgZm9yIHRoZVxyXG4gKiBzcGVjaWZpYyBsYW5ndWFnZSBnb3Zlcm5pbmcgcGVybWlzc2lvbnMgYW5kIGxpbWl0YXRpb25zXHJcbiAqIHVuZGVyIHRoZSBMaWNlbnNlLlxyXG4gKi9cclxuaW1wb3J0IHsgQ2hhcnRQcm9wcywgVGltZXNlcmllc0RhdGFSZWNvcmQgfSBmcm9tICdAc3VwZXJzZXQtdWkvY29yZSc7XHJcbmltcG9ydCB7IGNsZWFuRXZlbnRzLCBUUywgRVZFTlRfTkFNRSwgRU5USVRZX0lEIH0gZnJvbSAnQGRhdGEtdWkvZXZlbnQtZmxvdyc7XHJcblxyXG5leHBvcnQgaW50ZXJmYWNlIEV2ZW50Rmxvd0Zvcm1EYXRhIHtcclxuICBhbGxDb2x1bW5zWDogc3RyaW5nO1xyXG4gIGVudGl0eTogc3RyaW5nO1xyXG4gIG1pbkxlYWZOb2RlRXZlbnRDb3VudDogbnVtYmVyO1xyXG59XHJcblxyXG5leHBvcnQgaW50ZXJmYWNlIEV2ZW50Rmxvd0NoYXJ0UHJvcHMgZXh0ZW5kcyBDaGFydFByb3BzIHtcclxuICBmb3JtRGF0YTogRXZlbnRGbG93Rm9ybURhdGE7XHJcbiAgcXVlcmllc0RhdGE6IHtcclxuICAgIGRhdGE6IFRpbWVzZXJpZXNEYXRhUmVjb3JkW107XHJcbiAgfVtdO1xyXG59XHJcblxyXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB0cmFuc2Zvcm1Qcm9wcyhjaGFydFByb3BzOiBDaGFydFByb3BzKSB7XHJcbiAgY29uc3QgeyBmb3JtRGF0YSwgcXVlcmllc0RhdGEsIHdpZHRoLCBoZWlnaHQgfSA9XHJcbiAgICBjaGFydFByb3BzIGFzIEV2ZW50Rmxvd0NoYXJ0UHJvcHM7XHJcbiAgY29uc3QgeyBhbGxDb2x1bW5zWCwgZW50aXR5LCBtaW5MZWFmTm9kZUV2ZW50Q291bnQgfSA9IGZvcm1EYXRhO1xyXG4gIGNvbnN0IHsgZGF0YSB9ID0gcXVlcmllc0RhdGFbMF07XHJcblxyXG4gIGNvbnN0IGhhc0RhdGEgPSBkYXRhICYmIGRhdGEubGVuZ3RoID4gMDtcclxuICBpZiAoaGFzRGF0YSkge1xyXG4gICAgY29uc3QgdXNlcktleSA9IGVudGl0eTtcclxuICAgIGNvbnN0IGV2ZW50TmFtZUtleSA9IGFsbENvbHVtbnNYO1xyXG5cclxuICAgIC8vIG1hcCBmcm9tIHRoZSBTdXBlcnNldCBmb3JtIGZpZWxkcyB0byA8RXZlbnRGbG93IC8+J3MgZXhwZWN0ZWQgZGF0YSBrZXlzXHJcbiAgICBjb25zdCBhY2Nlc3NvckZ1bmN0aW9ucyA9IHtcclxuICAgICAgW0VOVElUWV9JRF06IChkYXR1bTogVGltZXNlcmllc0RhdGFSZWNvcmQpID0+IFN0cmluZyhkYXR1bVt1c2VyS2V5XSksXHJcbiAgICAgIFtFVkVOVF9OQU1FXTogKGRhdHVtOiBUaW1lc2VyaWVzRGF0YVJlY29yZCkgPT5cclxuICAgICAgICBkYXR1bVtldmVudE5hbWVLZXldIGFzIHN0cmluZyxcclxuICAgICAgW1RTXTogKGRhdHVtOiBUaW1lc2VyaWVzRGF0YVJlY29yZCk6IERhdGUgfCBudWxsID0+XHJcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLXVuZGVyc2NvcmUtZGFuZ2xlXHJcbiAgICAgICAgZGF0dW0uX190aW1lc3RhbXAgfHwgZGF0dW0uX190aW1lc3RhbXAgPT09IDBcclxuICAgICAgICAgID8gLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLXVuZGVyc2NvcmUtZGFuZ2xlXHJcbiAgICAgICAgICAgIG5ldyBEYXRlKGRhdHVtLl9fdGltZXN0YW1wKVxyXG4gICAgICAgICAgOiBudWxsLFxyXG4gICAgfTtcclxuXHJcbiAgICBjb25zdCBjbGVhbkRhdGEgPSBjbGVhbkV2ZW50cyhkYXRhLCBhY2Nlc3NvckZ1bmN0aW9ucyk7XHJcblxyXG4gICAgcmV0dXJuIHtcclxuICAgICAgZGF0YTogY2xlYW5EYXRhLFxyXG4gICAgICBoZWlnaHQsXHJcbiAgICAgIGluaXRpYWxNaW5FdmVudENvdW50OiBtaW5MZWFmTm9kZUV2ZW50Q291bnQsXHJcbiAgICAgIHdpZHRoLFxyXG4gICAgfTtcclxuICB9XHJcblxyXG4gIHJldHVybiB7IGRhdGE6IG51bGwsIGhlaWdodCwgd2lkdGggfTtcclxufVxyXG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./plugins/legacy-plugin-chart-event-flow/src/transformProps.ts\n");

/***/ })

}]);