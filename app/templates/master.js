/**
 * Load the templates and insert append them to the body.
 */
define(
	[
		"text!./editTest.html",
		"text!./home.html",
		"text!./listTests.html",
		"text!./runTest.html"
	], 
	function () {
		for (var i = 0; i < arguments.length; i++) {
			$("body").append(arguments[i]);
		}
	}
);
