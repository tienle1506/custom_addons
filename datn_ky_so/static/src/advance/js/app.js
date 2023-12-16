var _objMapValidTimeCode = {
    "0": "chứng thư số hợp lệ",
    "1": "lỗi không xác định",
    "2": "chứng thư số hết hạn",
    "3": "chứng thư số chưa đến hạn",
    "8": "không lấy được thông tin chứng thư số"
};

var _objMapCheckOCSP = {
    "0": "chứng thư số hợp lệ",
    "1": "lỗi không xác định",
    "4": "chứng thư số đã bị thu hồi.",
    "6": "kiểm tra trạng thái thu hồi của chứng thư không thành công",
    "7": "chứng thư số không được cấp bới CA tin tưởng",
    "8": "không lấy được thông tin chứng thư số",
    "9": "không lấy được thông tin chứng thư số CA",
    "10": "không tìm thấy đường dẫn tới server ocsp"
};

var _objMapCheckCRL = {
    "0": "chứng thư số hợp lệ",
    "1": "lỗi không xác định",
    "4": "chứng thư số đã bị thu hồi.",
    "6": "kiểm tra trạng thái thu hồi của chứng thư không thành công",
    "7": "chứng thư số không được cấp bới CA tin tưởng",
    "8": "không lấy được thông tin chứng thư số",
    "9": "không lấy được thông tin chứng thư số CA"
};

var _objMapCheckCRLBase64 = {
    "0": "chứng thư số hợp lệ",
    "1": "lỗi không xác định",
    "4": "chứng thư số đã bị thu hồi.",
    "6": "kiểm tra trạng thái thu hồi của chứng thư không thành công",
    "7": "chứng thư số không được cấp bới CA tin tưởng",
    "8": "không lấy được thông tin chứng thư số",
    "9": "không lấy được thông tin chứng thư số CA"
};

var _objMapCheckPluginAdvanced = {
    "0": "",
    "1": ""
};

function checkVersionPlugin() {
    showLoading('Đang xử lý');
    try {
        setTimeout(function () {
            vnpt_plugin.getVersion().then(function (data) {
                $('#txtVersionPlugin').val(data);
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function checkPluginAdvanced(id) {
    showLoading('Đang xử lý');
    try {
        setTimeout(function () {
            vnpt_plugin.checkPluginAdvanced().then(function (data) {
                if(data == 1) {
                    $('#txtPluginAdvanced' + id).val('Là plugin do VNPT cung cấp');
                }
                else {
                    $('#txtPluginAdvanced' + id).val('Không phải plugin do VNPT cung cấp');
                }

                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }
}

// function funcCallbackCheckPluginAdvanced(data) {
//     console.log(data);
// }

function checkPluginReady(id) {
    showLoading('Đang xử lý');
    try {
        setTimeout(function () {
            switch (id) {
                case 1:
                    vnpt_plugin.checkPlugin().then(function (data) {
                        console.log(data);
                        if(data == 1) {
                            $('#txtPluginReady'+id).val('Đã cài');
                        }
                        else {
                            $('#txtPluginReady'+id).val('Chưa cài');
                        }
                        // $('#txtPluginReady').val(data);
                        closeAlert();
                    });
                    break;
                case 2:
                    vnpt_plugin.checkPlugin().then(function (data) {
                        console.log(data);
                        if(data == 1) {
                            $('#txtPluginReady'+id).val('Đang chạy');
                        }
                        else {
                            $('#txtPluginReady'+id).val('Không hoạt động');
                        }
                        // $('#txtPluginReady').val(data);
                        closeAlert();
                    });
                    break;
            }

        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function funcCallBackGetCertInfo(data) {
    debugger;
    var _data_parser = JSON.parse(data);
    vnpt_plugin.CheckValidTime(_data_parser['serial'], $('#txtTime38261').val(), null, null).then(function (data) {
        console.log(data);
        $('#txt38261').val(_objMapValidTimeCode[data + '']);
        closeAlert();
    });
}

function checkValidTime(type) {
    showLoading('Đang xử lý');
    try {
        setTimeout(function () {
            switch (type) {
                case 0:
                    vnpt_plugin.CheckValidTime($('#txtSerialNumber38253').val(), $('#txtTime38253').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38253').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
                case 1:
                    vnpt_plugin.CheckValidTime($('#txtSerialNumber38255').val(), null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38255').val('Chứng thư số còn hạn');
                        }
                        else if(data == 2) {
                            $('#txt38255').val('Chứng thư số hết hạn');
                        }
                        else {
                            $('#txt38255').val('Có lỗi trong quá trình kiểm tra');
                        }
                        closeAlert();
                    });
                    break;
                case 2:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38256').val(), null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38256').val('Chứng thư số chưa bị thu hồi');
                        }
                        else if(data == 4) {
                            $('#txt38256').val('Chứng thư số đã bị thu hồi');
                        }
                        else {
                            $('#txt38256').val('Có lỗi trong quá trình kiểm tra');
                        }
                        closeAlert();
                    });
                    break;
                case 3:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38257').val(), null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 7) {
                            $('#txt38257').val('Không được cung cấp bởi CA tin tưởng');
                        }
                        else if(data == 0) {
                            $('#txt38257').val('Được cung cấp bởi CA tin tưởng');
                        }
                        else {
                            $('#txt38257').val('Có lỗi trong quá trình kiểm tra');
                        }

                        closeAlert();
                    });
                    break;
                case 4:
                    vnpt_plugin.getCertInfo(null, null).then(function (data) {
                        var _data_parser = JSON.parse(data);
                        vnpt_plugin.CheckValidTime(_data_parser['serial'], $('#txtTime38261').val(), null, null).then(function (data) {
                            console.log(data);
                            $('#txt38261').val(_objMapValidTimeCode[data + '']);
                            closeAlert();
                        });
                    });

                    break;
                case 5:
                    vnpt_plugin.getCertInfo(null, null).then(function (data) {
                        var _data_parser = JSON.parse(data);
                        $('#txt38262').val('Thời gian hiệu lực từ: ' + _data_parser['notBefore'] + ' đến: ' + _data_parser['notAfter']);
                        closeAlert();
                    });
                    break;
                case 6:
                    vnpt_plugin.getCertInfo(null, null).then(function (data) {
                        var _data_parser = JSON.parse(data);
                        vnpt_plugin.CheckValidTime(_data_parser['serial'], null, null, null).then(function (data) {
                            console.log(data);
                            if(data == 0) {
                                $('#txt38263').val('Chứng thư số còn hạn');
                            }
                            else {
                                $('#txt38263').val(_objMapValidTimeCode[data + '']);
                            }
                            closeAlert();
                        });
                    });
                    break;
                case 7:
                    vnpt_plugin.getCertInfo(null, null).then(function (data) {
                        var _data_parser = JSON.parse(data);
                        vnpt_plugin.CheckOCSP(_data_parser['serial'], null, null, null).then(function (data) {
                            console.log(data);
                            if(data == 0) {
                                $('#txt38264').val('Chứng thư số chưa bị thu hồi');
                            }
                            else {
                                $('#txt38264').val(_objMapCheckOCSP[data + '']);
                            }
                            closeAlert();
                        });
                    });
                    break;
                case 8:
                    vnpt_plugin.getCertInfo(null, null).then(function (data) {
                        var _data_parser = JSON.parse(data);
                        vnpt_plugin.CheckOCSP(_data_parser['serial'], null, null, null).then(function (data) {
                            console.log(data);
                            if(data == 0) {
                                $('#txt38265').val('Được cung cấp bởi CA tin tưởng');
                            }
                            else {
                                $('#txt38265').val(_objMapCheckOCSP[data + '']);
                            }
                            closeAlert();
                        });
                    });
                    break;
                case 9:
                    vnpt_plugin.CheckValidTime($('#txtSerialNumber38269').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38269').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
                case 10:
                    vnpt_plugin.CheckValidTime($('#txtSerialNumber38270').val(), $('#txtTime38270').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38270').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
                case 11:
                    vnpt_plugin.CheckValidTime($('#txtSerialNumber38271').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38271').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
                case 12:
                    vnpt_plugin.CheckValidTime(null, null, $('#txtSerialNumber38272').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38272').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
                case 13:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38274').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38274').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 14:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38275').val(), null, $('#txtUrl38275').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38275').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 15:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38276').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38276').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 16:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38277').val(), null, null, funcCallBack);
                    break;
                case 17:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38278').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38278').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 18:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38279').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38279').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 19:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38280').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38280').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 20:
                    var time = new Date().getDate() + "/" + (new Date().getMonth() + 1) + "/" + new Date().getFullYear() + " " + new Date().getHours() + ":" + new Date().getMinutes() + ":" + new Date().getSeconds();
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38281').val(), time, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38281').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 21:
                    vnpt_plugin.CheckOCSP($('#txtSerialNumber38282').val(), $('#txtTime38282').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38282').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 22:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38283').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38283').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 23:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38284').val(), null, $('#txtUrl38284').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38284').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 24:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38285').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38285').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 25:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38286').val(), null, null, funcCallBack);
                    break;
                case 26:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38287').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38287').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 27:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38288').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38288').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 28:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38289').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38289').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 29:
                    var time = new Date().getDate() + "/" + (new Date().getMonth() + 1) + "/" + new Date().getFullYear() + " " + new Date().getHours() + ":" + new Date().getMinutes() + ":" + new Date().getSeconds();
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38290').val(), time, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38290').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 30:
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38291').val(), $('#txtTime38291').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38291').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 31:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38293').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38293').val(_objMapCheckCRL[data + '']);
                        closeAlert();
                    });
                    break;
                case 32:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38294').val(), null, $('#txtUrl38294').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38294').val(_objMapCheckCRL[data + '']);
                        closeAlert();
                    });
                    break;
                case 33:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38295').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38295').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 34:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38296').val(), null, null, null, funcCallBackCRL);
                    break;
                case 35:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38297').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38297').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 36:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38298').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38298').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 37:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38299').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38299').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 38:
                    var time = new Date().getDate() + "/" + (new Date().getMonth() + 1) + "/" + new Date().getFullYear() + " " + new Date().getHours() + ":" + new Date().getMinutes() + ":" + new Date().getSeconds();
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38300').val(), time, null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38300').val('Chứng thư số chưa bị thu hồi');
                        }
                        else if(data == 4) {
                            $('#txt38300').val('Chứng thư số đã bị thu hồi');
                        }
                        else {
                            $('#txt38300').val('Có lỗi trong quá trình kiểm tra');
                        }
                        closeAlert();
                    });
                    break;
                case 39:
                    vnpt_plugin.CheckCRL($('#txtSerialNumber38301').val(), $('#txtTime38301').val(), null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38301').val('Chứng thư số chưa bị thu hồi');
                        }
                        else if(data == 4) {
                            $('#txt38301').val('Chứng thư số đã bị thu hồi');
                        }
                        else {
                            $('#txt38301').val('Có lỗi trong quá trình kiểm tra');
                        }
                        // $('#txt38301').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;

                case 40:
                    debugger;
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38302').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        if(data == 4) {
                            $('#txt38302').val('Chứng thư số đã bị thu hồi');
                        }
                        else if(data == 0) {
                            $('#txt38302').val('Chứng thư số chưa bị thu hồi');
                        }
                        else {
                            $('#txt38302').val('Có lỗi trong quá trình kiểm tra');
                        }
                        // $('#txt38302').val(_objMapCheckCRL[data + '']);
                        closeAlert();
                    });
                    break;
                case 41:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38303').val(), null, $('#txtUrl38303').val(), null, null).then(function (data) {
                        console.log(data);
                        $('#txt38303').val(_objMapCheckCRL[data + '']);
                        closeAlert();
                    });
                    break;
                case 42:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38304').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38304').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 43:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38305').val(), null, null, null, funcCallBackCRL);
                    break;
                case 44:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38306').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38306').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 45:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38307').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38307').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 46:
                    vnpt_plugin.CheckCRLBase64($('#txtSerialNumber38308').val(), null, null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38308').val(_objMapCheckOCSP[data + '']);
                        closeAlert();
                    });
                    break;
                case 47:
                    debugger;
                    var time = new Date().getDate() + "/" + (new Date().getMonth() + 1) + "/" + new Date().getFullYear() + " " + new Date().getHours() + ":" + new Date().getMinutes() + ":" + new Date().getSeconds();
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38309').val(), time, null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38309').val('Chứng thư số chưa bị thu hồi');
                        }
                        else if(data == 4) {
                            $('#txt38309').val('Chứng thư số đã bị thu hồi');
                        }
                        else {
                            $('#txt38309').val('Có lỗi trong quá trình kiểm tra');
                        }
                        closeAlert();
                    });
                    break;
                case 48:
                    debugger;
                    vnpt_plugin.CheckOCSPBase64($('#txtSerialNumber38310').val(), $('#txtTime38310').val(), null).then(function (data) {
                        console.log(data);
                        if(data == 0) {
                            $('#txt38310').val('Chứng thư số chưa bị thu hồi');
                        }
                        else if(data == 4) {
                            $('#txt38310').val('Chứng thư số đã bị thu hồi');
                        }
                        else {
                            $('#txt38310').val('Có lỗi trong quá trình kiểm tra');
                        }
                        closeAlert();
                    });
                    break;
            }
        },500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }
}

function funcCallBack(data) {
    closeAlert();
    alert(_objMapCheckOCSP[data + '']);
}

function funcCallBackCRL(data) {
    closeAlert();
    alert(_objMapCheckCRL[data + '']);
}

function checkCertOnLocal() {
    showLoading('Đang xử lý!');
    try {
        vnpt_plugin.GetAllCertificates($('#txtSerialNumber38254').val(), null, null).then(function (data) {
            console.log(data);
            if(data && data != '') {
                console.log(data);
                if(data && data !== '') {
                    $('#txt3809').val('Đã được import vào Window store');
                }
                else {
                    $('#txt3809').val('Chưa được import vào Window store');
                }
                closeAlert();
            }
            // var _data_parser = JSON.parse(data);
            // vnpt_plugin.GetAllCertificates(_data_parser['serial'], null, null).then(function (data) {
            //     console.log(data);
            //     if(data && data !== '') {
            //         $('#txt3809').val('Được cung cấp bởi CA tin tưởng');
            //     }
            //     else {
            //         $('#txt3809').val('Không được cung cấp bởi CA tin tưởng');
            //     }
            //     closeAlert();
            // });
        });
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function getCertInfo(type) {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            switch (type) {
                case 0:
                    vnpt_plugin.GetAllCertificates($('#txtSerialNumber38258').val(), null, null).then(function (data) {
                        console.log(data);
                        var _data_parser = JSON.parse(JSON.parse(data)[0]);
                        $('#txt38258').val(_data_parser['signatureAlgorithm']);
                        closeAlert();
                    });
                    break;
                case 1:
                    vnpt_plugin.GetAllCertificates($('#txtSerialNumber38259').val(), null, null, null).then(function (data) {
                        console.log(data);
                        var _data_parser = JSON.parse(JSON.parse(data)[0]);
                        $('#txt38259').val(_data_parser['keyUsage']);
                        closeAlert();
                    });
                    // vnpt_plugin.getCertInfo().then(function (data) {
                    //     var _data_parser = JSON.parse(data);
                    //     $('#txt38259').val(_data_parser['keyUsage']);
                    //     closeAlert();
                    // });
                    break;
                case 2:
                    vnpt_plugin.GetAllCertificates($('#txtSerialNumber38260').val(), null, null, null).then(function (data) {
                        var _data_parser = JSON.parse(data)[0];
                        $('#txt38260').val(_data_parser);
                        closeAlert();
                    });
                    // vnpt_plugin.getCertInfo().then(function (data) {
                    //     $('#txt38260').val(data);
                    //     closeAlert();
                    // });
                    break;
                case 3:
                    vnpt_plugin.getCertInfo().then(function (data) {
                        var _data_parser = JSON.parse(data);
                        $('#txt38266').val(_data_parser['signatureAlgorithm']);
                        closeAlert();
                    });
                    break;
                case 4:
                    vnpt_plugin.getCertInfo().then(function (data) {
                        var _data_parser = JSON.parse(data);
                        $('#txt38267').val(_data_parser['keyUsage']);
                        closeAlert();
                    });
                    break;
                case 5:
                    vnpt_plugin.getCertInfo().then(function (data) {
                        $('#txt38268').val(data);
                        closeAlert();
                    });
                    break;
            }
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function checkValidTimeBase64(type) {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            switch (type) {
                case 0:
                    vnpt_plugin.CheckValidTimeBase64($('#txtSerialNumber38273').val(), null, null, null).then(function (data) {
                        console.log(data);
                        $('#txt38273').val(_objMapValidTimeCode[data + '']);
                        closeAlert();
                    });
                    break;
            }
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function showCertificateViewer(type) {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            switch (type) {
                case 0:
                    vnpt_plugin.ShowCertificateViewer($('#txtSerialNumber38292').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38292').val(data);
                        closeAlert();
                    });
                    break;
            }
        },500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function changeLanguage(type) {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            switch (type) {
                case 0:
                    vnpt_plugin.setLanguage($('#txtLang38311').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38311').val(data);
                        closeAlert();
                    });
                    break;
                case 1:
                    vnpt_plugin.setLanguage($('#txtLang38312').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38312').val(data);
                        closeAlert();
                    });
                    break;
                case 2:
                    vnpt_plugin.setLanguage($('#txtLang38313').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38313').val(data);
                        closeAlert();
                    });
                    break;
                case 3:
                    vnpt_plugin.setLanguage($('#txtLang38314').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38314').val(data);
                        closeAlert();
                    });
                    break;
                case 4:
                    vnpt_plugin.setLanguage($('#txtLang38315').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38315').val(data);
                        closeAlert();
                    });
                    break;
                case 5:
                    vnpt_plugin.setLanguage($('#txtLang38316').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38316').val(data);
                        closeAlert();
                    });
                    break;
                case 6:
                    vnpt_plugin.setLanguage($('#txtLang38317').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38317').val(data);
                        closeAlert();
                    });
                    break;
                case 7:
                    vnpt_plugin.setLanguage($('#txtLang38318').val(), null).then(function (data) {
                        console.log(data);
                        $('#txt38318').val(data);
                        closeAlert();
                    });
                    break;
            }
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function openDocument() {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            vnpt_plugin.OpenDocument($('#txtBase6438327').val(), $('#txtName38327').val(), $('#txtExtension38327').val(), null).then(function (data) {
                console.log(data);
                $('#txt38327').val(data);
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function scanDocument() {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            vnpt_plugin.Scan($('#txtBase6438319').val(), null).then(function (data) {
                $('#txt38319').val(data);
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function scanDocumentFromConfig() {
    showLoading('Đang xử lý!');
    try {
        var scannerOptions = new ScannerOptions();
        scannerOptions.useADF = $('#chkAutoScroll').is(':checked');
        scannerOptions.blackWhite = $('#chkBlackWhite').is(':checked');
        scannerOptions.showUI = $('#chkShowUI').is(':checked');
        scannerOptions.useDuplex = $('#chkTwoPage').is(':checked');
        setTimeout(function () {
            vnpt_plugin.Scan($('#txtOption38320').val(), null, JSON.stringify(scannerOptions)).then(function (data) {
                $('#txt38320').val(data);
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function setIgnoreListFile() {

}

function handleFile() {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            vnpt_plugin.HandleFile().then(function (e) {
                var _data_parser = JSON.parse(e);
                debugger;
                $('#txt38339').val(e);
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        console.log(e);
        closeAlert();
    }

}

function GetAllFiles() {
    showLoading('Đang xử lý!');
    try {
        setTimeout(function () {
            vnpt_plugin.GetAllFiles($('#txtName38340').val(), null).then(function (e) {
                var _data_parser = JSON.parse(e);
                var rs = 'Danh sách các file scan sẽ được upload lên hệ thống: \n';
                if(_data_parser && _data_parser.length > 0) {
                    _data_parser.map((item) => {
                        rs += '- ' + item.split('\\')[item.split('\\').length-1] + '\n';
                    });
                    $('#txt38340').val(rs);
                }
                else {
                    $('#txt38340').val('Không có file nào!');
                }
                closeAlert();
            });
        }, 500);
    }
    catch (e) {
        $('#txt38340').val('Không thành công!');
        console.log(e);
        closeAlert();
    }
}

function getCertInfoFromBase64(certBase64) {

}
