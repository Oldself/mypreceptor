define(["../model/constants","./delegate","../model/TestVO", "../model/Model", "./application", "./routing"], 
	function(constants, delegate, TestVO, model, application, routing) {
	
	var testEdition = {};
	var ui = testEdition.ui = {};

	/** Handler for the event requesting to edit a test. */
	$(application).bind(constants.STATE_EDIT_TEST, function(event, testId) {
		if (testId)
			delegate.getTest(testId, function(testVO) {
				model.testVO(testVO);
				application.setState(constants.STATE_EDIT_TEST);
			});
		else {
			model.testVO(new TestVO());
			model.testVO().addEmptyTestItems();
			application.setState(constants.STATE_EDIT_TEST);
		}
	});
	
	/** Save test */
	ui.saveTest = function() {
		model.testVO().trimEmptyTestItems();
		delegate.saveTest(model.testVO().id(), model.testVO(), function(testId){
			application.back();
		});
	};
	
	/** Delete test - popup show */
	ui.showTestDeleteConfirmPopup = function() {
		// Pour contourner bug jQM (??) pas de gestion de l'historique
		$("#deleteTestConfirmPopup").popup({ history: false });
		$("#deleteTestConfirmPopup").popup('open');
	};
	
	/** Delete test - popup hide*/
	ui.hideTestDeleteConfirmPopup = function() {
		$("#deleteTestConfirmPopup").popup('close');
	};
	
	/** Delete test */
	ui.deleteTest = function() {
		$("#deleteTestConfirmPopup").popup('close');
		delegate.deleteTest(model.testVO().id(), function() {
			model.testVO(undefined);
			// TODO: a voir: normalement on ne devrait pas passer par model.ui
			model.ui.gotoTestList();
		});
	};
	
	/** Capture tab on last input field to add new empty test item */
	ui.onKeyDown = function(testItemVO, event) {
		// tab was pressed
		if (event.keyCode == 9 && !event.shiftKey) {
			var testItemVOs = model.testVO().testItemVOs;
			if (testItemVOs.indexOf(testItemVO) == testItemVOs().length-1)
				model.testVO().addEmptyTestItems(1);
		}
		return true;
	}
	
	return testEdition;
});