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

jQuery.extend({
    stringify  : function stringify(obj) {

        if ("JSON" in window) {
            return JSON.stringify(obj);
        }

        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string") obj = '"' + obj + '"';

            return String(obj);
        } else {
            // recurse array or object
            var n, v, json = [], arr = (obj && obj.constructor == Array);

            for (n in obj) {
                v = obj[n];
                t = typeof(v);
                if (obj.hasOwnProperty(n)) {
                    if (t == "string") {
                        v = '"' + v + '"';
                    } else if (t == "object" && v !== null){
                        v = jQuery.stringify(v);
                    }

                    json.push((arr ? "" : '"' + n + '":') + String(v));
                }
            }

            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    }
});

var barClosed = true;
function toogleBar(){
    if (barClosed){
        jQuery("#bar-open").removeClass("hidden");
		//window.parent.postMessage('resize','*')
		var parent_url = decodeURIComponent(document.location.hash.replace(/^#/, ''));
		XD.postMessage("resize",parent_url,window.parent)
        barClosed = false
    }else{
        setTimeout(function() { jQuery("#bar-open").addClass("hidden") }, 350);
		//window.parent.postMessage('resize','*')
	    var parent_url = decodeURIComponent(document.location.hash.replace(/^#/, ''));
        XD.postMessage("resize",parent_url,window.parent)
        barClosed = true
    }
    return false;
}

var editClosed = true;
var quickOffset = 0;
var editOffset = 0;
jQuery(document).ready(function(){
    var wdw = jQuery(window).width()
    var node = jQuery("#edit-quick-access");
    if (node.length){
        var edit = node.width()
        editOffset = ((wdw / 2) + edit)
        node.offset({left: node.offset().left + editOffset })
        node.hide()
        var lines = jQuery("ul#edit-url-list li form");
        for(var i=0; i < lines.length; i++){
            (function(){
                var el = lines[i];
                var inputs = jQuery("input[type=text]", el);
                var fn = function () {
                    jQuery("input[type=checkbox]", el).prop("checked",true);
                }
                jQuery(inputs).keypress(fn);
            })()
        }
    }
    jQuery("a[to]").click(function(i) { jumpTo(jQuery(this).attr('to'));return false; })
    jQuery("#edit-url-list").sortable({ 
        handle : '.move'
    });
    jQuery("#login-btn").click(function () {
        auth("/login?next=");
        return false;
    });
    jQuery("#logout-btn").click(function () {
		if (jQuery("meta[name='debug']").attr("content")) {
			auth("/logout?next=");
		} else {
			jQuery.get("https://barra.ist.utl.pt/logout",function(){
				var logoutURL = queryParam("logout")
				if(logoutURL) {
					jumpTo(logoutURL);
				} else {
					jumpTo("https://id.ist.utl.pt/cas/logout");
				}
			})
		}
		return false;
    })
})

function queryParam(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function auth(url){
    var remoteLogin = queryParam("login");
    var remoteNextParam = queryParam("next-param");
    var parent_url = decodeURIComponent(document.location.hash.replace(/^#/, ''));

    if (remoteLogin){
        var uri = Uri(remoteLogin);
        if (remoteNextParam){
            uri.addQueryParam(remoteNextParam,parent_url);
        }
        parent_url = uri.toString();
    }
    XD.postMessage('auth:' + url + encodeURIComponent(parent_url), decodeURIComponent(document.location.hash.replace(/^#/, '')),window.parent)
}

function jumpTo(url){
    if (url.match("https?://") || url.match("mailto:")){
        window.parent.postMessage('link:' + url,'*')
    }else{
        if(url[0] == "/"){
	    var parent_url = decodeURIComponent(document.location.hash.replace(/^#/, ''));
	    XD.postMessage('link:'+ window.location.origin + url,parent_url,window.parent)
		//            window.parent.postMessage('link:'+ window.location.origin + url,'*')
        }else{
	    var parent_url = decodeURIComponent(document.location.hash.replace(/^#/, ''));
            XD.postMessage('link:' + window.location.href + url,parent_url,window.parent)
	    //            window.parent.postMessage('link:' + window.location.href + url,'*')
        }
    }
}

function toogleEdit(){
    var node = jQuery("#ist-network-menu");
    var editNode = jQuery("#edit-quick-access");
    var wdw = jQuery(window).width()
    var menu = node.width()
    if (editClosed){
        quickOffset = ((wdw / 2) + menu)
        node.animate({
            left: "-=" + quickOffset
        },1000,function(){ node.hide() })
        node.css("top", "-395px")
        editNode.show()
        editNode.animate({
            left: "-=" + editOffset
        },1000, null ,function(){
            jQuery(".tooltip").fadeIn(650).delay(2000).fadeOut(650)
        })
        
        editClosed = false;
    } else {
        node.show()
        node.animate({
            left: "+=" + quickOffset
        },1000)
        editOffset = ((wdw / 2) + menu)
        editNode.animate({
            left: "+=" + editOffset
        },1000,function(){
            node.css("top", "0px");
            editNode.hide()
            jQuery(".tooltip").hide()
        })
        editClosed = true;
    }
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function isValid (domains, uri) {
    if (uri == ""){return true}
    var uri = new Uri(uri);
    if (!uri.host() || uri.host() == ""){
        return false;
    }
    for (var i = 0; i < domains.length; i++) {
        var domain = domains[i];
        if (endsWith(uri.host(),domain)) {
            return true;
        }
    };
    return false;
}

function saveEditedLinks(){
    var it = jQuery("ul#edit-url-list li form");
    var domains = jQuery("meta[name='domains']").attr("content").split(",")
    var result = []
    for(var i=0; i < it.length; i++){
        var el = it[i];
        var link = jQuery("#link", el).val()
        var uri = new Uri(link);
        
        if (!isValid(domains,link)){
            alert("Esse link é invalido. Usar apenas do dominios " + jQuery("meta[name='domains']").attr("content"));
            return;
        }

        var strct = {
            order: i,
            name: jQuery("#name", el).val(),
            link: jQuery("#link", el).val(),
            active: jQuery("#btn", el).is(':checked')
        }
        result[i] = strct;
    }



    jQuery.ajax({
        type:"POST",
        url:"/saveLinks/",
        data: { links : jQuery.stringify(result), csrfmiddlewaretoken: csrf },
        success: function() {
            jQuery('#center-list').html("")
            for(var i=0; i < result.length; i++){
                el = result[i]
                if (el['active'] && el['name'].length && el['link'].length){
                    jQuery('#center-list').append("<li><a href=\"#\" to=\"" + el['link']+ "\" title=\"" + el['name']+ "\">" + el['name']+ "</a></li>")
                }
            }
            jQuery("a[to]",jQuery('#center-list')).click(function(i) { jumpTo(jQuery(this).attr('to')) })
            toogleEdit()
        }
    })
}
