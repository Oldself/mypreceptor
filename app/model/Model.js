define(["./constants"], function(constants) {

	var model = function() {
	    var self = this;
		
	    self.isTouchDevice = "ontouchstart" in document.documentElement;
	    
		self.userNickname = ko.observable();
		self.isAdmin = ko.observable(false);
	    self.logoutUrl = ko.observable("");

		self.testVOs = ko.observableArray();
		self.testVO = ko.observable();
		self.testItemVO = ko.observable();
		self.mainState = ko.observable();
		
		self.testId = ko.observable();
		
		self.autoFocus = ko.observable(!self.isTouchDevice);
		
		// attachment point for functions that can be called from the UI
		self.ui = {};
		
		self.rawText = ko.observable("");		
	};
	
	// Le module est une instance du modèle
	return new model();

});