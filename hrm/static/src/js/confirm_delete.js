<template id="assets_backend" name="HRM Assets" inherit_id="web.assets_backend">
    <xpath expr="." position="inside">
        <script type="text/javascript">
            odoo.define('hrm.confirm_delete_department', function (require) {
                "use strict";

                var core = require('web.core');
                var _t = core._t;
                var Dialog = require('web.Dialog');

                var ListView = require('web.ListView');

                ListView.include({
                    render_buttons: function() {
                        var self = this;
                        this._super.apply(this, arguments);

                        if (this.$buttons) {
                            this.$buttons.on('click', '.o_list_button_delete', function () {
                                var record_ids = self.getSelectedIds();
                                if (record_ids.length) {
                                    Dialog.confirm(self, _t("Nếu bạn xóa hệ thống/ công ty hoặc phòng ban này sẽ bị xóa bên hồ sơ nhân sự, bạn có chắc chắn?"), {
                                        confirm_callback: function () {
                                            self.do_delete();
                                        },
                                    });
                                } else {
                                    Dialog.alert(self, _t("Please select a record to delete."));
                                }
                            });
                        }
                    },
                });
            });
        </script>
    </xpath>
</template>
