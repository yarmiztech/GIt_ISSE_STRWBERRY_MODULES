odoo.define("l10n_gcc_pos_inheriting.models", function (require) {
    "use strict";
    var models = require("point_of_sale.models");
    var utils = require("web.utils");
    var core = require("web.core");
    const {Gui} = require("point_of_sale.Gui");

    var _t = core._t;
    models.load_fields('product.product', 'ar_name');

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({

         initialize: function (attr, options) {
            this.ar_name = '';
            this.note = '';
            _super_orderline.initialize.apply(this, arguments);
        },
//        init_from_JSON: function (json) {
//            _super_orderline.init_from_JSON.apply(this, arguments);
//            if (json.ar_name) {
//                this.set_absolute_discount(json.ar_name);
//            }
//        },


//        initialize: function (attr, options) {
//            this.ar_name = false;
//            _super_orderline.initialize.apply(this, arguments);
//        },
        export_for_printing: function() {
        debugger;
            var line = _super_orderline.export_for_printing.apply(this,arguments);
            line.l10n_in_hsn_code = this.get_product().l10n_in_hsn_code;
            line.ar_name =this.product.ar_name
            line.note =this.note
//            var mou= this.enzapps_product_call(line)
            console.log(this,'line')
            return line;
        },
        enzapps_product_call: function(event){
             debugger;
             console.log(event,'event')
              var model = 'pos.order.line';
            var domain = [];
            var fields = [];
            self = this
            return this.pos.rpc({
                model: model,
                method: 'enzapps_product_call',
                args: [[this.product.id]]
            }).then(function (data) {
                debugger;
                var ar_name = data
                event.ar_name = ar_name
                if (document.getElementById("mou")) {
                document.getElementById("mou").innerText += data;
                return data
                }
            });
            },

});

});
