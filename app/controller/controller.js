/**
 * This module has two roles:
 * 
 * 1 - declare the import of all individual controllers
 * 2 - centralize into a single 'ui' object all the methods that
 *     can be called from the user interface. 
 */
define(["./application", "./testEdition", "./testRun", "./routing"], 

	function() {

		var controller = {};
		var module;

		controller.ui = {};
		
		// Loop over the imported modules
		for (var i = 0; i < arguments.length; i++) {
			module = arguments[i];
			if (module.ui)
				// Loop over the module properties
				for(var property in module.ui)
					controller.ui[property] = module.ui[property];
		}
		
		return controller;
		
});