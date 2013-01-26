define(["./constants", "../scripts/strings"], function(constants, strings) {

	return function(question, response, type) {
		var self = this;
		
		self.type = ko.observable(type);
		self.question = ko.observable(question);
		self.response = ko.observable(response);
		
		self.input = ko.observable("");		// user input with keyboard
		self.result = ko.observable();
		
		self.normalizedInput = ko.computed(function(){ return strings.normalize(self.input()); });
		self.normalizedResponse = ko.computed(function(){ return strings.normalize(self.response()); });
		
		self.isResponded = ko.computed(function(){
			return self.result() == constants.RESULT_PASS || self.input()==self.response();
		});
		
		self.resetResults = function() {
			self.input("");
			self.result(undefined);
		};
		
	};
	
});