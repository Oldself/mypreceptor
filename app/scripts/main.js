require([	"../model/Model", 
			"../controller/controller", 
			"../controller/application",
			"../scripts/crossroads.min",
			"../model/constants", 
			"../templates/master",
		], 
		function(
			model, 
			controller, 
			application,
			crossroads,
			constants
		) {

	$(document).ready(function() {
		if (!window.console)
			window.console = {log: function() {}};
		console.log("allez hop, on envoie la purée");
		
		// inject into the model the constants and controller functions
		for(var property in constants)
			model[property] = constants[property];
		for(var property in controller.ui)
			model.ui[property] = controller.ui[property];
			
		// For debug
		window.controller = controller;
		window.model = model; 

		ko.applyBindings(model);
		
		// Force the handling of current URL
		onBeforePageChange(undefined, {toPage:location.href});
		$(document).bind( "pagebeforechange", onBeforePageChange);
		
		application.init();
			
		/**
		 * This function is called by jQueryMobile each time 
		 * a new URL is clicked or changed by the browser 
		 */
		function onBeforePageChange (e, data) {
			e && e.preventDefault();
			// if the page change was hijacked by jQM, then expected HREF is data.toPage
			// else if the change was initiated by the browser (e.g. back) then we take the HREF from the location 
			var href = typeof data.toPage === "string" ? data.toPage : location.href;
			var hash = $.mobile.path.parseUrl( href ).hash;
			// Have crossroads process the routing
			crossroads.parse(hash);
			// update the location if necessary
			location.hash = hash;
		}


	});
	
});


