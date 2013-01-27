define(["../model/constants", "../model/Model","./delegate", "./application"], 
function(constants, model, delegate, application) {
	
	var admin = {};
	var ui = admin.ui = {};
	

	/** Handler for the event requesting to show the admin page. */
	$(application).bind(constants.STATE_ADMIN, function(event, info) {
		console.log("admin");
		if (info == "listUsers")
			delegate.listUsers(function(result) {
				model.rawHtml("<pre>" + result + "</pre>");
				application.setState(constants.STATE_ADMIN);
			});
		else if (info == "releaseNotes")
			delegate.getHtml("/fr/ReleaseNotes.html", function(result) {
				model.rawHtml(result);
				application.setState(constants.STATE_ADMIN);
			});
	});
	
	return admin;
});