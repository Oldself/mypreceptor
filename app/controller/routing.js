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
	
	// List tests for a user
	ui.gotoTestList = function() { changePage("listTests"); };
	routing.gotoTestList = function () { $(routingEventDispatcher).trigger(constants.STATE_LIST_TESTS); };
	crossroads.addRoute('#listTests', routing.gotoTestList);
	
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
	
	/** Helper function to change the location according to requested page */
	function changePage(newHash) {
		location.hash = newHash;
	}	

	return routing;
		
});