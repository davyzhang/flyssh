
var system = require("system")
var args  = system.args
var username = args[1]
var password = args[2]
var productID = args[3]
var targetSvr = args[4]

if (args.length < 4){
	console.log("usage: phatomjs path/to/script username password productID targetSvr")
	console.log("eg. phantomjs test.js bob securitpass 987 02 ")
	console.log("this will change bob's ssh product id 987 to 02.flyssh.net")
	phantom.exit()
}

var page = require('webpage').create();

page.open('http://www.flyssh.net', function(status) {
	page.evaluate(function(username,password) {
		var txt = document.getElementsByName('username')[0]
		txt.value = username
		var pass = document.getElementsByName('password')[0]
		pass.value = password
		var form = document.getElementsByTagName("form")[0]
		form.submit()
	},username,password);
});

page.onLoadFinished = function(status){
	title = page.evaluate(
		function(status){
			return document.title
		}
	)
	console.log("page loaded: ",title)
	if (title == "我的账户 - FlySSH") {
		console.log("changing ssh server ... ",targetSvr)
		page.open("https://buy.flyssh.net/clientarea.php?action=productdetails&id="+productID,function(){
			// console.log(page.content)
			page.evaluate(function(targetSvr){
				var sel = document.getElementsByName("newsrv")[0]
				var form = sel.form
				var val = targetSvr
				var opts = sel.options
				var found = false
				for(var opt, j = 0; opt = opts[j]; j++) {
				        if(opt.value == val) {
				        	found = true
				            sel.selectedIndex = j;
				            break;
				        }
    			}
    			if (found){
    				form.submit()
    			}else{
    				console.log("can't find target server "+targetSvr+" please check the name and try again.")
    				phantom.exit()
    			}
			},targetSvr) 
		})
		page.onLoadFinished = null
	}

}

page.onAlert = function (msg) {
	console.log("page alert says:",msg)
	console.log("Done")
	phantom.exit()
}

