define([], function(){
	
	var strings = {};
	
	/**
	 * Trim string, remove extra spaces and optionaly replace diacriticals.
	 */
	strings.normalize = function (text, diacriticalSensitive) {
		if (!text)
			return text;
		text = strings.trimExtraSpaces(strings.trim(text));
		if (!diacriticalSensitive)
			text = strings.replaceDiacriticals(text);
		return text;
	}

	/**
	 * Remove leading and trailing spaces
	 */
	strings.trim = function(text) {
		return text.replace(/^\s+|\s+$/g, "");
	}
	
	/**
	 * Remove extra spaces
	 */
	strings.trimExtraSpaces = function(text) {
		return text.replace(/\s\s+/g, " ");
	}
	
	/**
	 * Replace diacriticals and upper cases by their base counterpart (e.g. à => a, A => a).
	 * Convert all characters to lowercase.
	 */
	strings.replaceDiacriticals = function (text)
	{
		return text .replace(/[àâäáảãạăằắẳẵặâầấẩẫậÄÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ]/g, "a")
					.replace(/[èëéẻẽẹêềếểễệËÈÉẺẼẸÊỀẾỂỄỆ]/g, "e")
					.replace(/[ìïíỉĩịîÎÏÌÍỈĨỊ]/g, "i")
					.replace(/[öòóỏõọôồốổỗộơờớởỡợÖÒÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ]/g, "o")
					.replace(/[üûùúủũụưừứửữựÛÜÙÚỦŨỤƯỪỨỬỮỰ]/g, "u")
					.replace(/[ÿỳýỷỹỵỲÝỶỸỴ]/g, "y")
					.replace(/[đĐ]/g, "d")
					.replace(/[çÇ]/g, "c")
					.toLowerCase();
	}
	
	return strings;

});
