/*!
 * enquire.js v2.1.6 - Awesome Media Queries in JavaScript
 * Copyright (c) 2017 Nick Williams - http://wicky.nillia.ms/enquire.js
 * License: MIT */

!function(a){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=a();else if("function"==typeof define&&define.amd)define([],a);else{var b;b="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,b.enquire=a()}}(function(){return function a(b,c,d){function e(g,h){if(!c[g]){if(!b[g]){var i="function"==typeof require&&require;if(!h&&i)return i(g,!0);if(f)return f(g,!0);var j=new Error("Cannot find module '"+g+"'");throw j.code="MODULE_NOT_FOUND",j}var k=c[g]={exports:{}};b[g][0].call(k.exports,function(a){var c=b[g][1][a];return e(c?c:a)},k,k.exports,a,b,c,d)}return c[g].exports}for(var f="function"==typeof require&&require,g=0;g<d.length;g++)e(d[g]);return e}({1:[function(a,b,c){function d(a,b){this.query=a,this.isUnconditional=b,this.handlers=[],this.mql=window.matchMedia(a);var c=this;this.listener=function(a){c.mql=a.currentTarget||a,c.assess()},this.mql.addListener(this.listener)}var e=a(3),f=a(4).each;d.prototype={constuctor:d,addHandler:function(a){var b=new e(a);this.handlers.push(b),this.matches()&&b.on()},removeHandler:function(a){var b=this.handlers;f(b,function(c,d){if(c.equals(a))return c.destroy(),!b.splice(d,1)})},matches:function(){return this.mql.matches||this.isUnconditional},clear:function(){f(this.handlers,function(a){a.destroy()}),this.mql.removeListener(this.listener),this.handlers.length=0},assess:function(){var a=this.matches()?"on":"off";f(this.handlers,function(b){b[a]()})}},b.exports=d},{3:3,4:4}],2:[function(a,b,c){function d(){if(!window.matchMedia)throw new Error("matchMedia not present, legacy browsers require a polyfill");this.queries={},this.browserIsIncapable=!window.matchMedia("only all").matches}var e=a(1),f=a(4),g=f.each,h=f.isFunction,i=f.isArray;d.prototype={constructor:d,register:function(a,b,c){var d=this.queries,f=c&&this.browserIsIncapable;return d[a]||(d[a]=new e(a,f)),h(b)&&(b={match:b}),i(b)||(b=[b]),g(b,function(b){h(b)&&(b={match:b}),d[a].addHandler(b)}),this},unregister:function(a,b){var c=this.queries[a];return c&&(b?c.removeHandler(b):(c.clear(),delete this.queries[a])),this}},b.exports=d},{1:1,4:4}],3:[function(a,b,c){function d(a){this.options=a,!a.deferSetup&&this.setup()}d.prototype={constructor:d,setup:function(){this.options.setup&&this.options.setup(),this.initialised=!0},on:function(){!this.initialised&&this.setup(),this.options.match&&this.options.match()},off:function(){this.options.unmatch&&this.options.unmatch()},destroy:function(){this.options.destroy?this.options.destroy():this.off()},equals:function(a){return this.options===a||this.options.match===a}},b.exports=d},{}],4:[function(a,b,c){function d(a,b){var c=0,d=a.length;for(c;c<d&&b(a[c],c)!==!1;c++);}function e(a){return"[object Array]"===Object.prototype.toString.apply(a)}function f(a){return"function"==typeof a}b.exports={isFunction:f,isArray:e,each:d}},{}],5:[function(a,b,c){var d=a(2);b.exports=new d},{2:2}]},{},[5])(5)});

/*!
 * savvior v0.5.2 - A Javascript multicolumn layout tool alternative to Masonry or Salvattore.
 * http://savvior.org
 * 
 */
!function(a,b){"function"==typeof define&&define.amd?define("savvior",["enquire"],function(c){return a["new GridDispatch()"]=b(c)}):"object"==typeof exports?module.exports=b(require("enquire.js")):a.savvior=b(a.enquire)}(this,function(a){function b(a,b,c,d){d||!a.dataset?a.setAttribute("data-"+b,c):a.dataset[b]=c}function c(a,b,c){var d=0;for(d;d<a.length&&b.call(c,a[d],d)!==!1;d++);}function d(a){return"function"==typeof a}function e(a,b){for(b in a)return!1;return!0}function f(a,b){for(var c in a)b[c]=a[c];return b}"function"!=typeof window.CustomEvent&&function(){function a(a,b){b=b||{bubbles:!1,cancelable:!1,detail:void 0};var c=document.createEvent("CustomEvent");return c.initCustomEvent(a,b.bubbles,b.cancelable,b.detail),c}window.CustomEvent=a,a.prototype=window.CustomEvent.prototype}(),function(){for(var a=0,b=["ms","moz","webkit","o"],c=0;c<b.length&&!window.requestAnimationFrame;++c)window.requestAnimationFrame=window[b[c]+"RequestAnimationFrame"],window.cancelAnimationFrame=window[b[c]+"CancelAnimationFrame"]||window[b[c]+"CancelRequestAnimationFrame"];window.requestAnimationFrame||(window.requestAnimationFrame=function(b,c){var d=(new Date).getTime(),e=Math.max(0,16-(d-a)),f=window.setTimeout(function(){b(d+e)},e);return a=d+e,f}),window.cancelAnimationFrame||(window.cancelAnimationFrame=function(a){clearTimeout(a)})}();var g=function(a){this.columns=null,this.element=a,this.filtered=document.createDocumentFragment(),this.status=!1,this.columnClasses=null};g.prototype.setup=function(a,c){if(this.status)return!1;var e=document.createRange(),f=document.createElement("div");e.selectNodeContents(this.element),f.appendChild(e.extractContents()),window.requestAnimationFrame(function(){b(f,"columns",0),this.addColumns(f,a),this.status=!0,d(c)&&c.call(this)}.bind(this))},g.prototype.addColumns=function(a,d){var e,f,g,h=d.columnClasses||["column","size-1of"+d.columns],i=document.createDocumentFragment(),j=[],k=d.columns;for(this.filterItems(a,d.filter),h=Array.isArray(h)?h.join(" "):h;0!=k--;)e="[data-columns] > *:nth-child("+d.columns+"n-"+k+")",j.push(a.querySelectorAll(e));c(j,function(a){f=document.createElement("div"),g=document.createDocumentFragment(),f.className=h,c(a,function(a){g.appendChild(a)}),f.appendChild(g),i.appendChild(f)}),this.element.appendChild(i),b(this.element,"columns",d.columns),this.columns=d.columns,this.columnClasses=d.columnClasses},g.prototype.filterItems=function(a,d){if(!d)return a;var e,f,g;return g=Array.prototype.slice.call(a.children),f=a.querySelectorAll("[data-columns] > "+d),c(f,function(a){e=g.indexOf(a),this.filtered.appendChild(a),b(a,"position",e)},this),a},g.prototype.removeColumns=function(){var a,d=document.createRange(),e=document.createElement("div"),f=[];return d.selectNodeContents(this.element),a=Array.prototype.filter.call(d.extractContents().childNodes,function(a){return a instanceof window.HTMLElement}),f.length=a[0].childNodes.length*a.length,c(a,function(b,d){c(b.children,function(b,c){f[c*a.length+d]=b})}),b(e,"columns",0),f.filter(function(a){return!!a}).forEach(function(a){e.appendChild(a)}),e},g.prototype.redraw=function(a,b){var c,e=new CustomEvent("savvior:redraw",{detail:{element:this.element,from:this.columns,to:a.columns,filter:a.filter||null}});window.requestAnimationFrame(function(){this.columns!==a.columns&&(c=this.restoreFiltered(this.removeColumns()),this.addColumns(c,a)),window.dispatchEvent(e),d(b)&&b(this)}.bind(this))},g.prototype.restoreFiltered=function(a){if(0===this.filtered.childNodes.length)return a;var b,d=a;return c(this.filtered.querySelectorAll("[data-position]"),function(a){b=Number(a.getAttribute("data-position")),a.removeAttribute("data-position"),d.insertBefore(a,d.children[b]||null)}),a},g.prototype.restore=function(a,b){if(!this.status)return d(a)&&a(!1),!1;var e,f=document.createDocumentFragment(),g=[],h=new CustomEvent("savvior:restore",{detail:{element:this.element,from:this.columns}});window.requestAnimationFrame(function(){e=this.restoreFiltered(this.removeColumns()),c(e.childNodes,function(a){g.push(a)}),g.forEach(function(a){f.appendChild(a)}),this.element.appendChild(f),this.element.removeAttribute("data-columns"),window.dispatchEvent(h),d(a)&&a.call(b,b||this)}.bind(this))},g.prototype.addItems=function(a,b,e){var f=new CustomEvent("savvior:addItems",{detail:{element:this.element,grid:this}}),g=function(a){return b.clone?a.cloneNode(!0):a},h={append:function(a,b){var c=g(a);return b.appendChild(c),b},prepend:function(a,b){var c=g(a);return b.insertBefore(c,b.firstChild),b}};window.requestAnimationFrame(function(){var g=this.restoreFiltered(this.removeColumns());a instanceof NodeList||a instanceof Array?c(a,function(a){g=h[b.method].call(null,a,g)}):g=h[b.method].call(null,a,g),this.addColumns(g,{columns:this.columns,columnClasses:this.columnClasses,filter:this.filter}),window.dispatchEvent(f),d(e)&&e(this)}.bind(this))};var h=function(a,b){this.selector=a,this.options=b,this.queryHandlers=[],this.grids=[],this.ready=!1};h.prototype.register=function(){c(document.querySelectorAll(this.selector),function(a){this.grids.push(new g(a,this.options))},this);for(var b in this.options)this.queryHandlers.push(this.constructHandler(b,this.options[b]));return c(this.queryHandlers,function(b){a.register(b.mq,b.handler)}),this.ready=!0,this},h.prototype.constructHandler=function(a){return{mq:a,handler:{deferSetup:!0,setup:function(){this.gridSetup(a)}.bind(this),match:function(){this.gridMatch(a)}.bind(this),destroy:function(){}}}},h.prototype.gridSetup=function(a){var b;c(this.grids,function(c){c.setup(this.options[a],function(){b=new CustomEvent("savvior:setup",{detail:{element:c.element,columns:c.columns,filter:this.filter}}),window.dispatchEvent(b)})},this)},h.prototype.gridMatch=function(a){var b;c(this.grids,function(c){b=new CustomEvent("savvior:match",{detail:{element:c.element,from:c.columns,to:this.options[a].columns,query:a}}),c.redraw(this.options[a],function(){window.dispatchEvent(b)})},this)},h.prototype.unregister=function(b,e){c(this.queryHandlers,function(b){a.unregister(b.mq)}),c(this.grids,function(a){a.restore(function(){this.queryHandlers=[],this.ready=!1,d(b)&&b.call(this,e||this)},this)},this),this.grids=[]};var i=function(){if(!a)throw new Error("enquire.js not present, please load it before calling any methods");this.grids={}};return i.prototype.init=function(a,b){if(!a)throw new TypeError("Missing selector");if("string"!=typeof a)throw new TypeError("Selector must be a string");if("object"!=typeof b)throw new TypeError("Options must be an object");return this.grids[a]?this:document.querySelectorAll(a).length<1?this:(this.grids[a]=new h(a,b),this.grids[a].register(b),window.dispatchEvent(new CustomEvent("savvior:init")),this)},i.prototype.destroy=function(a,b){var f=new CustomEvent("savvior:destroy",{detail:{selectors:a}}),g=void 0===a||e(a)?Object.keys(this.grids):a,h=g.length,i=0,j=function(a){delete this.grids[g[i]],++i===h&&(window.dispatchEvent(f),d(b)&&b.call(a,this))}.bind(this);c(g,function(a){this.grids[a]&&this.grids[a].unregister(j)},this)},i.prototype.ready=function(a){if(void 0===a){var b=[];for(var c in this.grids)this.grids[c].ready&&b.push(c);return b.length>0&&b}return!!this.grids[a]&&this.grids[a].ready},i.prototype.addItems=function(a,b,e,g){var h,i,j={clone:!1,method:"append"};if(!this.grids[a])throw new TypeError("Grid does not exist.");if("string"==typeof b&&(b=document.querySelectorAll(b)),b instanceof Array)c(b,function(a){if(!(a instanceof Node))throw new TypeError("Supplied element in array is not instance of Node.")},this);else if(!(b instanceof Node||b instanceof NodeList))throw new TypeError("Supplied argument is not a Node or a NodeList.");return d(e)?(h=e,i=j):(h=g,i=f(e,j)),c(this.grids[a].grids,function(a){a.addItems(b,i,h)}),this},new i});

var allowModal = true; //Prevents double loads

function showModal(url) {
    if (allowModal) {
        allowModal = false
        var request = new XMLHttpRequest();
        request.open('GET', url);

        request.onload = function () {
            if (request.status == 200) {
                document.body.innerHTML += request.responseText;
            }
        }

        request.send();
        
    }

}


function toggle(){
  document.getElementById("modal").classList.toggle('showSide');
}

savvior.init('.gallery', {
  "screen and (max-width: 420px)": { columns: 2 },
  "screen and (min-width: 420px) and (max-width: 950px)": { columns: 3 },
  "screen and (min-width: 950px)": { columns: 4 },
});
