define(["./constants"], function(constants) {

	return function(question, response, type) {
		var self = this;
		
		self.type = ko.observable(type);
		self.question = ko.observable(question);
		self.response = ko.observable(response);
		
		self.input = ko.observable("");		// user input with keyboard
		self.result = ko.observable();
		
		self.normalizedInput = ko.computed(function(){ return self.input() && self.input().toLowerCase(); });
		self.normalizedResponse = ko.computed(function(){ return self.response() && self.response().toLowerCase(); });
		
		self.isResponded = ko.computed(function(){
			return self.result() == constants.RESULT_PASS || self.input()==self.response();
		});
		
		self.resetResults = function() {
			self.input("");
			self.result(undefined);
		};
		
	};
});