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


