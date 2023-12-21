odoo.define('datn_ky_so.kyso', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var BasicController = require('web.BasicController');
    var FormRenderer = require('web.FormRenderer');
    var basic_fields = require('web.basic_fields');
    var FieldBinaryFile = basic_fields.FieldBinaryFile;
    var FieldBinaryImage = basic_fields.FieldBinaryImage;
    var _t = core._t;
    var vnptPlugin;
    var serialNumber;
    var subjectCN;
    var timer = null;
    var DocumentViewer = require('mail.DocumentViewer');
    var framework = require('web.framework');
    var Context = require('web.Context');
    var pyUtils = require('web.py_utils');
    var ListRenderer = require('web.ListRenderer');
    var qweb = core.qweb;

    function hide_popup_kyso(){
        $("#thongtin_kyso_dialog").attr("aria-hidden", "true").css("display", "none").removeClass('show').addClass('hide');
        $('button[disabled="disabled"]').removeAttr("disabled");
    }

    function edit_form_preview_signed_file(){
        $('.modal-dialog').addClass('modal-dialog-preview_kyso');
        $('.modal-content').addClass('modal-content-preview_kyso');
        $('.modal-header').addClass('modal-header-preview_kyso');
        $('.modal-footer').addClass('modal-footer-preview_kyso');
        $('.modal-backdrop').removeClass('show');
        $('.modal-backdrop').removeClass('modal-backdrop');
        // nếu nhãn "Đã ký số" đang ẩn thì hiển thị lên
        if ($('.signed').hasClass('o_invisible_modifier')){
            $('.check_signed').toggleClass('o_invisible_modifier');
        }
    }

    function add_mask_thongbao (message) {
        $('body').append('<div class="ca_mask" style="z-index: 1100; border: none; margin: 0px; padding: 0px; width: 100%; height: 100%; top: 0px; left: 0px; background-color: rgb(0, 0, 0); opacity: 0.6; cursor: wait; position: fixed;"></div>' +
            '<div class="ca_mask" style="z-index: 1111; position: fixed; padding: 0px; margin: 0px; width: 30%; top: 40%; left: 35%; text-align: center; color: rgb(0, 0, 0); border: 0px; cursor: wait;">' +
                '<div style="background-color: transparent;"><div>' +
            '        <div class="" style="height: 50px">' +
            '            <img alt="Đang nạp..." src="/web/static/src/img/spin.png" style="animation: fa-spin 1s infinite steps(12);">' +
            '        </div>' +
            '        <br>' +
            '        <div class="oe_throbber_message" style="color:white">' + message + '</div>' +
            '        </div>' +
                '</div>' +
            '</div>'
            );
    }

    function remove_mask_thongbao () {
        $('.ca_mask').remove();
    }

    function chuyen_trangthai_sauduyet(){
        $('.o_statusbar_buttons button').css('display', 'None');
        $('.o_statusbar_status .btn-primary').removeClass('btn-primary').addClass('btn-secondary');
        $('[data-value="confirmed"]').addClass('btn-primary');
    }

    function get_info_cts_from_token(self, key, rec_ids, is_next_default, loai_ky) {
        // check plugin
        add_mask_thongbao('Đang kiểm tra Plugin');
        vnpt_plugin.checkPlugin().then(function (data) {
            remove_mask_thongbao();
            if (data === "1") {
                vnpt_plugin.getVersion().then(function (data) {
                    if (data !== '1.0.4.3'){
                        remove_mask_thongbao();
                        show_view_tai_plugin(self);
                        return;
                    }
                    clearTimeout(timer); // clear
                    vnpt_plugin.setLicenseKey(key).then(function (data) {
                        if (data.split(":").length > 1 && data.split(":")[1][0] !== '1'){
                            remove_mask_thongbao();
                            alert("Lincense Plugin không hợp lệ hoặc đã hết hạn");
                            return;
                        }
                        add_mask_thongbao('Đã gửi yêu cầu chọn chứng thư.<br/>Vui lòng chọn các chứng thư có sẵn');
                        var isOnlyFromToken = (loai_ky === 'dongbo_1_hoso' || loai_ky === 'dongbo_nhieu_hoso') ? true : false;
                        vnpt_plugin.getCertInfo(null, isOnlyFromToken).then(function (data) {
                            remove_mask_thongbao();
                            if (data === "" || data === null) {
                                alert("Không lấy được thông tin chứng thư số");
                                return;
                            }
                            var jsOb = JSON.parse(data);
                            if (jsOb !== "" || jsOb != null) {
                                serialNumber = jsOb.serial;
                                subjectCN = jsOb.subjectCN;
                                let dateTime = null;
                                let ocspUrl = null;
                                let certBase64 = jsOb.base64;
                                if (certBase64 === null || certBase64.length === 0) {
                                    alert("Không lấy được chuỗi base64 của chứng thư số");
                                    return;
                                }
                                vnpt_plugin.ValidateCertificateBase64(certBase64, dateTime, ocspUrl).then(function (data) {
                                    if (Number(data) === 0) {
                                        if (loai_ky === 'duyet_1_hoso' || loai_ky === 'duyet_nhieu_hoso'){
                                            add_mask_thongbao('Đang phê duyệt hồ sơ');
                                            self._rpc({
                                                model: 'vnpt.hr.employee.edition',
                                                method: 'complete_kyso_duyet',
                                                args: [jsOb, rec_ids, is_next_default, 'token', loai_ky],
                                            }).then(function (result) {
                                                remove_mask_thongbao();
                                                if (result.success){
                                                    self.do_notify('Ký số trên dữ liệu thành công!');
                                                    if (loai_ky === 'duyet_1_hoso'){
                                                        chuyen_trangthai_sauduyet(self, result);
                                                    }
                                                    self.do_action(result.action);
                                                }else{
                                                    show_view_error(self, result.message, result.view_id);
                                                }
                                            });

                                            setTimeout(function () {
                                                $('.blockOverlay').css('display', 'None');
                                                $('.blockMsg').css('display', 'None');
                                            }, 3000);
                                        } else if (loai_ky === 'dongbo_1_hoso' || loai_ky === 'dongbo_nhieu_hoso'){
                                            var dataJS = {};

                                            var arrData = [];
                                            // 1
                                            var option = {
                                                DigestAlgorithm: 'SHA256',
                                                encoding: 'utf8',
                                                detached: true,
                                            };
                                            dataJS.type = 'hash';
                                            dataJS.sigOptions = JSON.stringify(option);
                                            var jsData = "";

                                            for (let i = 0; i < rec_ids.length; i ++){
                                                dataJS.data = rec_ids[i].hash_string;
                                                // dataJS.data = 'xo/IX7Y+rQEMtKxiHxf5GuaS5V8dOJ7R4RwEPbtGV9U=';
                                                jsData = JSON.stringify(dataJS);
                                                arrData.push(jsData);
                                            }
                                            var serial;
                                            if (serialNumber == null || serialNumber == ""){
                                                serial = "";
                                            }else{
                                                serial = serialNumber;
                                            }
                                            add_mask_thongbao('Đang thực hiện ký số');
                                            vnpt_plugin.signArrDataAdvanced(arrData, serial, false).then(function (data) {
                                                remove_mask_thongbao();
                                                complete_kyso_dongbo(self, jsOb, rec_ids, data, certBase64, loai_ky);
                                            }).catch(function (e) {
                                                alert(e);
                                             });
                                        }
                                    } else {
                                        let err = parse_error_cts(data);
                                        framework.unblockUI();
                                        alert(err);
                                    }
                                }).catch(function (e) {
                                    framework.unblockUI();
                                    alert(e);
                                });
                            }
                        }).catch(function (e) {
                            framework.unblockUI();
                            alert(e);
                        });
                    }).catch(function (e) {
                        console.log(e)
                    });
                });
            } else {
                remove_mask_thongbao();
                timer = setTimeout(checkPlugin, 1500);
            }
            return true;
        }).catch(function (e) {
            remove_mask_thongbao();
            show_view_tai_plugin(self);
        });
    }

    function show_view_tai_plugin(self){
        framework.unblockUI();
        self._rpc({
            model: 'temp_model_kyso',
            method: 'get_view_tai_plugin',
        }).then(function (data) {
            self.do_action(data);
        });
    }

    function show_view_error(self, message, view_id){
        self.do_action({
            name: 'Thông báo',
            type: 'ir.actions.act_window',
            view_type: 'form',
            view_mode: 'form',
            res_model: 'temp_model_kyso',
            context: {
                'default_name': message,
            },
            views: [[view_id, 'form']],
            target: 'new'
        });
    }


    function parse_error_cts (data) {
        let err;
        switch (Number(data)) {
            case 0:
                err = "Chứng thư số hợp lệ";
                break;
            case 1:
                err = "Lỗi không xác định";
                break;
            case 2:
                err = "Chứng thư số hết hạn";
                break;
            case 3:
                err = "Chứng thư số chưa đến hạn";
                break;
            case 4:
                err = "Chứng thư số đã bị thu hồi";
                break;
            case 5:
                err = "Chứng thư số không có quyền ký dữ liệu";
                break;
            case 6:
                err = "Kiểm tra trạng thái thu hồi của chứng thư không thành công";
                break;
            case 7:
                err = "Chứng thư số không được cấp bới CA tin tưởng";
                break;
            case 8:
                err = "Không lấy được thông tin chứng thư số";
                break;
            case 9:
                err = "Không lấy được thông tin chứng thư số CA";
                break;
            case 10:
                err = "Không lấy được thông tin chứng thư số CA";
                break;
            default:
                err = "Lỗi không xác định";
                break;
        }
        return err;
    }

    FieldBinaryImage.include({
        init: function (parent, name, record) {
            this._super.apply(this, arguments);
            if (this.model === 'res.users' && this.name === 'chu_ky') {
                this.placeholder = '/datn_ky_so/static/src/img/upload_icon.png'
            }
        }
    });

    BasicController.include({
        // Todo: Thay đổi câu thông báo khi discard chỉnh sửa
        // Todo: Tắt luôn popup khi bấm hủy (ko sửa j) ở màn hình tùy chỉnh cá nhân
        _discardChanges: function (recordID, options) {
            var self = this;
            recordID = recordID || this.handle;
            return this.canBeDiscarded(recordID).then(function (needDiscard) {
                if (self.displayName === 'Thay đổi tùy chỉnh cá nhân') {
                    let close_btn = $('[data-dismiss="modal"]');
                    if (close_btn && close_btn.length > 0) {
                        close_btn.click();
                        return;
                    }
                }
                if (options && options.readonlyIfRealDiscard && !needDiscard) {
                    return;
                }
                self.model.discardChanges(recordID);
                if (self.model.canBeAbandoned(recordID)) {
                    self._abandonRecord(recordID);
                    return;
                }
                return self._confirmSave(recordID);
            });
        },
    });

    FormRenderer.include({
        _renderHeaderButton: function (node) {
            var self = this;
            var $result = this._super.apply(this, arguments);
            if (self.state.model === 'datn.kyso.file') {
                if (node.attrs.name === 'action_kyso_canhan') {
                    $result.on('click', function () {
                        let field_not_valid = self.canBeSaved(self.state.id);
                        if (field_not_valid.length === 0) {
                            self.check_kyso_gui_xn('action_kyso_canhan');
                        }
                    });
                }
                if (node.attrs.name === 'action_kyso_kynhay') {
                    $result.on('click', function () {
                        let field_not_valid = self.canBeSaved(self.state.id);
                        if (field_not_valid.length === 0) {
                            self.check_kyso_gui_xn('action_kyso_kynhay');
                        }
                    });
                }
                if (node.attrs.name === 'action_kyso_coquan') {
                    $result.on('click', function () {
                        let field_not_valid = self.canBeSaved(self.state.id);
                        if (field_not_valid.length === 0) {
                            self.check_kyso_gui_xn('action_kyso_coquan');
                        }
                    });
                }
                if (node.attrs.name === 'action_kyso_dau_coquan') {
                    $result.on('click', function () {
                        let field_not_valid = self.canBeSaved(self.state.id);
                        if (field_not_valid.length === 0) {
                            self.check_kyso_gui_xn('action_kyso_dau_coquan');
                        }
                    });
                }

            }
            return $result;

        },
        signAdvanceView: function (edition_id, _2c_base64, chu_ky, signature) {
            var self = this;
            vnpt_plugin.getCertInfo().then(function (data) {
                remove_mask_thongbao();
                framework.unblockUI();
                if (data === "" || data === null) {
                    alert("Không lấy được thông tin chứng thư số");
                    return;
                }
                var jsOb = JSON.parse(data);
                if (jsOb !== "" || jsOb != null) {
                    serialNumber = jsOb.serial;
                    subjectCN = jsOb.subjectCN;
                    let dateTime = null;
                    let ocspUrl = null;
                    let certBase64 = jsOb.base64;
                    if (jsOb.code === -1) {
                        alert("Key Plugin không hợp lệ");
                        return;
                    }
                    if (certBase64 === null || certBase64.length === 0) {
                        alert("Không lấy được chuỗi base64 của chứng thư số");
                        return;
                    }
                    add_mask_thongbao('Đang kiểm tra thông tin chứng thư');
                    vnpt_plugin.ValidateCertificateBase64(certBase64, dateTime, ocspUrl).then(function (data) {
                        remove_mask_thongbao();
                        if (Number(data) === 0) {
                            self.initSignPage(edition_id, _2c_base64, chu_ky, 'token', signature);
                        } else {
                            let err = parse_error_cts(data);
                            alert(err);
                        }
                    }).catch(function (e) {
                        remove_mask_thongbao();
                        alert(e);
                    });
                }
            }).catch(function (e) {
                remove_mask_thongbao();
                alert(e);
            });
        },
        initSignPage: function (edition_id, _2c_base64, chu_ky, hinhthuc_kyso, signature) {
            var self = this;
            let options = {
                Callback: function (getPdfSignatureOptions) {
                    self.SignAdvanced(edition_id, _2c_base64, 'pdf', getPdfSignatureOptions, hinhthuc_kyso)
                },//this.sign.bind(this), // Hàm callback khi chọn ký dữ liệu
                comments: [],
                signatures: signature,
                visibleType: 1, // 0=text_only, 1=text_and_left_image, 2=image_only,
                fontStyle: 0, // 0=normal, 1=bold, 2=italic, 3=bold-italic,
                fontColor: '0000ff', // Màu chữ trên chữ ký, comment
                fontSize: 8, // Fontsize nội dung text trên chữ ký, comment
                signatureImg: chu_ky,
                visibleText: 'Ký bởi:____________\nNgày ký: ' + self.getCurrentDate(),
            };
            vnptPlugin = $('#pdf-advanced').vnptpdf(options);
            vnptPlugin.initDataBase64(_2c_base64);
            vnptPlugin.start();
            setTimeout(function () {
                $('.o_dialog_error').parent().find('[data-dismiss="modal"]').click();
                $('#pdf-cancel').on('click', function (e) {
                    framework.unblockUI();
                });
                var offset = $("#signature_").offset();
                if (offset) {
                    $('.pdf-working-area').animate({
                        scrollTop: offset.top - 300,
                        scrollLeft: offset.left
                    }, 10);
                }
            }, 2000);
        },
        SignAdvanced: function (edition_id, data, type, option, hinhthuc_kyso) {
            var self = this;
            switch (hinhthuc_kyso) {
                case 'token':
                    var dataJS = {};
                    var arrData = [];
                    // 1
                    dataJS.data = data;
                    dataJS.type = type;
                    option.SigSigningTimeVisible = true;
                    option.SigningTime = self.getCurrentDate();
                    option.SigColorRGB = '0,0,255';
                    option.SigEmailVisible = false;
                    option.SigCompanyVisible = false;
                    option.SigPositionVisible = false;
                    dataJS.sigOptions = JSON.stringify(option);

                    var jsData = "";
                    jsData += JSON.stringify(dataJS);
                    //
                    arrData.push(jsData);
                    var serial;
                    if (serialNumber == null || serialNumber == "") {
                        serial = "";
                    } else {
                        serial = serialNumber;
                    }
                    framework.blockUI();

                    vnpt_plugin.signArrDataAdvanced(arrData, serial, false).then(function (data) {
                        if (data === '-1') {
                            framework.unblockUI();
                            alert('Ký lỗi')
                        } else if (JSON.parse(JSON.parse(data)[0]).error !== '') {
                            framework.unblockUI();
                        } else {
                            let _base64_daky = JSON.parse(JSON.parse(data)[0]).data;
                            self.complete_kyso(_base64_daky, edition_id);
                        }
                    }).catch(function (e) {
                        alert(e);
                    });
                    break;
                case 'smart_ca':
                    framework.blockUI();
                    self._rpc({
                        model: 'vnpt.hr.employee.edition',
                        method: 'action_kyso_smart_ca',
                        args: [edition_id, data, option],
                    }).then(function (result) {
                        remove_mask_thongbao();
                        if (result.success === true) {
                            self.do_action({
                                name: 'Xem trước sơ yếu lý lịch đã ký số - Mẫu 2c hợp nhất',
                                type: 'ir.actions.act_window',
                                view_type: 'form',
                                view_mode: 'form',
                                res_model: 'temp_model_kyso',
                                context: {
                                    'attachment_id': result.attachment_id ? result.attachment_id : -1,
                                    'file_name': result.file_name,
                                    'edition_id': result.edition_id,
                                },
                                views: [[result.view_id, 'form']],
                                target: 'new'
                            }).then(function () {
                                edit_form_preview_signed_file();
                            });
                        } else if (result.not_found_user_smart_ca){
                            self.not_found_user_smart_ca = true;
                            self.do_action({
                                name: 'Thông báo',
                                type: 'ir.actions.act_window',
                                view_type: 'form',
                                view_mode: 'form',
                                res_model: 'temp_model_kyso',
                                views: [[result.view_id, 'form']],
                                target: 'new'
                            }).then(function () {
                                $('#message_warning').text(result.message);
                            }).fail(function () {
                                self.SignAdvanced(edition_id, data, type, option, hinhthuc_kyso);
                            });
                        }
                        else{
                            self.not_found_user_smart_ca = true;
                            show_view_error(self, result.message, result.view_id);
                        }
                    });
                    setTimeout(function () {
                        framework.unblockUI();
                        if (!self.not_found_user_smart_ca){
                            add_mask_thongbao('Đã gửi yêu cầu ký.<br/>Vui lòng xác nhận trên ứng dụng ký số');
                        }
                    }, 3000);
                    // code block
                    break;
                default:
                    console.log(hinhthuc_kyso);
            }
        },
        complete_kyso: function (_base64_daky, edition_id) {
            var self = this;
            self._rpc({
                model: 'datn.kyso.file',
                method: 'complete_kyso',
                args: [edition_id, _base64_daky],
            })
                .then(function (result) {
                    alert('Ký số thành công')
                    location.reload();
                    framework.unblockUI();
                });
        },
        getCurrentDate: function () {
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();
            var hh = String(today.getHours()).padStart(2, '0');
            var min = String(today.getMinutes()).padStart(2, '0');
            var ss = String(today.getSeconds()).padStart(2, '0');
            return dd + '/' + mm + '/' + yyyy + " - " + hh + ":" + min + ":" + ss;
        },
        action_kyso_duyet: function (edition_ids, hinhthuc_kyso, key, is_next_default, loai_duyet) {
            var self = this;
            switch (hinhthuc_kyso) {
                case 'token':
                    get_info_cts_from_token(self, key, edition_ids, is_next_default, loai_duyet);
                    break;
                case 'smart_ca':
                    framework.blockUI();
                    self._rpc({
                        model: 'vnpt.hr.employee.edition',
                        method: 'action_duyet_smart_ca',
                        args: [edition_ids, is_next_default, loai_duyet],
                    }).then(function (result) {
                        remove_mask_thongbao();
                        if (result.success){
                            self.do_notify('Ký số trên dữ liệu thành công!');
                            if (loai_duyet === 'duyet_1_hoso'){
                                chuyen_trangthai_sauduyet(self, result);
                            }
                            self.do_action(result.action);
                        }else if (result.not_found_user_smart_ca){
                            self.not_found_user_smart_ca = true;
                            self.do_action({
                                name: 'Thông báo',
                                type: 'ir.actions.act_window',
                                view_type: 'form',
                                view_mode: 'form',
                                res_model: 'temp_model_kyso',
                                views: [[result.view_id, 'form']],
                                target: 'new'
                            }).then(function () {
                                $('#message_warning').text(result.message);
                            }).fail(function () {
                                self.action_kyso_duyet(edition_ids, hinhthuc_kyso, key, is_next_default, loai_duyet);
                            });
                        }
                        else{
                            self.not_found_user_smart_ca = true;
                            show_view_error(self, result.message, result.view_id);
                        }
                    });
                    setTimeout(function () {
                        framework.unblockUI();
                        if (!self.not_found_user_smart_ca){
                            add_mask_thongbao('Đã gửi yêu cầu ký.<br/>Vui lòng xác nhận trên ứng dụng ký số');
                        }
                    }, 3000);
                    // code block
                    break;
                default:
                    console.log(hinhthuc_kyso);
            }
        },
        action_kyso: function (edition_id, data, hinhthuc_kyso) {
            if(!vnpt_plugin.checkBrowser()){
				alert("Trình duyệt hiện tại không hỗ trợ Plugin. Vui lòng sử dụng trình duyệt khác");
				return;
			}
            var self = this;
            let _2c_base_64 = data._2c_base_64;
            let signature = data.signature;
            let chu_ky = data.chu_ky;
            let key = data.key;

            switch (hinhthuc_kyso) {
                case 'token':
                    // check plugin
                    add_mask_thongbao('Đang kiểm tra Plugin');
                    vnpt_plugin.checkPlugin().then(function (data) {
                        if (data === "1") {
                            vnpt_plugin.getVersion().then(function (data) {
                                if (data !== '1.0.4.3'){
                                    remove_mask_thongbao();
                                    show_view_tai_plugin(self);
                                    return;
                                }
                                clearTimeout(timer); // clear
                                vnpt_plugin.setLicenseKey(key).then(function (data) {
                                    if (data.split(":").length > 1 && data.split(":")[1][0] !== '1'){
                                        remove_mask_thongbao();
                                        alert("Lincense Plugin không hợp lệ hoặc đã hết hạn");
                                        return;
                                    }
                                    remove_mask_thongbao();
                                    add_mask_thongbao('Đã gửi yêu cầu chọn chứng thư.<br/>Vui lòng chọn các chứng thư có sẵn');
                                    self.signAdvanceView(edition_id, _2c_base_64, chu_ky, signature);
                                }).catch(function (e) {
                                    console.log(e)
                                });
                            });
                        } else {
                            remove_mask_thongbao();
                            timer = setTimeout(checkPlugin, 1500);
                        }
                        return true;
                    }).catch(function (e) {
                        remove_mask_thongbao();
                        show_view_tai_plugin(self);
                    });
                    break;
                case 'smart_ca':
                    self.initSignPage(edition_id, _2c_base_64, chu_ky, 'smart_ca', signature);
                    // code block
                    break;
                default:
                    console.log(hinhthuc_kyso);
            }
        },
        check_kyso_gui_xn: function (type) {
            var self = this;
            var edition_id = self.state.data.id;
            if (!edition_id) {
                return
            }
            self._rpc({
                model: 'datn.kyso.file',
                method: 'send_to_approve_kyso',
                args: [edition_id, type],
            }).then(function (data) {
                remove_mask_thongbao();
                if (data.render === 'fail') {
                    console.log(data.message);
                } else if (data.is_config) {
                    self.action_kyso(edition_id, data, data.hinhthuc_kyso);
                } else {
                    let name = data.file_name ? 'Xem trước sơ yếu lý lịch đã ký số - Mẫu 2c hợp nhất' : 'Chọn hình thức ký số';
                    self.do_action({
                        name: name,
                        type: 'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        res_model: 'temp_model_kyso',
                        context: {
                            'edition_id': edition_id,
                            'attachment_id': data.attachment_id ? data.attachment_id : -1,
                            'file_name': data.file_name
                        },
                        views: [[data.view_id, 'form']],
                        target: 'new'
                    }).then(function () {
                        if (data.file_name) {
                            edit_form_preview_signed_file();
                        }
                    });
                }
            });
            setTimeout(function () {
                $('.blockOverlay').css('display', 'None');
                $('.blockMsg').css('display', 'None');
            }, 3000);
            $('button[disabled="disabled"]').removeAttr("disabled");
        },
    });

});