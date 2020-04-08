Tenant_Creating = function() {
    this.timer = null;
};

Tenant_Creating.prototype = {
    serve: function() {
        this.timer = setInterval(this.isSiteReady.bind(this), 10000);
    },
    
    isSiteReady: function() {
        function success(response) {
            if (response.ready) {
                clearInterval(this.timer);
                $('p#created').removeClass('d-none');
            }
        }
        let dataEl = $('p#created');
        let url = dataEl.data('isReadyUrl');
        let request = {'web': dataEl.data('web')};
        this.ajaxCall(url, request, success.bind(this));  // data-is-ready-url
    },

    ajaxCall: function(url, request, successFn) {
      $.ajax({
        url: url,
        data: request || {},
        dataType: 'json',
        success: successFn
      });
    },
};

tc = new Tenant_Creating();
tc.serve();
