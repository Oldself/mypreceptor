define(["../model/constants", "../model/Model","./delegate"], 
function(constants, model, delegate) {
	
	var application = {};
	var ui = application.ui = {};
	
	/** Apply new state */
	application.setState = function (newState) {
		model.mainState(newState);
		application.updateDisplay();
	};
	
	ui.back = application.back = function() {
		// TODO: ici il faut gérer vers quelle page on veut réellement remonter car en cas de lien profond, le back ne veut rien dire
		history.back();
	};
	
	/** Apply the state and the jQM enhancements */
	application.updateDisplay = function() {
		$(document).trigger("create");
		$("[data-role=listview]").listview("refresh");
	};
	
	/** This function is called only once when application initializes. */
	application.init = function() {
		delegate.init(function (loginInfos) {
			var authLink = delegate.getAuthLink(loginInfos);
			if (authLink) {
				model.isAuthenticated(false);
				model.loginUrl(authLink);
				model.ui.gotoHome();
				model.userNickname("demo");
				model.isAdmin(false);
			}
			else {
				model.isAuthenticated(true);
				model.userNickname(loginInfos[0]);
				model.logoutUrl(loginInfos[1]);
				model.loginUrl(loginInfos[2]);
				model.isAdmin(loginInfos[3]);
			}
			application.updateDisplay();
		});
	}
	
	ui.logout = function() {
		location.href = model.logoutUrl();
	}
	
	return application;
});