/**
 * Convert value objets (VO) to and from JS (plain JavaScript object) or JSON
 */
define(["./mapper", "../model/TestVO", "../model/TestItemVO"], function(mapper, TestVO, TestItemVO){
	
	var mapper = {};
	
	/** TestVO LIST => VO */
	mapper.testVOs_fromJS = function(jsTestList) {
		var testVOs = [];
		var testVO;
		for (var i=0; i<jsTestList.length; i++) {
			testVO = new TestVO();
			testVO.id(jsTestList[i][0]);
			testVO.title(jsTestList[i][1]);
			testVOs.push(testVO);
		}
		return testVOs;
	};
	
	/** TestVO => VO */
	mapper.testVO_fromJS = function(jsonTestVO) {
		var testVO = new TestVO();
		testVO.id(jsonTestVO.id);
		testVO.title(jsonTestVO.title);
		for (var i=0; i<jsonTestVO.testItemVOs.length; i++) {
			var jsonTestItemVO = jsonTestVO.testItemVOs[i];
			var testItemVO = new TestItemVO(
				jsonTestItemVO.question,
				jsonTestItemVO.response,
				jsonTestItemVO.type
			);
			testVO.testItemVOs.push(testItemVO);
		}
		return testVO;
	};
	
	/** TestVO => JSON */
	mapper.testVO_toJSON = function(testVO) {
		return ko.toJSON(mapper.testVO_toJS(testVO));
	};
	
	/** TestVO => JS */
	mapper.testVO_toJS = function(testVO) {
		var jsTestVO = {
			title : testVO.title(),
			id: testVO.id(),
			testItemVOs : []
		};
		for (var i=0; i<testVO.testItemVOs().length; i++) {
			jsTestVO.testItemVOs.push(mapper.testItemVO_toJS(testVO.testItemVOs()[i]));
		}
		return jsTestVO;
	};
	
	/** TestItemVO => JS */
	mapper.testItemVO_toJS = function(testItemVO) {
		var result = {
			question: testItemVO.question(),
			response: testItemVO.response(),
			type: testItemVO.type()
		};
		return result;
	};
	
	return mapper;
	
});
