Tenant_Creating = function() {
};

Tenant_Creating.prototype = {
    ajaxUrl: $('p#created').data;  // data-is-ready-url
    serve: function() {
        debugger;
    },
    
    isSiteReady: function() {
      $.ajax({
        url: '/ajax/is_site_ready/',
        //data: {
        //  'username': username
        //},
        dataType: 'json',
        success: (function (data) {
          if (data.is_ready) {
            this.onReady();
          }
        }).bind(this);
      });
    },
    
    onReady: function() {

    }
};
debugger;
tc = new Tenant_Creating();
tc.serve();
