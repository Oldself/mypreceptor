define(["./constants", "../scripts/strings"], function(constants, strings) {

	return function(testVO, question, response, type) {
		var self = this;
		
		self.testVO = ko.observable(testVO);
		self.type = ko.observable(type);
		self.question = ko.observable(question);
		self.response = ko.observable(response);
		
		self.input = ko.observable("");		// user input with keyboard
		self.result = ko.observable();

		self.getResponse = ko.computed(function() {return self.testVO().reversedQA() ? self.question() : self.response(); });
		self.getQuestion = ko.computed(function() {return self.testVO().reversedQA() ? self.response() : self.question(); });
		
		self.normalizedInput = ko.computed(function(){ return strings.normalize(self.input(), self.testVO().diacriticalSensitive()); });
		self.normalizedResponse = ko.computed(function(){ return strings.normalize(self.getResponse(), self.testVO().diacriticalSensitive()); });
		
		self.isResponded = ko.computed(function(){
			return self.result() == constants.RESULT_PASS || self.input()==self.response();
		});
		
		self.resetResults = function() {
			self.input("");
			self.result(undefined);
		};
		
		
	};
	
});