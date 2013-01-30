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
				// here we do not have to check for authentication, the caller takes care of it
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
	
	/** get any html page */
	delegate.getHtml = function (url, success, error) {
		$.ajax({
			url: url,
			cache: false,
			success: function(result) {
				checkAuth(result);
				success(result);
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "text"
		});
	};
	
	/** ADMIN: list users */
	delegate.listUsers = function (success, error) {
		$.ajax({
			url: constants.SERVER_URL,
			data: {
				action:		'listUsers'
			},
			cache: false,
			success: function(result) {
				checkAuth(result);
				success(result);
			},
			error: error ? error : delegate.genericErrorHandler,
			dataType: "json"
		});
	};
	
	delegate.genericErrorHandler = function(jqXHR, textStatus, errorThrown) { 
		alert("X:"+textStatus + " " + errorThrown);
	};
	
	function checkAuth(result) {
		var authLink = delegate.getAuthLink(result);
		if (authLink)
			location.href = authLink;
	}
	
	delegate.getAuthLink = function(result) {
		if (result instanceof Array && result.length && result[0] == "AUTHENTICATE")
			return result[1];
		return false;
	};
	
	
	return delegate;
	
});