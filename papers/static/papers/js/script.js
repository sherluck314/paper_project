$('.select-area li').click(function(e){
    var seli = $(this);
    if (seli.hasClass('before-select-li')){
        seli.removeClass('before-select-li');
        seli.addClass('after-select-li');
    }
    else if (seli.hasClass('after-select-li')){
        seli.removeClass('after-select-li');
        seli.addClass('before-select-li');
    }
});

$('.empty_button').click(function(e){
    var seli = $('.after-select-li');
    seli.removeClass('after-select-li');
    seli.addClass('before-select-li');
});

$('.condition_button').click(function(e){
    var seli = $('.after-select-li');
    var str_condition = "";
    var s_condition = "&";
    if ($(this).hasClass('or_button')){
        s_condition = '|';
    }
    if (seli.length === 0) {
        alert("请选择至少一个标签！")
    }
    else {
        for (var i = 0, len = seli.length; i < len; i++) {
            str_condition = str_condition+seli[i].firstElementChild.innerText+s_condition
        }
        if (seli.length > 1) {
            str_condition = str_condition.substr(0, str_condition.length-1)
        }
         $(location).attr("href",$('#bs-example-navbar-collapse-1 > ul > li:nth-child(2) > a')[0].href+"search/"+str_condition)
    }
});


( function( window ) {

'use strict';

// class helper functions from bonzo https://github.com/ded/bonzo

function classReg( className ) {
  return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
}

var hasClass, addClass, removeClass;

if ( 'classList' in document.documentElement ) {
  hasClass = function( elem, c ) {
    return elem.classList.contains( c );
  };
  addClass = function( elem, c ) {
    elem.classList.add( c );
  };
  removeClass = function( elem, c ) {
    elem.classList.remove( c );
  };
}
else {
  hasClass = function( elem, c ) {
    return classReg( c ).test( elem.className );
  };
  addClass = function( elem, c ) {
    if ( !hasClass( elem, c ) ) {
      elem.className = elem.className + ' ' + c;
    }
  };
  removeClass = function( elem, c ) {
    elem.className = elem.className.replace( classReg( c ), ' ' );
  };
}
})( window );

