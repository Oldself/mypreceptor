define(["../model/constants", "../model/Model","./delegate", "./application"], 
function(constants, model, delegate, application) {
	
	var admin = {};
	var ui = admin.ui = {};
	

	/** Handler for the event requesting to show the admin page. */
	$(application).bind(constants.STATE_ADMIN, function(event) {
		console.log("admin");
		delegate.listUsers(function(result) {
			model.rawText(result);
			application.setState(constants.STATE_ADMIN);
		});
	});
	
	return admin;
});