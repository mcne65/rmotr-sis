(function () {
    window.mixpanel = mixpanel;
    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
    window.executeMixpanel = function(callable){
        if(!window.MIXPANEL_CONFIG.trackingEnabled){
            console.log("Tracking disabled");
            return;
        }else{
            console.log("Executing callable")
        }
        callable();
    }
    window.getParameterByName = getParameterByName;
}());
