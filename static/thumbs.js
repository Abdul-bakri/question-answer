$(window).on('load', function() {
    console.log('the page is loaded');
});
$('.widget.thumbs-up').on('click', function() {
    console.log('thumbs up was clicked');
    var state = $(this).attr('data-state');
    if (state == 'pending') {
        console.log('request in progress, dropping second click');
        return;
    }
    var checked  = state === 'checked';
    var nextState = checked ? 'unchecked' : 'checked';
    var elt = $(this);
    elt.attr('data-state', 'pending');
    $.ajax('/api/update-thumbs-up', {
        method: 'POST',
        data: {
            answer_id: $(this).attr('data-answer-id'),
            want_thumbs_up: !checked,
            _csrf_token: csrfToken
        },
        success: function(data) {
            console.log('post succeeded with result %s', data.result);
            elt.attr('data-state', nextState);
        },
        error: function() {
            console.error('post failed');
            elt.attr('data-state', state);
        }
    });
});


$('.widget.thumbs-down').on('click', function() {
    console.log('thumbs down was clicked');
    var state = $(this).attr('data-state');
    if (state == 'pending') {
        console.log('request in progress, dropping second click');
        return;
    }
    var checked  = state === 'checked';
    var nextState = checked ? 'unchecked' : 'checked';
    var elt = $(this);
    elt.attr('data-state', 'pending');
    $.ajax('/api/update-thumbs-down', {
        method: 'POST',
        data: {
            answer_id: $(this).attr('data-answer-id'),
            want_thumbs_down: !checked,
            _csrf_token: csrfToken
        },
        success: function(data) {
            console.log('post succeeded with result %s', data.result);
            elt.attr('data-state', nextState);
        },
        error: function() {
            console.error('post failed');
            elt.attr('data-state', state);
        }
    });
});