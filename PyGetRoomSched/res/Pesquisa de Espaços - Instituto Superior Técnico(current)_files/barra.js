/* 
 * a backwards compatable implementation of postMessage
 * by Josh Fraser (joshfraser.com)
 * released under the Apache 2.0 license.  
 *
 * this code was adapted from Ben Alman's jQuery postMessage code found at:
 * http://benalman.com/projects/jquery-postmessage-plugin/
 * 
 * other inspiration was taken from Luke Shepard's code for Facebook Connect:
 * http://github.com/facebook/connect-js/blob/master/src/core/xd.js
 *
 * the goal of this project was to make a backwards compatable version of postMessage
 * without having any dependency on jQuery or the FB Connect libraries
 *
 * my goal was to keep this as terse as possible since my own purpose was to use this 
 * as part of a distributed widget where filesize could be sensative.
 * 
 */

// everything is wrapped in the XD function to reduce namespace collisions
var XD = function(){
  
    var interval_id,
    last_hash,
    cache_bust = 1,
    attached_callback,
    window = this;
    
    return {
        postMessage : function(message, target_url, target) {
            
            if (!target_url) { 
                return; 
            }
    
            target = target || parent;  // default to parent
    
            if (window['postMessage']) {
                // the browser supports window.postMessage, so call it with a targetOrigin
                // set appropriately, based on the target_url parameter.
                target['postMessage'](message, target_url.replace( /([^:]+:\/\/[^\/]+).*/, '$1'));

            } else if (target_url) {
                // the browser does not support window.postMessage, so set the location
                // of the target to target_url#message. A bit ugly, but it works! A cache
                // bust parameter is added to ensure that repeat messages trigger the callback.
                target.location = target_url.replace(/#.*$/, '') + '#' + (+new Date) + (cache_bust++) + '&' + message;
            }
        },
  
	    receiveMessage : function(callback, source_origin) {
            
            // browser supports window.postMessage
            if (window['postMessage']) {
                // bind the callback to the actual event associated with window.postMessage
                if (callback) {
                    attached_callback = function(e) {
                        if ((typeof source_origin === 'string' && e.origin !== source_origin)
			    || (Object.prototype.toString.call(source_origin) === "[object Function]" && source_origin(e.origin) === !1)) {
                            return !1;
                        }
                        callback(e);
                    };
                }
                if (window['addEventListener']) {
                    window[callback ? 'addEventListener' : 'removeEventListener']('message', attached_callback, !1);
                } else {
                    window[callback ? 'attachEvent' : 'detachEvent']('onmessage', attached_callback);
                }
            } else {
                // a polling loop is started & callback is called whenever the location.hash changes
                interval_id && clearInterval(interval_id);
                interval_id = null;

                if (callback) {
                    interval_id = setInterval(function(){
			    var hash = document.location.hash,
			    re = /^#?\d+&/;
			    if (hash !== last_hash && re.test(hash)) {
				last_hash = hash;
				callback({data: hash.replace(re, '')});
			    }
			}, 100);
                }
            }   
        }
    };
}();

(function () {
    if (!Array.prototype.reduce){
      Array.prototype.reduce = function(fun){
        var len = this.length;
        if (typeof fun != "function")
          throw new TypeError();

        // no value to return if no initial value and an empty array
        if (len == 0 && arguments.length == 1)
          throw new TypeError();

        var i = 0;
        if (arguments.length >= 2)
        {
          var rv = arguments[1];
        }
        else
        {
          do
          {
            if (i in this)
            {
              rv = this[i++];
              break;
            }

            // if array contains no values, no initial value to return
            if (++i >= len)
              throw new TypeError();
          }
          while (true);
        }

        for (; i < len; i++)
        {
          if (i in this)
            rv = fun.call(null, rv, this[i], i, this);
        }

        return rv;
      };
    }
    if (!Array.prototype.map){
      Array.prototype.map = function(fun){
        var len = this.length;
        if (typeof fun != "function")
          throw new TypeError();

        var res = new Array(len);
        var thisp = arguments[1];
        for (var i = 0; i < len; i++)
        {
          if (i in this)
            res[i] = fun.call(thisp, this[i], i, this);
        }

        return res;
      };
    }

    var scriptEl = document.getElementById("ist-bar");
    if (!scriptEl){
        var elements = document.getElementsByTagName("script");
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i]
            if (el.getAttribute("src") && el.getAttribute("src").match(/barra\.js$/)){
                if (el.parentNode == document.head){
                    alert("Barra incluida no <Head>. Deve ser incluida no body no ponto onde se deseja apresentar.")
                    return;
                }else{
                    scriptEl = el;
                    break;
                }
            }
        };
    }
    var _server = scriptEl.getAttribute("src").match("(https?://[^/]+)/.*")[1]
    var barClosed=true
    function resize(a){
        if (a.data == "resize"){
            if (barClosed){
                barClosed = false
                $_istBarraJQ("#ist-bar-container").animate({
                    height: '430px'
                }, 350)
                $_istBarraJQ("#ist-bar-iframe").animate({
                    height: '430px'
                }, 350)
            }else{
            barClosed = true
                $_istBarraJQ("#ist-bar-container").animate({
                    height: '34px'
                }, 350)
                $_istBarraJQ("#ist-bar-iframe").animate({
                    height: '34px'
                }, 350)
            }
        }else if (a.data.match("link:(.*)")){
            window.location = a.data.match("link:(.*)")[1]
        }else if (a.data.match("auth:(.*)")){
            window.location = _server + a.data.match("auth:(.*)")[1]
        }
    }
	
    function resource(x) { return _server + x; }
    
    var fileref=document.createElement('script')
    fileref.setAttribute("type","text/javascript")
    fileref.setAttribute("src", resource("/site_media/static/js/jquery.js"))
    document.getElementsByTagName("head")[0].appendChild(fileref)
   
    var headID = document.getElementsByTagName("head")[0];         
    var cssNode = document.createElement('link');
    cssNode.type = 'text/css';
    cssNode.rel = 'stylesheet';
    cssNode.href = resource("/site_media/static/css/barra-inc.css");
    cssNode.media = 'screen';
    headID.appendChild(cssNode);
   
    var referenceNode = scriptEl;
    var container = document.createElement("div");
    container.setAttribute("id","ist-bar-container");
    var newIframe = document.createElement("iframe");
    newIframe.setAttribute("id","ist-bar-iframe");
    newIframe.setAttribute("frameBorder","0");
//    newIframe.setAttribute("vspace","0");
//    newIframe.setAttribute("hspace","0");
    newIframe.setAttribute("marginwidth","0");
    newIframe.setAttribute("marginheight","0");
    newIframe.setAttribute("scrolling","no");
    var query = []
    
    if (scriptEl.getAttribute("data-fluid") == "true"){
        query.push(["fluid",scriptEl.getAttribute("data-fluid")])   
    }

    if (scriptEl.getAttribute("data-use-offline") == "true"){
        query.push(["offline",scriptEl.getAttribute("data-use-offline")])   
    }

    if (scriptEl.getAttribute("data-login")){
        query.push(["login",scriptEl.getAttribute("data-login")])   
    }

    if (scriptEl.getAttribute("data-logout")){
        query.push(["logout",scriptEl.getAttribute("data-logout")])   
    }
    
    if (scriptEl.getAttribute("data-next-param")){
        query.push(["next-param",scriptEl.getAttribute("data-next-param")])   
    }

    if (query.length === 0){
        newIframe.setAttribute("src",resource('/include/#' + encodeURIComponent(document.location.href)));    
    }else{
        var assembly = query.map(function (x) {
            return x[0] + "=" + encodeURI(x[1]);
        }).reduce(function (x,y) {
            return x + "&" + y;
        });
        newIframe.setAttribute("src",resource('/include/?' + assembly + '#' + encodeURIComponent(document.location.href)));
    }
    
	function presentBar(){
		$_istBarraJQ("#ist-bar-iframe").show();
	}
	
	if ( window.addEventListener ) { 
	  newIframe.addEventListener( "load", presentBar, false );
	}
	else if ( window.attachEvent ) { 
	  newIframe.attachEvent( "onload", presentBar );
	}
	else {
	  newIframe.onload = presentBar;
	}

    container.appendChild(newIframe);
    XD.receiveMessage(resize, _server);
    referenceNode.parentNode.insertBefore(container, referenceNode.nextSibling);
})()
