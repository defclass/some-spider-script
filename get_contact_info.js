var cheerio = require("cheerio");
var fs = require('fs');

filename = '/home/hq/Desktop/raw-files/company-info.cvs';
dirname = "/home/hq/Desktop/raw-files/ContactPages/";


var dirList = fs.readdirSync(dirname);

dirList.forEach(function(item){
  if(!fs.statSync(dirname + '/' + item).isDirectory()){
    //如果不是目录，读入该文件
    fs.readFile(dirname + '/' + item, function (err, data) {
      if (err) {
        console.log(data);
        throw err;
      }
      var $ = cheerio.load(data);
      var key = null;
      var i = 0;
      var one_info = [];
      
      $("#contact-person .contact-detail .dl-horizontal").children().each(function(){
        var text = $(this).text().replace(/:/g,'');
        
        if(key == null ){
          key = text;
        } else {
          if(key == "Telephone"){
            one_info["Telephone"] = text;
          }
          else if(key == "Fax"){
            one_info["Fax"] = text;
          }
          else if(key == "Address"){
            one_info["Address"] = text;
          }
          else if(key == "Country/Region"){
            one_info["Country/Region"] = text;
          }
          else if(key == "Province/State"){
            one_info["Province/State"] = text;
          }
          else if (key == "City"){
            one_info["City"] = text;
          }
          key = null ;
        }
      });
      var comp_name = $(".company-info-data tr td:last-child").html();
      var website = $(".company-info-data td a").html();
      one_info["comp_name"] = comp_name;
      one_info["website"] = website;

      var stand_info = [];
      stand_info['comp_name'] = "N/A";
      stand_info['website'] = "N/A";
      stand_info['Telephone'] = "N/A";
      stand_info['Fax'] = "N/A";
      stand_info['Country/Region'] = "N/A";
      stand_info['Province/State'] = "N/A";
      stand_info['City'] = "N/A";


      var str = "";
      for(var stand_key in stand_info){
        if(one_info.hasOwnProperty(stand_key)){
          stand_info[stand_key] = one_info[stand_key];
        }
        str = str +  stand_info[stand_key] + ",";
      }
      
      fs.appendFile(filename, str + "\n" , function (err1) {
        if (err){
          console.log('The "data to append" was appended to file!');
          throw err1;
        }
      });
    });
  }
});
