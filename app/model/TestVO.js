/**
 * A group of TestItemVO 
 */
define(["./constants", "./TestItemVO"], function(constants, TestItemVO) {
	
	return function() {
		var self = this;
		self.id = ko.observable("" + (new Date()).getTime());			// default id = timeStamp in seconds, as a String
		self.title = ko.observable("sans titre");
		self.testItemVOs = ko.observableArray();
		
		
		self.totalTestItems = ko.computed(function() {
			return self.testItemVOs().length;
		});
		
		self.addEmptyTestItems = function(n) {
			n = typeof(n) == "number" ? n : 3;		// when called from template, n is a testVO
			for (var i=0; i<n; i++)
				self.testItemVOs.push(new TestItemVO("", "", ""));
			$(document).trigger("create");		// TODO move into a controller
		};
		
		self.trimEmptyTestItems = function() {
			console.log("TRIM");
			for (var i=self.testItemVOs().length -1; i>=0; i--)
				if (!self.testItemVOs()[i].question() || !self.testItemVOs()[i].response())
					self.testItemVOs.splice(i, 1);
		};
		
		self.unrespondedTestItemVOs = ko.computed(function() {
			var result = [];
			var testItemVOs = self.testItemVOs();
			for (var i=0; i<testItemVOs.length; i++)
				if (!testItemVOs[i].isResponded())
					result.push(testItemVOs[i]);
			return result;
		});
		
		self.nbRespondedTestItem = ko.computed(function() {
			return self.totalTestItems() - self.unrespondedTestItemVOs().length;
		});
		
		self.nbUnrespondedTestItem = ko.computed(function() {
			return self.unrespondedTestItemVOs().length;
		});
		
		self.resetResults = function() {
			var testItemVOs = self.testItemVOs();
			for (var i=0; i<testItemVOs.length; i++)
				testItemVOs[i].resetResults();
		};

		
	};
	
});
