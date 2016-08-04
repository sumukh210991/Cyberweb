// Ajax client helper library, uses POST
// Alan Riggins, CS596 SP 2010

function HttpRequest(sURL, fpCallback) {
    this.request = this.createXmlHttpRequest();
    this.request.open("POST", sURL, true);
    
    var tempRequest = this.request;
    tempRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
    function requestReadyStateChange() {
        if(tempRequest.readyState == 4) {
            if(tempRequest.status == 200) {
                fpCallback(tempRequest.responseText);
                } else if(tempRequest.status == 401) {
                	window.location.href = '/signin';
                }
            else {
                alert("An error occurred while trying to communicate with the server"
                + " ready state: " + tempRequest.readyState +
                  " status: " + tempRequest.status);
                }
            }
        }
        
    this.request.onreadystatechange = requestReadyStateChange;    
}
    
HttpRequest.prototype.createXmlHttpRequest = function() {
    if(window.XMLHttpRequest) {
        var oHttp = new XMLHttpRequest();
        return oHttp;
    }
    else if(window.ActiveXObject) {
        var version = ("MSXML2.XmlHttp.6.0",
                       "MSXML2.XmlHttp.3.0",
                       "MSXML2.XmLHttp",
                       "Microsoft.XMLHTTP");
        for(var i=0; i < version.length; i++) {
            try {
                var oHttp = new ActiveXObject(version[i]);
                return oHttp;
                }
            catch(err) {} // do nothing here
            }
        }
    return null;        
}
    
HttpRequest.prototype.send = function(params) {
    this.request.send(params);
}