Tenant_Creating = function() {
    this.common = new Common();
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
        this.common.ajaxCall(url, request, success.bind(this));  // data-is-ready-url
    }
};

tc = new Tenant_Creating();
tc.serve();
