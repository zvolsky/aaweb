Common = function() {
};

Common.prototype = {
    ajaxCall: function(url, request, successFn) {
      $.ajax({
        url: url,
        data: request || {},
        dataType: 'json',
        success: successFn
      });
    }
};

// https://stackoverflow.com/questions/49541397/django-ajax-csrf-token-missing
/*
// CSRF_COOKIE_SECURE = True if https else False
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
    url: url,
    type: 'POST',
    headers:{
        "X-CSRFToken": csrftoken
    },
    data: data,
    cache: true,
});
*/

// ??? https://github.com/jpadilla/django-rest-framework-jwt/issues/45
