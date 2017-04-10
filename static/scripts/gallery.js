function showModal(url) {
    $.get(url, function( data ) {
      $( "body" ).append( data );
    });  
};

$(document).ready(function () {
 	var $grid = $('.gallery').masonry({
		itemSelector: 'a',
		columnWidth: 'a',
        fitWidth: true,
		percentPosition: true,
	});
	//	 layout Masonry after each image loads
	$grid.imagesLoaded().progress(function() {
		$grid.masonry('layout');
	});
    
    $(window).resize(function () {
        $grid.masonry('bindResize')
    });
});


//$(function() {
//    $("a").click(function() {
//        return someMethodName($(this).attr('href'));
//    });
//});
//
//function someMethodName(href)
//{
//    console.log(href);
//    return false;
//}