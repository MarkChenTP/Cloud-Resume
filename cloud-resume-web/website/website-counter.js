// Set url with the invoke URL of WebsiteVisitAPI Prod stage endpoint created from cloud-resume-app-sam-template.yaml
var xmlhttp = new XMLHttpRequest(),
  method = 'GET',
  url = 'https://j4t1bzn382.execute-api.us-east-2.amazonaws.com/prod/webvisit'; 
xmlhttp.open(method, url, true);

xmlhttp.onload = function () {
  // Do something with the retrieved data (found in xmlhttp.response)
  if (xmlhttp.readyState === xmlhttp.DONE) {
    if (xmlhttp.status === 200) {
      var jsonObj = JSON.parse(xmlhttp.response);
      document.getElementById("WebVisitCounter").innerHTML = 'Total Visits: ' + jsonObj.totalVisits;
    }
  }

};
xmlhttp.send(null);
