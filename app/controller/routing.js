/**
 * This module handles the routing.
 * 
 * ui.xyz : functions called from the UI to request the display of a given "page".
 * 			These functions are called with the KO context data.
 * 
 * crossroads.addRoute : handler function to actually apply the layout corresponding to a URL
 * 
 */
define([
		"../model/constants", 
		"../scripts/crossroads.min", 
		"../model/Model", 
		"./application"
	], function(
		constants, 
		crossroads, 
		model, 
		application
	) {

	var routing = {};
	var ui = routing.ui = {};
	var routingEventDispatcher = application;
	
	// Home page
	ui.gotoHome = function() { application.setState(constants.STATE_HOME);};
	routing.gotoHome = ui.gotoHome;
	crossroads.addRoute('', routing.gotoHome);
	crossroads.addRoute('#', routing.gotoHome);		// needed for IE8
	
	// List tests for a user
	ui.gotoTestList = function(arg) { changePage("listTests"); };
	routing.gotoTestList = function () { $(routingEventDispatcher).trigger(constants.STATE_LIST_TESTS); };
	crossroads.addRoute('#listTests', routing.gotoTestList);

	// List demo tests
	ui.gotoTestListDemo = function() { changePage("listTestsDemo"); };
	routing.gotoTestListDemo = function () { $(routingEventDispatcher).trigger(constants.STATE_LIST_TESTS, ["demo"]); };
	crossroads.addRoute('#listTestsDemo', routing.gotoTestListDemo);
	
	// Run a test
	ui.gotoRunTest = function(testVO) { changePage("runTest?testId=" + testVO.id());	};
	routing.gotoRunTest = function(testId) { $(routingEventDispatcher).trigger(constants.STATE_RUN_TEST, [testId]); };
	crossroads.addRoute('#runTest?testId={testId}', routing.gotoRunTest);

	// Create new test	
	ui.gotoNewTest = function(testVO) { changePage("newTest");	};
	routing.gotoNewTest = function() { $(routingEventDispatcher).trigger(constants.STATE_EDIT_TEST) }; 
	crossroads.addRoute('#newTest', routing.gotoNewTest);
	
	// Edit existing test
	ui.gotoEditTest = function(testVO) { changePage("editTest?testId=" + testVO.id()); };
	routing.gotoEditTest = function(testId) { $(routingEventDispatcher).trigger(constants.STATE_EDIT_TEST, [testId]) }; 
	crossroads.addRoute('#editTest?testId={testId}', routing.gotoEditTest);
	
	// Admin page
	ui.gotoAdmin = function(info) { changePage("admin?info=" + info); };
	routing.gotoAdmin = function(info) { $(routingEventDispatcher).trigger(constants.STATE_ADMIN, [info]) }; 
	crossroads.addRoute('#admin?info={info}', routing.gotoAdmin);
	
	/** Helper function to change the location according to requested page */
	function changePage(newHash) {
		location.hash = newHash;
	}	

	return routing;
		
});