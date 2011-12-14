
var mcm = {};

mcm.util = {
	map : function (f, a) {
		r = new Array();

		var len = a.length;
		for (var i = 0; i < len; i++){
			r[i] = f(a[i]);
		}
		return r;
	},
	max : function (a) {
		var max = a[0];
		var len = a.length;
		for (var i = 1; i < len; i++) if (a[i] > max) max = a[i];
		return max;
	},
	min : function (a) {
		var min = a[0];
		var len = a.length;
		for (var i = 1; i < len; i++) if (a[i] < min) min = a[i];
		return min;
	},
	sprintf : function (format, etc) {
	    var arg = arguments;
	    var i = 1;
	    return format.replace(/%((%)|s)/g, function (m) { return m[2] || arg[i++] })
	}
};