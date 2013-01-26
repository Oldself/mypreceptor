/**
 * Local interface to the remote server API.
 */
define(["./mapper", "../model/constants"], function(mapper, constants){
	
	var delegate = {}
	
	/** Init: get user login and logout url */
	delegate.init = function(success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {'action':'init'},
			cache: false,
			success: function (loginInfos){
				checkAuth(loginInfos);
				success(loginInfos);
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "json"
		});
	};
	
	/** Get user tests list */
	delegate.getUserTests = function(success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {'action':'getUserTests'},
			cache: false,
			success: function (jsTestList){
				checkAuth(jsTestList);
				success(mapper.testVOs_fromJS(jsTestList));
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "json"
		});
	};

	/** Get test */
	delegate.getTest = function (testId, success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {'action':'getTest', 'testId':testId},
			cache: false,
			success: function(jsonTestVO) {
				success(mapper.testVO_fromJS(jsonTestVO));
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "json"
		});
	};
	
	/** Save test */
	delegate.saveTest = function (testId, testVO, success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {
				action:		'saveTest', 
				testId:		testId,
				title:		testVO.title(),
				testDTO:	mapper.testVO_toJSON(testVO)
			},
			cache: false,
			success: function(testId) {
				console.log(testId);
				success(testId);
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "json",
			type:"POST"
		});
	};
	
	/** Delete test */
	delegate.deleteTest = function (testId, success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {
				action:		'deleteTest', 
				testId:		testId
			},
			cache: false,
			success: function(result) {
				console.log(result);
				success(result);
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "text"
		});
	};
	
	delegate.genericErrorHandler = function(jqXHR, textStatus, errorThrown) { 
		alert("X:"+textStatus + " " + errorThrown);
	};
	
	function checkAuth(result) {
		console.log("CHECK AUTH");
		if (result instanceof Array && result.length && result[0] == "AUTHENTICATE")
			location.href = result[1];
	}
	
	return delegate;
	
});