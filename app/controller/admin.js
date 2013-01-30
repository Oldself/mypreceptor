define(["../model/constants", "../model/Model","./delegate", "./application"], 
function(constants, model, delegate, application) {
	
	var admin = {};
	var ui = admin.ui = {};
	

	/** Handler for the event requesting to show the admin page. */
	$(application).bind(constants.STATE_ADMIN, function(event, info) {
		console.log("admin");
		if (info == "listUsers")
			delegate.listUsers(function(result) {
				var tmp = "<h3>Liste des utilisateurs</h3><table>";
				tmp += "<tr><th width=75%>nickname</th><th>nb tests</th></tr>";
				for (var i=0; i<result.length; i++)
					tmp += "<tr><td>" + result[i][0] + "</td><td>" + result[i][1] + "</td></tr>";
				tmp += "</table>"
				model.rawHtml(tmp);
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