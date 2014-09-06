var cheerio = require("cheerio");
var fs = require('fs');

filename = '/home/hq/Desktop/raw-files/cat-urls.txt';
for(i=0;i<=40;i++){
  path = dirname + i + ".html";

  //  var file = fs.readFileSync(path, "utf8");
  fs.readFile(path, function (err, data) {
    if (err) {
      console.log(data);
      throw err;
    }
    var $ = cheerio.load(data);
    
    $(".card .cat .atm").remove();
    $(".card .loc .dot-product").each(function(){
      fs.appendFile(filename, $(this).attr("href") + "\n", function (err1) {
        if (err){
          console.log('The "data to append" was appended to file!');
          throw err1;
        }
      });
    });
  });
}


