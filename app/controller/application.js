define(["../model/constants", "../model/Model","./delegate"], 
function(constants, model, delegate) {
	
	var application = {};
	var ui = application.ui = {};
	
	/** Apply new state */
	application.setState = function (newState) {
		model.mainState(newState);
		application.updateDisplay();
	};
	
	/**
	 * Handler for "our" back button. We want the user to be able
	 * to use our back button or the browser back button, so
	 * we do the same thing.
	 */
	ui.back = application.back = function() {
		history.back();
	};
	
	/** Apply the state and the jQM enhancements */
	application.updateDisplay = function() {
		$(document).trigger("create");
		$("[data-role=listview]").listview("refresh");
	};
	
	/** 
	 * This function is called only once when application initializes.
	 * The routing mechanism will then take care of applying the right
	 * start page. 
	 */
	application.init = function() {
		delegate.init(function (loginInfos) {
			model.isAuthenticated(loginInfos[0]);
			model.userNickname(loginInfos[1]);
			model.logoutUrl(loginInfos[2]);
			model.loginUrl(loginInfos[3]);
			model.isAdmin(loginInfos[4]);
			application.updateDisplay();
		});
	}
	
	ui.logout = function() {
		location.href = model.logoutUrl();
	}
	
	ui.login = function() {
		location.href = model.loginUrl();
	}
	
	return application;
});