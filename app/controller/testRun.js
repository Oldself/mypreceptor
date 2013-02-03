/**
 * Controller managing the test execution page, as well as the test list display.
 */
define(["../model/constants","./delegate","../model/TestVO", "../model/Model", "./application"], function(constants, delegate, TestVO, model, application) {
	
	var testRun = {};
	var ui = testRun.ui = {};
	
	/** Handler for the event requesting to display the list of tests. */
	$(application).bind(constants.STATE_LIST_TESTS, function() { getListTests(false, constants.STATE_LIST_DEMO_TESTS); });
	
	/** Handler for the event requesting to display the list of demo tests. */
	$(application).bind(constants.STATE_LIST_DEMO_TESTS, function() { getListTests(true, constants.STATE_LIST_DEMO_TESTS); });
	
	function getListTests(isDemo, newState) {
		delegate.getUserTests(isDemo, function(jsTestVOs) {
			jsTestVOs.sort(function(a, b) {return a.title() > b.title() ? 1 : -1});
			model.testVOs.removeAll();
			for (var i=0; i<jsTestVOs.length; i++)
				model.testVOs.push(jsTestVOs[i]);
			application.setState(newState);
		});
	}
	
	/** Handler for the event requesting to run one test. */
	$(application).bind(constants.STATE_RUN_TEST, function(event, testId) {
		delegate.getTest(testId, function(testVO) {
			model.testVO(testVO);
			selectUnrespondedTestItem();
			application.setState(constants.STATE_RUN_TEST);
		});
	});
	
	/** When user press enter or space when result is shown as exact, proceed to next test. */
	$(document).bind("keypress", function(event) {
		var charCode = (typeof event.which == "number") ? event.which : event.keyCode;	// cross-browser !
		if ((charCode == 13 || charCode == 32) && model.mainState() == constants.STATE_RUN_TEST) {
			var testItemVO = model.testItemVO();
			if (testItemVO && testItemVO.normalizedInput() == testItemVO.normalizedResponse() && model.testVO().nbUnrespondedTestItem()!=0)
				ui.responseOK(testItemVO);
		}
	});

	/** Re run current test */
	ui.reRunTest = function () {
		model.testVO().resetResults();
		selectUnrespondedTestItem();
		application.setState(constants.STATE_RUN_TEST);
	};

	
	/** User says he had the right result */
	ui.responseOK = function(testItemVO) {
		testItemVO.result(constants.RESULT_PASS);
		selectUnrespondedTestItem();
		application.updateDisplay();
	};

	/** User says he had the wrong result */
	ui.responseNOK = function(testItemVO) {
		model.testItemVO().input("");
		selectUnrespondedTestItem();
		application.updateDisplay();
	};

	/** Randomly select an unresponded test item */
	function selectUnrespondedTestItem () {
		var testItemVOs = model.testVO().unrespondedTestItemVOs();
		var i = Math.floor(Math.random()*testItemVOs.length);
		model.testItemVO(testItemVOs.length && testItemVOs[i]);
	};
	
	return testRun;
});