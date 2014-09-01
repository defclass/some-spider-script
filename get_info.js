var request = require("request");
var cheerio = require("cheerio");

var url = "http://www.alibaba.com/products/F0/plastic_recycle/----------------------50----------------------------EU.html";
var exec = require('child_process').exec;
urls = new Array();
exec("curl "+url,{maxBuffer: 1024 * 1000000}, function (error, stdout, stderr) {
  if (error !== null) {
    console.log('exec error: ' + error);
    exit();
  }
  var $ = cheerio.load(stdout);
  $(".card .cat .atm").remove();
  $(".card .cat .dot-product").each(function(){
    urls.push($(this).attr("href"));
  });
  console.log("abc");
  
});
console.log("def");

