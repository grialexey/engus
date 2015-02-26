$(document).ready(function() {
    var $cards = $('.card');
    if ($cards.length > 0) {
        $cards.each(function() {
            new Card($(this));
        });
    }
});