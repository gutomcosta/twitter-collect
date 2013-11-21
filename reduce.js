db = db.getMongo().getDB( "tweets_boston_db" );


var getDateFrom = function(doc) {
	var s = doc.created_at;
 	var date = new Date(s.replace(/^\w+ (\w+) (\d+) ([\d:]+) \+0000 (\d+)$/,"$1 $2 $4 $3 UTC"));
 	var dateKey = date.getMonth()+"/"+date.getDate()+"/"+date.getFullYear()+"  "+date.getHours()+":"+date.getMinutes();
 	var time = date.getHours()+":"+date.getMinutes();
	return {'date': new Date(dateKey), 'sdate': dateKey, 'time':time};
};


var result = db.tweets.group({ keyf: getDateFrom, initial: {count:0}, reduce: function(obj,prev) {prev.count++;} });

for (var i = 0; i < result.length; i++) {
	var line = result[i]["time"]+";"+result[i]["count"];
	printjson(line)
};



