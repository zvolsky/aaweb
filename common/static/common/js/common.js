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
