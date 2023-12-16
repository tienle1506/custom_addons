﻿/*!
 * =============================================================
 * vnptpdf v1.0.2 - PDF Advanced signature helper.
 *
 * Copyright © 2019 VNPT IT
 * Author: TuanBS<tuanbs@vnpt.vn>
 * =============================================================
 */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // CommonJS
        module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        root.VnptPdf = factory(root.jQuery);
    }
}(this, function ($) {
    var pluginName = "vnptpdf";
    var properties_lang={
        add:'Thêm',
        logoText:'KySo',
        vi:'Tiếng Việt',
        en:'Tiếng Anh',
        legend_1:'Chữ ký',
        legend_2:'Bình luận',
        adv_text:'Tùy chọn nâng cao',
        label1:'Kiểu hiển thị',
        viewTypeOpt1:'Chỉ hiển thị mô tả',
        viewTypeOpt2:'Ảnh chữ ký và mô tả',
        viewTypeOpt3:'Chỉ hiển thị ảnh',
        label2:'Tùy chọn hình hảnh',
        label3:'Cỡ chữ hiển thị',
        modalTitle1:'Thêm ảnh chữ ký',
        modalTitle2:'Thêm comment',
        labelTextView:'Trang hiển thị',
        labelContentView:'Nội dung hiển thị',
        cancel:'Huỷ',
        confirm:'Xác nhận',
        fontSize:'Cỡ chữ',
        sign:'Ký dữ liệu',
        vi:'Tiếng Việt',
        vn:'Tiếng Anh',
    }
    
    /**
     * 
     * @param {any} element Wrapper element
     * @param {any} options Plugin options
     * @param {any} callback Callback function
     */
    function VnptPdf(element, options) {
        var defaults = {
            Callback: null,
            location: '',
            reason: '',
            signatures: [],
            comments: [],
            pdfFile: {
                file: null,
                totalPages: 0
            },
            fontName: 'Time',
            fontSize: 10,
            fontStyle: 3,
            visibleType: 2,
            fontColor: '000000',
            visibleText: 'Ký bởi: _______________\nNgày ký: ' + this.getCurrentDate() + '\nTổ chức xác thực: _ _ _ _ _ _ _ _ _',
            signatureImg: "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",
            useDefaultText: true,
            TextAlign: 1,
            
        };
        this.wrapper = element;
        this.CallBack = options.Callback;        
        this.settings = $.extend(true, defaults, options);
        if ((typeof options.visibleText !== 'undefined') && options.visibleText !== '') {
            this.settings.useDefaultText = false;
        }
        this.pdfPages = [];
        this.show = false;
        
        $('body').append('<div id="dpi" style="height: 1in; left: -100%; position: absolute; top: -100%; width: 1in;"></div>');
        $("[data-label]").each(function(){
            lege
            console.log($(this).attr('data-label'));
        });
    }

    VnptPdf.prototype.getCurrentDate = function () {
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        var hh = today.getHours();
        var min = today.getMinutes();
        var ss = today.getSeconds();

        return dd + '/' + mm + '/' + yyyy + " - " + hh + ":" + min + ":" + ss;
    };

    /**
     * */
    VnptPdf.prototype.initUI = function () {
        
        const self = this;

        // Color picker plugin
        this.wrapper.html(pdfWorkingArea.replace('SIG-COLOR', '#' + this.settings.fontColor));
        jscolor.installByClassName("jscolor");

        // Add comment modal
        this.wrapper.append(_addCommentModal);

        // Add signature view modal
        this.wrapper.append(_addSignatureModal);
        $('#add-signature-modal').find('.pdf-btn').click(function () {
            self.addSignatureHandle();
        });
        $('#sig-font-color').change({ msgTarget: this }, this.changeFontColorEvent);

        //this.changeSignatureVisibleType();
        this.changeSignatureVisibleImg();

        // Add change visible type listener
        this.visibleTypeInput = $('#sign-visible-type-select');
        this.visibleTypeInput.val('' + this.settings.visibleType);
        this.visibleTypeInput.change({ msgTarget: this }, this.changeSignatureVisibleTypeEvent);
       
        //this.textAlignTypeInput = $('input[name="textAlign"]');
        //this.textAlignTypeInput.change({ msgTarget: this }, this.changeTextAlignOptionEvent);

        this.signatureTextInput = $('#pdf-sign-text');
        this.signatureTextInput.val('' + this.settings.visibleText.replace("\n", '\n'));
        this.signatureTextInput.keyup({ msgTarget: this }, this.updateSignatureTextEvent);

        this.signatureTextDefaultInput = $('#useDefaultText');
        this.signatureTextDefaultInput.change({ msgTarget: this }, this.changeVisibleTextDefault);

        this.fontNameInput = $('#sign-font-type-select');
        this.fontNameInput.change({ msgTarget: this }, this.changeSignatureFontNameEvent);

        $('#sign-font-style-select').val('' + this.settings.fontStyle);
        this.fontNameInput.val(this.settings.fontName);
        $('#sign-font-style-select').change({ msgTarget: this }, this.changeFontStyleEvent);
        
        $('#pdf-sign-page').val(this.settings.sigPage);
        this.signaturePageBtn = $('#pdf-sign-page-btn');
        this.signaturePageBtn.click({ msgTarget: this }, this.changeSignaturePageEvent);

        this.signatureImgBtn = $('#signature-img-btn');
        this.signatureImgBtn.click({ msgTarget: this }, this.changeSignatureImageEvent);

        this.signatureCommentBtn = $('#add-comment-btn');
        this.signatureCommentBtn.click({ msgTarget: this }, this.addComment);

        this.signatureAddBtn = $('#add-sig-btn');
        this.signatureAddBtn.click({ msgTarget: this }, this.addSignature);

        $(".pdf-action-menu").mCustomScrollbar({
            theme: "minimal-dark"
        });

        $('.pdf-action-menu').append(_menuSwitch);
        
        
        $('.page-aside-switch').click(function () {
            let menuW = $('.pdf-action-menu').width();
            $('.pdf-action-menu').css('width', 370 - menuW);
            if (menuW > 0) {
                $('.pdf-action-menu').css('padding', '0');
                $('.pdf-page').css('padding-left', '0');
            } else {
                $('.pdf-action-menu').css('padding', '10px 25px');
                $('.pdf-action-menu').css('padding-top', '45px');
            }
            self.windowResizeEventHandle();
        });

        $('#sig-font-size').asRange();
        $('#sig-font-size').asRange('set', '' + this.settings.fontSize); 
        $('#sig-font-size').on('asRange::change', function (e) {
            self.settings.fontSize = $('#sig-font-size').asRange('get');
            self.setFontSize();
        });

        var coll = document.getElementsByClassName("pdf-collapsible");
        var i;

        for (i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function () {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        }
    };

    /**
     * Init pdf data from base64 encode
     * @param {any} base64 pdf data with base64 encoded
     */
    VnptPdf.prototype.initDataBase64 = function (base64) {
        var typedarray = this.convertDataURIToBinary(base64);
        this.initData(typedarray);
    };

    /**
     * Init pdf data from file
     * @param {any} file Pdf data file
     */
    VnptPdf.prototype.initDataFile = function (file) {
        var fileReader = new FileReader();
        var self = this;
        getBase64(file);
        fileReader.onload = function () {
            var typedarray = new Uint8Array(this.result);
            self.initData(typedarray);
        };
        fileReader.readAsArrayBuffer(file);
    };
    function getBase64(file) {
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            console.log(reader.result);
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };
    }
    /**
     * Init pdf data from byte array
     * @param {any} typedarrayData byte[] array pdf data
     */
    VnptPdf.prototype.initData = function (typedarrayData) {
        this.data = typedarrayData;
    };

    VnptPdf.prototype.start = function () {
        var self = this;
        self.initUI();
        PDFJS.getDocument(self.data).then(function (pdf) {
            if (pdf.numPages < self.settings.sigPage) {
                console.error('[Error] >> options[sigPage] is invalid, total pages is %d', pdf.numPages);
                return;
            }

            if (self.settings.useLastPage) {
                self.settings.sigPage = pdf.numPages;
                $('#pdf-sign-page').val(self.settings.sigPage);
            }

            const totalPages = pdf.numPages;
            this.pdfPages = [];

            self.renderPdf(pdf, 1, totalPages);
        });
        
    };
   
    /**
     * Render all pdf pages using recursive function
     * @param {any} pdf PDF content
     * @param {any} index page index 
     * @param {any} totalPages Total pages
     */
    VnptPdf.prototype.renderPdf = function (pdf, index, totalPages) {
        const self = this;
        $action_buttons=$('#action-btns');
        // Recursive stop condition
        if (index > totalPages) {
            self.show = true;
            $('#action-btns').empty();
            $('#action-btns').append(
                ' <button class="pdf-btn" style="min-width:100px;" id="pdf-complete" data-label="sign">'+properties_lang.sign+'</button>' +

                ' <button class="pdf-btn pdf-btn-second"  style="min-width:100px;" id="pdf-cancel" data-label="cancel">'+properties_lang.cancel+'</button>'
            );

            self.btnSign = $('#pdf-complete');
            self.btnSign.click({ msgTarget: this }, this.complete);

            self.btnCancel = $('#pdf-cancel');
            self.btnCancel.click({ msgTarget: this }, this.reject);
            self.initDefaultSignature();
            self.initSignatures();
            self.initComments();
            return;
        }

        pdf.getPage(index).then(function (page) {
            const dpi = document.getElementById('dpi').offsetWidth;
            var xview = page.getViewport(1);
            self.pdfPages.push({
                width: xview.width,
                height: xview.height
            });
            let canvasId = "pdfPage_" + (index);
            var canvasI = _canvasPdf.replace("ID_VALUE", canvasId);
            $('.pdf-page').append(canvasI);

            var viewport = page.getViewport(1 / 72 * dpi);

            var canvas = document.getElementById(canvasId);
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Render PDF page into canvas context.
            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            var renderTask = page.render(renderContext);

            renderTask.promise.then(function () {
                $('#' + canvasId).show();
                self.renderPdf(pdf, index + 1, totalPages);
            });
        });

        var add=$('[data-label="add"]');
        var logoText=$('[data-label="logoText"]');
        var legend_1=$('[data-label="legend_1"]');
        var legend_2=$('[data-label="legend_2"]');
        var adv_text=$('[data-label="adv_text"]');
        var label1=$('[data-label="label1"]');
        var viewTypeOpt1=$('[data-label="viewTypeOpt1"]');
        var viewTypeOpt2=$('[data-label="viewTypeOpt2"]');
        var viewTypeOpt3=$('[data-label="viewTypeOpt3"]');
        var label2=$('[data-label="label2"]');
        var label3=$('[data-label="label3"]');
        var modalTitle1=$('[data-label="modalTitle1"]');
        var modalTitle2=$('[data-label="modalTitle2"]');
        var labelTextView=$('[data-label="labelTextView"]');
        var labelContentView=$('[data-label="labelContentView"]');
        var cancel=$('[data-label="cancel"]');
        var confirm=$('[data-label="confirm"]');
        var fontSize=$('[data-label="fontSize"]');
        var sign=$('[data-label="sign"]');
        var langOption1=$('[data-label="vi"]');
        var langOption2=$('[data-label="en"]');
        
        $('#sel-change-lang').change(function(){
            $val=$(this).val();
            var sign1=$("#action-btns").find('[data-label="sign"]');
            var cancel1=$("#action-btns").find('[data-label="cancel"]');
            if($val==1){
                properties_lang={
                    add:'+ Add',
                    logoText:'KySo',
                    legend_1:'Signatures',
                    legend_2:'Comments',
                    adv_text:'Advance options',
                    label1:'Display Type',
                    viewTypeOpt1:'Show text only',
                    viewTypeOpt2:'Display text and images',
                    viewTypeOpt3:'Show image only',
                    label2:'Image options',
                    label3:'Font size',
                    modalTitle1:'Add signature to page',
                    modalTitle2:'Add comment',
                    labelTextView:'Display page',
                    labelContentView:'Display content',
                    cancel:'Cancel',
                    confirm:'Confirm',
                    fontSize:'Font size',
                    sign:'Sign data',
                    vi:'Vietnamese',
                    en:'English',


                }
                
            }else{
                properties_lang={
                    add:'Thêm',
                    logoText:'KySo',
                    legend_1:'Chữ ký',
                    legend_2:'Bình luận',
                    adv_text:'Tùy chọn nâng cao',
                    label1:'Kiểu hiển thị',
                    viewTypeOpt1:'Chỉ hiển thị mô tả',
                    viewTypeOpt2:'Ảnh chữ ký và mô tả',
                    viewTypeOpt3:'Chỉ hiển thị ảnh',
                    label2:'Tùy chọn hình hảnh',
                    label3:'Cỡ chữ hiển thị',
                    modalTitle1:'Thêm ảnh chữ ký',
                    modalTitle2:'Thêm comment',
                    labelTextView:'Trang hiển thị',
                    labelContentView:'Nội dung hiển thị',
                    cancel:'Huỷ',
                    confirm:'Xác nhận',
                    fontSize:'Cỡ chữ',
                    sign:'Ký dữ liệu',
                    vi:'Tiếng Việt',
                    en:'Tiếng Anh',
                }
            }
            add.text(properties_lang.add);
            logoText.text(properties_lang.logoText);
            legend_1.text(properties_lang.legend_1);
            legend_2.text(properties_lang.legend_2);
            adv_text.text(properties_lang.adv_text);
            label1.text(properties_lang.label1);
            viewTypeOpt1.text(properties_lang.viewTypeOpt1);
            viewTypeOpt2.text(properties_lang.viewTypeOpt2);
            viewTypeOpt3.text(properties_lang.viewTypeOpt3);
            label2.text(properties_lang.label2);
            label3.text(properties_lang.label3);
            modalTitle1.text(properties_lang.modalTitle1);
            modalTitle2.text(properties_lang.modalTitle2);
            labelTextView.text(properties_lang.labelTextView);
            labelContentView.text(properties_lang.labelContentView);
            cancel.text(properties_lang.cancel);
            confirm.text(properties_lang.confirm);
            fontSize.text(properties_lang.fontSize);
            sign.text(properties_lang.sign);
            sign1.text(properties_lang.sign);
            cancel1.text(properties_lang.cancel);
            langOption1.text(properties_lang.vi);
            langOption2.text(properties_lang.en);
            console.log('demo'+$(this).val());

        });
    };

    VnptPdf.prototype.updateSignatureTextEvent = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.visibleText = evt.target.value;
        self.settings.useDefaultText = false;
        self.setVisibleText();
    };

    VnptPdf.prototype.setVisibleText = function () {
        let htmlInner = '<span>' + this.settings.visibleText.replace(/(?:\r\n|\r|\n)/g, '<br>') + '</span>';
        $('.sig-text').html(htmlInner);
        if (!this.settings.useDefaultText) {
            $('#useDefaultText').prop('checked', false); 
        }
    };

    VnptPdf.prototype.changeVisibleTextDefault = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.useDefaultText = evt.target.checked;
    };

    VnptPdf.prototype.changeSignatureFontNameEvent = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.fontName = evt.target.value;
        self.setFontName();
    };

    VnptPdf.prototype.setFontName = function () {
        $('.signaturebox').css('font-family', this.getFontFamily(this.settings.fontName));
        //$('.pdf-comment span').css('font-family', this.getFontFamily());
    };

    VnptPdf.prototype.getFontFamily = function (family) {
        switch (family) {
            case 'Time':
                return '"Times New Roman", Times, serif';
            case 'Roboto':
                return 'Roboto';
            case 'Arial':
                return 'Arial, Helvetica, sans-serif';
            default:
                return '"Times New Roman", Times, serif';
        }
    };

    VnptPdf.prototype.changeFontStyleEvent = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.fontStyle = evt.target.value;
        self.setFontStyle(self.settings.fontStyle);
    };

    /**
     * */
    VnptPdf.prototype.setFontStyle = function () {
        $('.font-style').css('font-weight', '');
        $('.font-style').css('font-style', '');
        $('.font-style').css('font-decoration', '');
        switch ('' + this.settings.fontStyle) {
            case '1':
                $('.font-style').css('font-weight', 'bold');
                break;
            case '2':
                $('.font-style').css('font-style', 'italic');
                break;
            case '3':
                $('.font-style').css('font-style', 'italic');
                $('.font-style').css('font-weight', 'bold');
                break;
            case '4':
                $('.font-style').css('font-decoration', 'underline');
                break;
        }

        $('#sign-font-style-select').find(":selected").css('font-style', 'italic');
    };

    /**
     * 
     * @param {any} evt Change color event
     */
    VnptPdf.prototype.changeFontColorEvent = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.fontColor = evt.target.value;
        self.setFontColor();
    };

    /**
     * */
    VnptPdf.prototype.setFontColor = function () {
        $('.signaturebox').css('color', '#' + this.settings.fontColor);
        //$('.pdf-comment span').css('color', '#' + this.settings.fontColor);
    };

    /**
     * Handle change visible type radio button checked
     * @param {any} evt Radio button checked event
     */
    VnptPdf.prototype.changeSignatureVisibleTypeEvent = function (evt) {
        const self = evt.data.msgTarget;
        self.settings.visibleType = parseInt('' + evt.target.value);
        self.changeSignatureVisibleType();
    };

    /**
     * Handle change text align option
     * @param {any} evt Radio button checked event
     */
    //VnptPdf.prototype.changeTextAlignOptionEvent = function (evt) {
    //    const self = evt.data.msgTarget;
    //    self.settings.TextAlign = parseInt('' + evt.target.value);
    //    console.log(self.settings)
    //    console.log(evt.target.value);
    //    self.changeTextAlignOption();
    //};


    /**
     * Change signature visible type
     * */
    VnptPdf.prototype.changeSignatureVisibleType = function () {
        const boxHtml = this.getSignatureVisibleElement(this.settings.visibleType);
        const self = this;
        this.settings.signatures.forEach(function (box) {
            if (typeof box.element === 'undefined') {
                return;
            }
            let boxContent = box.element.find('.sign-box-content');
            boxContent.empty();
            boxContent.html(boxHtml);
            self.setVisibleText();
            self.setFontName();
            self.setFontStyle();
            self.setFontSize();
            self.setFontColor();
        });
    };

    //VnptPdf.prototype.changeTextAlignOption = function () {
    //    const value = $('input[name="textAlign"]:checked')[0].value;
    //    console.log(value);
    //    if (value == 0) $(".sig-text").css('text-align', 'left');
    //    if (value == 1) $(".sig-text").css('text-align', 'center');
    //    if (value == 2) $(".sig-text").css('text-align', 'right');
    //};

    VnptPdf.prototype.setFontSize = function () {
        const dpi = document.getElementById('dpi').offsetWidth;
        const size = Math.ceil(this.settings.fontSize * dpi / 72);
        $('.signaturebox').css('font-size', size + 'px');
        //$('.pdf-comment span').css('font-size', size + 'px');
    };

    VnptPdf.prototype.changeSignaturePageEvent = function (evt) {
        const self = evt.data.msgTarget;
        const p = Number($('#pdf-sign-page').val());
        if (isNaN(p) || p < 1 || p > self.pdfPages.length) {
            alert("Trang đặt chữ ký không hợp lệ. (Số trang từ 1 đến " + self.pdfPages.length + ")");
            return;
        }

        self.settings.sigPage = p;
        self.initSignatureBox();

    };

    /**
     * 
     * @param {any} evt Select file event
     */
    VnptPdf.prototype.changeSignatureImageEvent = function (evt) {
        const self = evt.data.msgTarget;
        $(document).on(
            'change',
            '#pdf-sign-image-file :file',
            function (event) {
                if (!$(this).get(0).files) {
                    console.log('null');
                    return;
                }

                var input = $(this), numFiles = input.get(0).files ? input
                    .get(0).files.length : 1, label = input.val().replace(
                        /\\/g, '/').replace(/.*\//, '');
                $('#pdf-sign-img-name').val(label);
                var f = input.get(0).files[0];

                var reader = new FileReader();
                reader.addEventListener("load", function () {
                    var prefix = ("" + this.result).substr(0, ("" + this.result).indexOf("base64,") + 7);
                    self.settings.signatureImg = this.result.replace(prefix, "");
                    self.changeSignatureVisibleImg();
                });
                if (f) {
                    reader.readAsDataURL(f);
                }
            });
    };

    /**
     * */
    VnptPdf.prototype.changeSignatureVisibleImg = function () {
        const style = $('#vnptpdf-style');
        if (style) {
            style.remove();
        }
        const styleElem = document.head.appendChild(document.createElement("style"));
        styleElem.innerHTML = ".signature-img::before{background-image: url(data:image/png;base64," + this.settings.signatureImg + ");background-position: center;}";
    };

    /**
     * 
     * @param {any} sig Signature instance 
     * @param {any} index signature page index
     */
    VnptPdf.prototype.initSignature = function (sig, index) {
        const sigHtml = this.getSignatureVisibleElement(this.settings.visibleType).replace('signature_', 'signature_' + index);
        const sigElement = $(_signatureBox).appendTo(this.wrapper.find('.pdf-page'));
        sigElement.find('.sign-box-content').empty();
        sigElement.find('.sign-box-content').html(sigHtml);
        sig.element = sigElement;

        sig.urx = sig.x + sig.width;
        sig.ury = sig.y + sig.height;

        const sigRow = $('<tr></tr>').appendTo('#pdf-signatures-table>tbody');
        sig.signatureRow = sigRow;
        sigRow.append('<td>' + (this.settings.signatures.indexOf(sig) + 1) + '</td>');
        sigRow.append('<td class="sig-rectangle">[' + sig.x + ',' + sig.y + ',' + sig.urx + ',' + sig.ury + ']</td >');
        sigRow.append('<td>' + sig.page + '</td>');

        const actionCell = $('<td class="comment-act">' + _trashIcon + '</td>').appendTo(sigRow);
        actionCell.click({ msgTarget: this, elmentTarget: sig }, this.removeSignature);


        const page = sig.page;
        const pdfPage = $('#pdfPage_' + page);
        const boundX = pdfPage[0].offsetLeft;
        const boundY = pdfPage[0].offsetTop;
        const pageHeight = Math.ceil(this.pdfPages[page - 1].height);
        const x = sig.x;
        const y = sig.y;
        const height = sig.height;
        const width = sig.width;
        const dpi = document.getElementById('dpi').offsetWidth;

        var yPos = Math.floor((pageHeight - y - height) * dpi / 72) + 9 - 4 + boundY;
        var xPos = boundX + 9 + Math.floor(x * dpi / 72);
        var h = Math.floor(height * dpi / 72);
        var w = Math.floor(width * dpi / 72);
        sig.element.css({ 'top': yPos, 'left': xPos, 'height': h, 'width': w, 'position': 'absolute' });
        sig.element.show();

        sig.element.draggable({
            containment: pdfPage,
            drag: function () {
                const boundX = pdfPage[0].offsetLeft;
                const boundY = pdfPage[0].offsetTop;
                const top = sig.element[0].offsetTop;
                const left = sig.element[0].offsetLeft;
                const xPos = Math.floor((left - boundX - 9) / dpi * 72);
                sig.x = xPos;
                const h = Math.floor(sig.element[0].offsetHeight / dpi * 72);
                const yPos = pageHeight - Math.ceil((top - boundY - 9) / dpi * 72) - h;
                sig.y = yPos;
                sig.urx = sig.x + sig.width;
                sig.ury = sig.y + sig.height;
                sig.signatureRow.find('.sig-rectangle').text('[' + sig.x + ',' + sig.y + ',' + sig.urx + ',' + sig.ury + ']');
            },
            stop: function () {
            }
        })
            .resizable({
                resize: function (event, ui) {
                    var w = Math.floor(sig.element[0].offsetWidth / dpi * 72);
                    var h = Math.floor(sig.element[0].offsetHeight / dpi * 72);
                    sig.width = w;
                    sig.height = h;
                    sig.urx = sig.x + sig.width;
                    sig.ury = sig.y + sig.height;
                    sig.signatureRow.find('.sig-rectangle').text('[' + sig.x + ',' + sig.y + ',' + sig.urx + ',' + sig.ury + ']');
                },
                stop: function (event, ui) {
                }
            });

        pdfPage.droppable({
            accept: sig.element,
            over: function () {
                sig.element.draggable('option', 'containment', $(this));
            }
        });

        //const self = this;
        //window.addEventListener('resize', function () {
        //    self.windowResizeEventHandle();
        //});
        this.setFontColor();
        this.setFontSize();
        this.setFontStyle();
        this.setFontName();
        this.setVisibleText();
    };

    /**
     * 
     * @param {any} type String signature visible type
     * @returns {any} html signature box
     */
    VnptPdf.prototype.getSignatureVisibleElement = function (type) {
        let html = '';
        switch (type) {
            case 0:
                html = _textOnly;
                break;
            case 1:
                html = _textandLogoLeft;
                break;
            case 2:
                html = _logoOnly;
                break;            
        }

        return html;
    };

    /**
     * */
    VnptPdf.prototype.initSignatureBoxEvent = function () {
        const dpi = document.getElementById('dpi').offsetWidth;
        const page = this.settings.sigPage;
        const pageHeight = Math.ceil(this.pdfPages[page - 1].height);
        const pdfPage = $('#pdfPage_' + page);
        const signBox = this.signatureBox;
        const self = this;

        signBox
            .draggable({
                containment: pdfPage,
                drag: function () {
                    const boundX = pdfPage[0].offsetLeft;
                    const boundY = pdfPage[0].offsetTop;
                    const top = signBox[0].offsetTop;
                    const left = signBox[0].offsetLeft;
                    const xPos = Math.floor((left - boundX - 9) / dpi * 72);
                    self.settings.x = xPos;

                    const h = Math.floor(signBox[0].offsetHeight / dpi * 72);
                    const yPos = pageHeight - Math.ceil((top - boundY - 9) / dpi * 72) - h;
                    self.settings.y = yPos;
                    $('#signbox-xpos').val(xPos);
                    $('#signbox-ypos').val(yPos);

                },
                stop: function () {
                }
            })
            .resizable({
                resize: function (event, ui) {
                    var w = Math.floor(signBox[0].offsetWidth / dpi * 72);
                    var h = Math.floor(signBox[0].offsetHeight / dpi * 72);
                    self.settings.width = w;
                    self.settings.height = h;
                    $('#signbox-width').val(w);
                    $('#signbox-height').val(h);
                },
                stop: function (event, ui) {
                }
            });

        pdfPage.droppable({
            accept: signBox,
            over: function () {
                signBox.draggable('option', 'containment', $(this));
            }
        });
    };

    VnptPdf.prototype.initSignatures = function () {
        const self = this;
        self.settings.signatures.forEach(function (sig, index) {
            if (sig.page > self.pdfPages.length) {
                console.error('[Error] Signature page invalid.');
                $('#pdf-signatures-error').text('[Error] Signature page invalid.');
                return;
            }
            self.initSignature(sig, index);
        });
    };

    VnptPdf.prototype.initDefaultSignature = function () {
        if (this.settings.signatures === null || this.settings.signatures.length === 0) {
            const pageHeight = Math.ceil(this.pdfPages[0].height);
            this.settings.signatures = [{
                x: 20, // bottom_left x value
                y: pageHeight - 120 - 9 - 80, // bottom_left y value
                width: 220,
                height: 80,
                page: this.pdfPages.length // mặc định để trang cuối
            }];
        }
    };

    VnptPdf.prototype.initComments = function () {
        const self = this;
        this.settings.comments.forEach(function (comment) {
            if (comment.page > self.pdfPages.length) {
                console.error('[Error] Comment page invalid.');
                $('#pdf-comments-error').text('[Error] Comment page invalid.');
                return;
            }
            self.initComment(comment);
        });
    };

    VnptPdf.prototype.initComment = function (comment) {
        const com = _comment.replace('COMMENT', comment.text);
        const commentElement = $(com).appendTo(this.wrapper.find('.pdf-page'));
        comment.element = commentElement;
        if (typeof comment.fontSize === 'undefined') {
            comment.fontSize = 13;
        }
        if (typeof comment.fontName === 'undefined') {
            comment.fontName = 'Time';
        }
        if (typeof comment.fontStyle === 'undefined') {
            comment.fontStyle = 0;
        }

        const commentRow = $('<tr></tr>').appendTo('#pdf-comments-table>tbody');
        comment.commentRow = commentRow;
        commentRow.append('<td>' + (this.settings.comments.indexOf(comment) + 1) + '</td>');
        commentRow.append('<td>' + comment.text + '</td >');
        commentRow.append('<td>' + comment.page + '</td>');

        const actionEditCell = $('<td class="comment-act">' + _editIcon + '</td>').appendTo(commentRow);
        actionEditCell.click({ msgTarget: this, elmentTarget: comment }, this.editComment);

        const actionCell = $('<td class="comment-act">' + _trashIcon + '</td>').appendTo(commentRow);
        actionCell.click({ msgTarget: this, elmentTarget: comment }, this.removeComment);

        const pdfPage = $('#pdfPage_' + comment.page);
        const boundX = pdfPage[0].offsetLeft;
        const boundY = pdfPage[0].offsetTop;
        const pageHeight = Math.ceil(this.pdfPages[comment.page - 1].height);
        const dpi = document.getElementById('dpi').offsetWidth;

        const x = comment.x || 50;
        const y = comment.y || 50;
        const width = comment.width || 200;
        const height = comment.height || 15;

        var yPos = (pageHeight - y - height) * dpi / 72 + 9 - 4 + boundY;
        var xPos = boundX + 9 + Math.floor(x * dpi / 72);
        var h = Math.floor(height * dpi / 72);
        var w = Math.floor(width * dpi / 72);
        //var h = height * dpi / 72;
        //var w = width * dpi / 72;
        comment.element.css({ 'top': yPos, 'left': xPos, 'height': h, 'width': w, 'position': 'absolute' });
        comment.element.show();

        comment.element.draggable({
            containment: pdfPage,
            drag: function () {
                const boundX = pdfPage[0].offsetLeft;
                const boundY = pdfPage[0].offsetTop;
                const top = comment.element[0].offsetTop;
                const left = comment.element[0].offsetLeft;
                const xPos = Math.floor((left - boundX - 9) / dpi * 72);
                comment.x = xPos;
                const h = Math.floor(comment.element[0].offsetHeight / dpi * 72);
                const yPos = pageHeight - (top - boundY - 9+4) / dpi * 72 - h;
                comment.y = Math.floor(yPos);
            },
            stop: function () {
            }
        })
            .resizable({
                resize: function (event, ui) {
                    var w = Math.floor(comment.element[0].offsetWidth / dpi * 72);
                    var h = Math.floor(comment.element[0].offsetHeight / dpi * 72);
                    comment.width = w;
                    comment.height = h;
                },
                stop: function (event, ui) {
                }
            });

        pdfPage.droppable({
            accept: comment.element,
            over: function () {
                comment.element.draggable('option', 'containment', $(this));
            }
        });
        let commentTextElement = commentElement.find('span');
        let w3 = 'normal';
        let s = 'normal';
        switch ('' + comment.fontStyle) {
            case '1':
                w3 = 'bold';
                s = 'normal';
                break;
            case '2':
                s = 'italic';
                break;
            case '3':
                s = 'italic';
                w3 = 'bold';
                break;
            case '4':
                break;
        }
        const size = Math.ceil(comment.fontSize * dpi / 72);
        commentTextElement.css({
            'font-family': this.getFontFamily(comment.fontName),
            'font-size': size,
            'color': '#' + comment.fontColor
        });
        commentElement.css({
            'font-style': s,
            'font-weight': w3
        });
    };

    VnptPdf.prototype.editComment = function (evt) {
        const self = evt.data.msgTarget;
        const comment = evt.data.elmentTarget;

        let addCommentModal = document.getElementById('add-comment-modal');
        $('#comment-text').val(comment.text);
        $('#comment-text-page').val(comment.page);
        $('#com-font-name').val(comment.fontName);
        $('#com-font-style').val(comment.fontStyle);
        $('#comment-font-color').val(comment.fontColor);
        $('#com-font-size').val(comment.fontSize);
        $('#com-font-size').asRange();
        $('#com-font-size').asRange('set', '' + comment.fontSize);
        jscolor.installByClassName("jscolor");
        $('#comment-font-color').addClass('jscolor-active');
        $('#comment-font-color').css('background-color', '#' + comment.fontColor);
        addCommentModal.style.display = "block";
        $('#add-comment-modal').find('#com-add').click(function () {
            self.editCommentHandle(comment);
        });
        $('#add-comment-modal').find('#com-close').click(function () {
            $("#add-comment-modal").find('#com-add').off("click");
            addCommentModal.style.display = "none";
        });

        const span = addCommentModal.getElementsByClassName("pdf-modal-close")[0];
        span.onclick = function () {
            addCommentModal.style.display = "none";
        };
    };

    VnptPdf.prototype.editCommentHandle = function (comment) {
        const text = $('#comment-text').val();
        if ('' === text) {
            alert('Nhập nội dung comment để tiếp tục');
            return;
        }

        const p = Number($('#comment-text-page').val());
        if (isNaN(p) || p < 1 || p > this.pdfPages.length) {
            alert("Trang đặt comment không hợp lệ. (Số trang từ 1 đến " + this.pdfPages.length + ")");
            return;
        }
        comment.page = p;
        comment.text = text;
        comment.fontSize = $('#com-font-size').asRange('get');
        comment.fontName = $('#com-font-name').val();
        comment.fontStyle = $('#com-font-style').val();
        comment.fontColor = $('#comment-font-color').val();
        this.settings.comments.forEach(function (comm) {
            comm.element.remove();
            comm.commentRow.remove();
        });
        this.initComments();
        $("#add-comment-modal").find('#com-add').off("click");
        document.getElementById('add-comment-modal').style.display = "none";
    };

    VnptPdf.prototype.removeComment = function (evt) {
        const self = evt.data.msgTarget;
        const comment = evt.data.elmentTarget;
        if (!confirm("Xác nhận xóa comment '" + comment.text + "'")) {
            return;
        }
        let temp = [];
        self.settings.comments.forEach(function (comm) {
            comm.element.remove();
            comm.commentRow.remove();
            if (comm === comment) {
                comm.element = null;
            } else {
                temp.push(comm);
            }
        });
        self.settings.comments = temp;
        self.initComments();
    };

    VnptPdf.prototype.removeSignature = function (evt) {
        const self = evt.data.msgTarget;
        const sig = evt.data.elmentTarget;
        if (!confirm("Xác nhận xóa hình ảnh chữ ký")) {
            return;
        }
        let temp = [];
        self.settings.signatures.forEach(function (comm) {
            comm.element.remove();
            comm.signatureRow.remove();
            if (comm === sig) {
                comm.element = null;
            } else {
                temp.push(comm);
            }
        });
        self.settings.signatures = temp;
        self.initSignatures();
    };

    /**
     * 
     * @param {any} evt Add signature comment event
     */
    VnptPdf.prototype.addComment = function (evt) {
        let addCommentModal = document.getElementById('add-comment-modal');
        jscolor.installByClassName("jscolor");
        const self = evt.data.msgTarget;
        $('#add-comment-modal').find('#com-add').click(function () {
            self.addCommentHandle();
        });
        $('#add-comment-modal').find('#com-close').click(function () {
            $("#add-comment-modal").find('#com-add').off("click");
            addCommentModal.style.display = "none";
        });
        addCommentModal.style.display = "block";
        $('#com-font-size').asRange();

        const span = addCommentModal.getElementsByClassName("pdf-modal-close")[0];
        span.onclick = function () {
            $("#add-comment-modal").find('#com-add').off("click");
            addCommentModal.style.display = "none";
        };
    };

    VnptPdf.prototype.addCommentHandle = function () {
        const self = this;
        const text = $('#comment-text').val();
        if ('' === text) {
            alert('Nhập nội dung comment để tiếp tục');
            return;
        }

        const p = Number($('#comment-text-page').val());
        if (isNaN(p) || p < 1 || p > self.pdfPages.length) {
            alert("Trang đặt comment không hợp lệ. (Số trang từ 1 đến " + self.pdfPages.length + ")");
            return;
        }

        let comm = {
            x: 50,
            y: 500,
            width: 200,
            height: 20,
            page: p,
            text: text,
            fontColor: $('#comment-font-color').val(),
            fontSize: $('#com-font-size').asRange('get'),
            fontName: $('#com-font-name').val(),
            fontStyle: $('#com-font-style').val()
        };

        self.settings.comments.push(comm);
        self.initComment(comm);
        $('#comment-text').val('');
        $('#comment-text-page').val('');
        $("#add-comment-modal").find('#com-add').off("click");
        document.getElementById('add-comment-modal').style.display = "none";
    };

    /**
     * 
     * @param {any} evt Add signature comment event
     */
    VnptPdf.prototype.addSignature = function (evt) {
        let addSignatureModal = document.getElementById('add-signature-modal');
        addSignatureModal.style.display = "block";
        window.onclick = function (event) {
            if (event.target === addSignatureModal) {
                addSignatureModal.style.display = "none";
            }
        };
        const span = addSignatureModal.getElementsByClassName("pdf-modal-close")[0];
        span.onclick = function () {
            addSignatureModal.style.display = "none";
            addSignatureModal.style.display = "none";
        };
    };

    VnptPdf.prototype.addSignatureHandle = function () {
        const self = this;
        const p = Number($('#sig-text-page').val());
        if (isNaN(p) || p < 1 || p > self.pdfPages.length) {
            alert("Trang đặt ảnh chữ ký không hợp lệ. (Số trang từ 1 đến " + self.pdfPages.length + ")");
            return;
        }

        let comm = {
            x: 50,
            y: 500,
            width: 200,
            height: 100,
            page: p
        };

        self.settings.signatures.push(comm);
        self.initSignature(comm);
        $('#sig-text-page').val('');
        document.getElementById('add-signature-modal').style.display = "none";
    };

    /**
     * */
    VnptPdf.prototype.windowResizeEventHandle = function () {
        if (!this.show) {
            return;
        }
        const page = this.settings.sigPage;
        const pdfPage = $('#pdfPage_' + page);
        const boundX = pdfPage[0].offsetLeft;
        const boundY = pdfPage[0].offsetTop;
        const pageHeight = this.pdfPages[page - 1].height;
        const x = this.settings.x;
        const y = this.settings.y;
        const height = this.settings.height;
        const dpi = document.getElementById('dpi').offsetWidth;

        var yPos = Math.floor((pageHeight - y - height) * dpi / 72) + 9 - 4 + boundY;
        var xPos = boundX + 9 + Math.floor(x * dpi / 72);
        this.signatureBox.css({ 'top': yPos, 'left': xPos });
        console.log(boundX);
        this.settings.comments.forEach(function (comment) {
            const xPos1 = boundX + 9 + Math.floor(comment.x * dpi / 72);
            const yPos1 = Math.floor((pageHeight - comment.y - comment.height) * dpi / 72) + 9 - 4 + boundY;
            comment.element.css({ 'top': yPos1, 'left': xPos1 });
        });
    };

    /**
     * 
     * @param {any} evt Final function
     */
    VnptPdf.prototype.complete = function (evt) {
        const self = evt.data.msgTarget;
        self.show = false;
        self.wrapper.empty();
		// signAdvanceAfterView(self.getPdfSignatureOptions());
        self.CallBack(self.getPdfSignatureOptions());
    };

    VnptPdf.prototype.reject = function (evt) {
        const self = evt.data.msgTarget;
        self.show = false;
        self.wrapper.empty();
    };

    /**
     * @return {any} json object
     * */
    VnptPdf.prototype.getPdfSignatureOptions = function () {
		let sigOptions = new PdfSigner();			
		sigOptions.ImageBase64 = this.settings.signatureImg;
		sigOptions.SigColorRGB = '0,0,0';
		sigOptions.SigTextSize = this.settings.fontSize;
		sigOptions.AdvancedCustom = true;
		sigOptions.AdvancedWithoutDisplay = true;
		sigOptions.SigType = this.settings.visibleType;
		sigOptions.SigVisible = true;		
		sigOptions.SigSignerVisible = true;		
		sigOptions.sigBold = false;
		sigOptions.ValidationOption = false;
		
		let signatures = [];
		this.settings.signatures.forEach(function (sig) {
            signatures.push({
                rectangle: "" + sig.x + "," + sig.y + "," + Math.floor(sig.x + sig.width) + "," + Math.floor(sig.y + sig.height),
				llx: sig.x,
				lly: sig.y,
				urx: Math.floor(sig.x + sig.width),
				ury: Math.floor(sig.y + sig.height),
                page: sig.page,				
            });
        });
		sigOptions.listSignature = signatures;
		
		let comments = [];
		this.settings.comments.forEach(function (comment) {
            comments.push({
                Description: comment.text,                
                page: comment.page,
				llx: comment.x,
				lly: comment.y,
				urx: Math.floor(comment.x + comment.width),
				ury: Math.floor(comment.y + comment.height),				                                
                commentFontSize: comment.fontSize,
				OnlyDescription: true
                //fontColor: this.settings.fontColor
            });
        });
		sigOptions.listComment = comments;
		
		
		/*
        const signRectangle = "" + this.settings.x + "," + this.settings.y + "," + (this.settings.x + this.settings.width) + "," + (this.settings.y + this.settings.height);										
        let comments = [];
        this.settings.comments.forEach(function (comment) {
            comments.push({
                text: comment.text,
                rectangle: "" + comment.x + "," + comment.y + "," + Math.floor(comment.x + comment.width) + "," + Math.floor(comment.y + comment.height),
                page: comment.page,
                fontName: comment.fontName,
                fontStyle: comment.fontStyle,
                fontSize: comment.fontSize,
                fontColor: comment.fontColor
            });
        });

        console.log(this.settings.visibleText);

        let signatures = [];
        this.settings.signatures.forEach(function (sig) {
            signatures.push({
                rectangle: "" + sig.x + "," + sig.y + "," + Math.floor(sig.x + sig.width) + "," + Math.floor(sig.y + sig.height),
                page: sig.page
            });
        });
		

        let res = {
            fontName: this.settings.fontName,
            fontSize: this.settings.fontSize,
            fontColor: this.settings.fontColor,
            fontStyle: this.settings.fontStyle,
            imageSrc: this.settings.signatureImg,
            visibleType: this.settings.visibleType,
            comment: Base64.encode(JSON.stringify(comments)),
            signatures: Base64.encode(JSON.stringify(signatures)),
            TextAlign: this.settings.TextAlign
        };
        console.log(this.settings.useDefaultText);
        if (!this.settings.useDefaultText) {
            res = $.extend(true, { signatureText: this.settings.visibleText.replace(/\n/g, "\\n")}, res);
        }
		*/
        return sigOptions;
    };

    /**
     * 
     * @param {any} base64 base64 encoded
     * @return {any} byte array
     */
    VnptPdf.prototype.convertDataURIToBinary = function (base64) {
        var raw = window.atob(base64);
        var rawLength = raw.length;
        var array = new Uint8Array(new ArrayBuffer(rawLength));

        for (i = 0; i < rawLength; i++) {
            array[i] = raw.charCodeAt(i);
        }
        return array;
    };

    // 
    $.fn[pluginName] = function (options) {
        var vnptPdf;
        if (!$.data(this, pluginName)) {
            vnptPdf = new VnptPdf(this, options);
            $.data(this, pluginName, vnptPdf);
        }
        return vnptPdf;
    };

    const pdfWorkingArea =
        '<div class="pdf-working-area">' +

        '<nav class="site-navbar navbar navbar-default navbar-fixed-top navbar-mega" role="navigation">' +
        '      <div class="navbar-header">' +
        '        <div class="navbar-brand navbar-brand-center site-gridmenu-toggle" data-toggle="gridmenu">' +
        '          <img class="navbar-brand-logo" src="data:image/png;base64,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" title="VNPT-Kyso">' +
        '          <span class="navbar-brand-text hidden-xs-down" data-label="logo-text"> '+properties_lang.logoText+'</span>' +
        '        </div>' +
        '      </div>' +
        '    ' +
        '      <div class="navbar-container container-fluid">' +
        '        <!-- Navbar Collapse -->' +
        '        <div class="collapse navbar-collapse navbar-collapse-toolbar" id="site-navbar-collapse">' +
        '          <!-- Navbar Toolbar -->' +
        '          <ul class="nav navbar-toolbar">' +
        '            ' +
        '          </ul>' +
        '          <!-- End Navbar Toolbar -->' +
        '    ' +
        '          <!-- Navbar Toolbar Right -->' +
        '          <ul class="nav navbar-toolbar navbar-right navbar-toolbar-right">' +
        '            ' +
        '          </ul>' +
        '          <!-- End Navbar Toolbar Right -->' +
        '        </div>' +
        '        <!-- End Navbar Collapse -->' +
        '      </div>' +
        '    </nav>' +

        '    <div class="pdf-action-menu page-aside-left">' +
        '        <div class="pdf-action-menu-content"><br/><br/>' +
        '            <div class="lang-box form-group">'+
        '               <select name="sel-change-lang" id="sel-change-lang" class="sign-visible-types" style="max-width:160px;">' +
        '                  <option value="0" data-label="vi">'+properties_lang.vi+'</option>' +
        '                  <option value="1" data-label="en">'+properties_lang.en+'</option>' +
        '               </select>' +
        '            </div>'+
        '            <fieldset>' +
        '                <legend data-label="legend_1">'+properties_lang.legend_1+'</legend>' +
        '                <div class="pdf-input-group">' +
        '                    <div class="pdf-size-row">' +
        '                        <div id="pdf-signatures">' +
        '                            <table class="table-striped" id="pdf-signatures-table" cellspacing="0">' +
        '                               <tbody>' +
        '                               </tbody>' +
        '                            </table>' +
        '                            <div class="pdf-size-row">' +
        '                               <label id="pdf-signatures-error" class="error"></label>' +
        '                            </div>' +
        '                            <div class="group-box-adv">'+
        '                               <button class="pdf-btn pdf-btn-second" id="add-sig-btn" data-label="add">+ '+properties_lang.add+'</button>' +
        
        '                            </div>'+
        '                        </div>' +
        '                    </div>' +
        '                </div>' +
        '                <a class="pdf-collapsible" href="javascript:void(0)"  data-label="adv_text">'+properties_lang.adv_text+'</a>' +
        '                <div class="pdf-collapse-content" style="">' +
        '                <div style="display:none">' +
        '                   <label  data-label="labelContentView">'+properties_lang.labelContentView+':</label>' +
        '                    <div class="pdf-input-group">' +
        '                        <textarea id="pdf-sign-text" rows="4" type="text" class="" style="width: calc(100% - 20px);"></textarea>' +
        '                    </div>' +
        '                    <label class="checkbox-container">Hiển thị nội dung mặc định' +
        '                        <input id="useDefaultText" type="checkbox" checked="checked" value="1">' +
        '                          <span class="checkmark"></span>' +
        '                    </label>' +          
        '                </div >' +
        '                <div class="form-group">' +
        '                    <label class="label-text"  data-label="label1">'+properties_lang.label1+':</label>' +
        '                    <select name="sign-visible-type" id="sign-visible-type-select" class="sign-visible-types">' +
        '                      <option value="0"  data-label="viewTypeOpt1">1. '+properties_lang.viewTypeOpt1+'</option>' +
        '                      <option value="1"  data-label="viewTypeOpt2">2. '+properties_lang.viewTypeOpt2+'</option>' +
        '                      <option value="2"  data-label="viewTypeOpt3">3. '+properties_lang.viewTypeOpt3+'</option>' +        
        '                    </select>' +
        '                </div>' +
        '                <div  class="form-group">' +
        '                    <label class="label-text" data-label="label2">'+properties_lang.label2+':</label>' +
        '                    <div class="pdf-input-group-upload">' +
        '                        <input id="pdf-sign-img-name" type="text" class="pdf-file-name"' +
        '                               readonly="readonly">' +
        '                        <span class="pdf-input-group-btn">' +
        '                            <span class="pdf-btn pdf-btn-second pdf-btn-file" id="pdf-sign-image-file">' +
        '                                ... <input id="signature-img-btn" name="SetupFile" type="file"' +
        '                                           accept="image/x-png,image/gif,image/jpeg" required>' +
        '                            </span>' +
        '                        </span>' +
        '                    </div>' +
        '                </div>' +        
        '                <div class="form-group">' +
        '                    <label class="label-text" data-label="label3">'+properties_lang.label3+':</label><br />' +
        '                    <input id="sig-font-size" class="example" type="range" min="5" max="15" name="points" step="1" />' +
        '                </div >' +
        '                </div>' +
        '            </fieldset>' +
        '            <fieldset>' +
        '                <legend data-label="legend_2">'+properties_lang.legend_2+'</legend>' +
        '                <div class="pdf-input-group">' +
        '                    <div class="pdf-size-row">' +
        '                        <div id="pdf-comments">' +
        '                            <table class="table-striped" id="pdf-comments-table" cellspacing="0">' +
        '                               <tbody>' +
        '                               </tbody>' +
        '                            </table>' +
        '                            <div class="pdf-size-row">' +
        '                               <label id="pdf-comments-error" class="error"></label>' +
        '                            </div>' +
        '                            <button class="pdf-btn pdf-btn-second" data-label="add" id="add-comment-btn">+ Thêm</button>' +
        '                        </div>' +
        '                    </div>' +
        '                </div>' +
        '            </fieldset>' +
        '            <div id="action-btns" class=group-buttons>' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="pdf-page">' +
        '        <div id="dragThis">' +
        '             <div id="sign-box-content"></div>' +
        '        </div>' +
        '    </div>' +
        '</div>';
    var _canvasPdf = '<canvas id="ID_VALUE" class="pdf-viewport"></canvas><br/>';

    const _menuSwitch =
        '<div class="page-aside-switch">' +
        '	<i class="icon md-chevron-left" aria-hidden="true"><</i>' +
        '	<i class="icon md-chevron-right" aria-hidden="true">></i>' +
        '</div>';

    const _signatureBox =
        '        <div id="signature_" class="signature-view font-style">' +
        '             <div class="sign-box-content">' +
        '             </div > ' +
        '        </div>';

    const _textOnly =
        '                 <div id="" class="signaturebox">' +
        '                     <div class="signaturebox-text-only sig-text">' +
        '                         <span>Ky boi: Ten chu chung thu</span><br />' +
        '                         <span>Ngay ky: 18/03/2019</span>' +
        '                     </div>' +
        '        </div>';

    const _textandLogoLeft =
        '    <div id="" class="signaturebox">' +
        '        <div class="signaturebox-image-left">' +
        '            <div class="sig-text">' +
        '                <span>Ky boi: Ten chu chung thu</span><br />' +
        '                <span>Ngay ky: 18/03/2019</span>' +
        '            </div>' +
        '            <div class="signature-img signaturebox-image-left-img">' +
        '            </div>' +
        '             </div > ' +
        '        </div>';
    const _logoOnly =
        '                 <div id="" class="signaturebox">' +
        '        <div class="signature-img signaturebox-image-only">' +
        '        </div>' +
        '        </div>';
    const _textAndLogoTop =
        '    <div id="" class="signaturebox">' +
        '        <div class="signaturebox-image-top">' +
        '            <div class="sig-text">' +
        '                <span>Ky boi: Ten chu chung thu</span><br />' +
        '                <span>Ngay ky: 18/03/2019</span>' +
        '            </div>' +
        '            <div class="signature-img signaturebox-image-top-img">' +
        '            </div>' +
        '        </div>' +
        '        </div>';
    const _textAndBackground =
        '    <div id="" class="signaturebox">' +
        '        <div class="signature-img signaturebox-textonly">' +
        '            <div class="sig-text">' +
        '                <span>Ky boi: Ten chu chung thu</span><br />' +
        '                <span>Ngay ky: 18/03/2019</span>' +
        '            </div>' +
        '             </div>' +
        '        </div>';
    const _addCommentModal =
        '<div id="add-comment-modal" class="pdf-modal">' +
        '        <div class="pdf-modal-content pdf-modal-dialog" style="max-width:480px;">' +
        '            <div class="pdf-modal-header">' +
        '                <span class="pdf-modal-close">×</span>' +
        '                <h4  data-label="modalTitle2">'+properties_lang.modalTitle2+'</h4>' +
        '            </div>' +
        '            <div class="pdf-modal-body">' +
        '                <div class="pdf-modal-row">' +
        '                    <div class="width-70 form-group">' +
        '                        <label class="label-text"  data-label="labelContentView">'+properties_lang.labelContentView+'</label>' +
        '                        <input id="comment-text" class="pdf-file-name pdf-modal-input-text" type="text"><br>' +
        '                    </div>' +
        '                    <div class="width-30  form-group">' +
        '                        <label  class="label-text"  data-label="labelTextView">'+properties_lang.labelTextView+'</label>' +
        '                        <input id="comment-text-page" class="pdf-file-name pdf-modal-input-text" type="text">' +
        '                    </div>' +
        '                </div>' +
        '                <div class="pdf-modal-row">' +
        '                    <div class="width-70"></div>' +        
        '                    <div class="width-30">' +        
        '                    </div>' +
        '                </div>' +        
        '                <div class="form-group">' +
        '                    <label class="label-text"  data-label="fontSize">'+properties_lang.fontSize+'</label>' +
        '                    <input id="com-font-size" class="example" type="range" min="5" max="15" name="points" step="1" />' +
        '                </div>' +
        '                <div class="group-buttons">' +
        '                   <button id="com-add" style="min-width:100px;" class="pdf-btn" data-label="confirm">'+properties_lang.confirm+'</button>' +
        '                   <button id="com-close" style="min-width:100px;" class="pdf-btn pdf-btn-second" data-label="cancel">'+properties_lang.cancel+'</button>' +
       
        '                </div>' +
        '            </div>' +

        '        </div>' +
        '    </div>';

    const _addSignatureModal =
        '<div id="add-signature-modal" class="pdf-modal">' +
        '    <div class="pdf-modal-content pdf-modal-dialog" style="max-width:420px;">' +
        '    <div class="pdf-modal-header">' +
        '        <span class="pdf-modal-close">&times;</span>' +
        '        <h4  data-label="modalTitle1">'+properties_lang.modalTitle1+'</h4>' +
        '    </div>' +
        '    <div class="pdf-modal-body">' +
        '    <div class="form-group form-label-inline">' +
        '        <label class="label-text"  data-label="labelTextView">'+properties_lang.labelTextView+'</label>' +
        '        <input id="sig-text-page" class="pdf-file-name pdf-modal-input-text" type="text" />' +
        '    </div>' +
        '    <div class="group-buttons">' +
        '        <button class="pdf-btn"  data-label="confirm">'+properties_lang.confirm+'</button>' +
        '    </div>' +
        '    </div>' +

        '    </div>' +
        '</div>';

    const _comment = '<div class="pdf-comment"><span>COMMENT</span></div>';

    const _trashIcon = '<svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="trash-alt" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" class="svg-inline--fa fa-trash-alt fa-w-14 fa-2x"><path fill="currentColor" d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12zM432 80h-82.41l-34-56.7A48 48 0 0 0 274.41 0H173.59a48 48 0 0 0-41.16 23.3L98.41 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0-16-16zM171.84 50.91A6 6 0 0 1 177 48h94a6 6 0 0 1 5.15 2.91L293.61 80H154.39zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12z" class=""></path></svg>';
    const _editIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 401.52289 401"class=""><g><path d="m370.589844 250.972656c-5.523438 0-10 4.476563-10 10v88.789063c-.019532 16.5625-13.4375 29.984375-30 30h-280.589844c-16.5625-.015625-29.980469-13.4375-30-30v-260.589844c.019531-16.558594 13.4375-29.980469 30-30h88.789062c5.523438 0 10-4.476563 10-10 0-5.519531-4.476562-10-10-10h-88.789062c-27.601562.03125-49.96875 22.398437-50 50v260.59375c.03125 27.601563 22.398438 49.96875 50 50h280.589844c27.601562-.03125 49.96875-22.398437 50-50v-88.792969c0-5.523437-4.476563-10-10-10zm0 0" data-original="#000000" class="active-path" data-old_color="#494949" fill="#464646"/><path d="m376.628906 13.441406c-17.574218-17.574218-46.066406-17.574218-63.640625 0l-178.40625 178.40625c-1.222656 1.222656-2.105469 2.738282-2.566406 4.402344l-23.460937 84.699219c-.964844 3.472656.015624 7.191406 2.5625 9.742187 2.550781 2.546875 6.269531 3.527344 9.742187 2.566406l84.699219-23.464843c1.664062-.460938 3.179687-1.34375 4.402344-2.566407l178.402343-178.410156c17.546875-17.585937 17.546875-46.054687 0-63.640625zm-220.257812 184.90625 146.011718-146.015625 47.089844 47.089844-146.015625 146.015625zm-9.40625 18.875 37.621094 37.625-52.039063 14.417969zm227.257812-142.546875-10.605468 10.605469-47.09375-47.09375 10.609374-10.605469c9.761719-9.761719 25.589844-9.761719 35.351563 0l11.738281 11.734375c9.746094 9.773438 9.746094 25.589844 0 35.359375zm0 0" data-original="#000000" class="active-path" data-old_color="#494949" fill="#464646"/></g> </svg>';
    const Base64 = { _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", encode: function (e) { var t = ""; var n, r, i, s, o, u, a; var f = 0; e = Base64._utf8_encode(e); while (f < e.length) { n = e.charCodeAt(f++); r = e.charCodeAt(f++); i = e.charCodeAt(f++); s = n >> 2; o = (n & 3) << 4 | r >> 4; u = (r & 15) << 2 | i >> 6; a = i & 63; if (isNaN(r)) { u = a = 64 } else if (isNaN(i)) { a = 64 } t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a) } return t }, decode: function (e) { var t = ""; var n, r, i; var s, o, u, a; var f = 0; e = e.replace(/[^A-Za-z0-9+/=]/g, ""); while (f < e.length) { s = this._keyStr.indexOf(e.charAt(f++)); o = this._keyStr.indexOf(e.charAt(f++)); u = this._keyStr.indexOf(e.charAt(f++)); a = this._keyStr.indexOf(e.charAt(f++)); n = s << 2 | o >> 4; r = (o & 15) << 4 | u >> 2; i = (u & 3) << 6 | a; t = t + String.fromCharCode(n); if (u != 64) { t = t + String.fromCharCode(r) } if (a != 64) { t = t + String.fromCharCode(i) } } t = Base64._utf8_decode(t); return t }, _utf8_encode: function (e) { e = e.replace(/rn/g, "n"); var t = ""; for (var n = 0; n < e.length; n++) { var r = e.charCodeAt(n); if (r < 128) { t += String.fromCharCode(r) } else if (r > 127 && r < 2048) { t += String.fromCharCode(r >> 6 | 192); t += String.fromCharCode(r & 63 | 128) } else { t += String.fromCharCode(r >> 12 | 224); t += String.fromCharCode(r >> 6 & 63 | 128); t += String.fromCharCode(r & 63 | 128) } } return t }, _utf8_decode: function (e) { var t = ""; var n = 0; var r = c1 = c2 = 0; while (n < e.length) { r = e.charCodeAt(n); if (r < 128) { t += String.fromCharCode(r); n++ } else if (r > 191 && r < 224) { c2 = e.charCodeAt(n + 1); t += String.fromCharCode((r & 31) << 6 | c2 & 63); n += 2 } else { c2 = e.charCodeAt(n + 1); c3 = e.charCodeAt(n + 2); t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63); n += 3 } } return t } }
    return VnptPdf;

    }));




/* == jquery mousewheel plugin == Version: 3.1.13, License: MIT License (MIT) */
!function (a) { "function" === typeof define && define.amd ? define(["jquery"], a) : "object" == typeof exports ? module.exports = a : a(jQuery) }(function (a) { function b(b) { var g = b || window.event, h = i.call(arguments, 1), j = 0, l = 0, m = 0, n = 0, o = 0, p = 0; if (b = a.event.fix(g), b.type = "mousewheel", "detail" in g && (m = -1 * g.detail), "wheelDelta" in g && (m = g.wheelDelta), "wheelDeltaY" in g && (m = g.wheelDeltaY), "wheelDeltaX" in g && (l = -1 * g.wheelDeltaX), "axis" in g && g.axis === g.HORIZONTAL_AXIS && (l = -1 * m, m = 0), j = 0 === m ? l : m, "deltaY" in g && (m = -1 * g.deltaY, j = m), "deltaX" in g && (l = g.deltaX, 0 === m && (j = -1 * l)), 0 !== m || 0 !== l) { if (1 === g.deltaMode) { var q = a.data(this, "mousewheel-line-height"); j *= q, m *= q, l *= q } else if (2 === g.deltaMode) { var r = a.data(this, "mousewheel-page-height"); j *= r, m *= r, l *= r } if (n = Math.max(Math.abs(m), Math.abs(l)), (!f || f > n) && (f = n, d(g, n) && (f /= 40)), d(g, n) && (j /= 40, l /= 40, m /= 40), j = Math[j >= 1 ? "floor" : "ceil"](j / f), l = Math[l >= 1 ? "floor" : "ceil"](l / f), m = Math[m >= 1 ? "floor" : "ceil"](m / f), k.settings.normalizeOffset && this.getBoundingClientRect) { var s = this.getBoundingClientRect(); o = b.clientX - s.left, p = b.clientY - s.top } return b.deltaX = l, b.deltaY = m, b.deltaFactor = f, b.offsetX = o, b.offsetY = p, b.deltaMode = 0, h.unshift(b, j, l, m), e && clearTimeout(e), e = setTimeout(c, 200), (a.event.dispatch || a.event.handle).apply(this, h) } } function c() { f = null } function d(a, b) { return k.settings.adjustOldDeltas && "mousewheel" === a.type && b % 120 === 0 } var e, f, g = ["wheel", "mousewheel", "DOMMouseScroll", "MozMousePixelScroll"], h = "onwheel" in document || document.documentMode >= 9 ? ["wheel"] : ["mousewheel", "DomMouseScroll", "MozMousePixelScroll"], i = Array.prototype.slice; if (a.event.fixHooks) for (var j = g.length; j;)a.event.fixHooks[g[--j]] = a.event.mouseHooks; var k = a.event.special.mousewheel = { version: "3.1.12", setup: function () { if (this.addEventListener) for (var c = h.length; c;)this.addEventListener(h[--c], b, !1); else this.onmousewheel = b; a.data(this, "mousewheel-line-height", k.getLineHeight(this)), a.data(this, "mousewheel-page-height", k.getPageHeight(this)) }, teardown: function () { if (this.removeEventListener) for (var c = h.length; c;)this.removeEventListener(h[--c], b, !1); else this.onmousewheel = null; a.removeData(this, "mousewheel-line-height"), a.removeData(this, "mousewheel-page-height") }, getLineHeight: function (b) { var c = a(b), d = c["offsetParent" in a.fn ? "offsetParent" : "parent"](); return d.length || (d = a("body")), parseInt(d.css("fontSize"), 10) || parseInt(c.css("fontSize"), 10) || 16 }, getPageHeight: function (b) { return a(b).height() }, settings: { adjustOldDeltas: !0, normalizeOffset: !0 } }; a.fn.extend({ mousewheel: function (a) { return a ? this.bind("mousewheel", a) : this.trigger("mousewheel") }, unmousewheel: function (a) { return this.unbind("mousewheel", a) } }) }); !function (a) { "function" == typeof define && define.amd ? define(["jquery"], a) : "object" == typeof exports ? module.exports = a : a(jQuery) }(function (a) { function b(b) { var g = b || window.event, h = i.call(arguments, 1), j = 0, l = 0, m = 0, n = 0, o = 0, p = 0; if (b = a.event.fix(g), b.type = "mousewheel", "detail" in g && (m = -1 * g.detail), "wheelDelta" in g && (m = g.wheelDelta), "wheelDeltaY" in g && (m = g.wheelDeltaY), "wheelDeltaX" in g && (l = -1 * g.wheelDeltaX), "axis" in g && g.axis === g.HORIZONTAL_AXIS && (l = -1 * m, m = 0), j = 0 === m ? l : m, "deltaY" in g && (m = -1 * g.deltaY, j = m), "deltaX" in g && (l = g.deltaX, 0 === m && (j = -1 * l)), 0 !== m || 0 !== l) { if (1 === g.deltaMode) { var q = a.data(this, "mousewheel-line-height"); j *= q, m *= q, l *= q } else if (2 === g.deltaMode) { var r = a.data(this, "mousewheel-page-height"); j *= r, m *= r, l *= r } if (n = Math.max(Math.abs(m), Math.abs(l)), (!f || f > n) && (f = n, d(g, n) && (f /= 40)), d(g, n) && (j /= 40, l /= 40, m /= 40), j = Math[j >= 1 ? "floor" : "ceil"](j / f), l = Math[l >= 1 ? "floor" : "ceil"](l / f), m = Math[m >= 1 ? "floor" : "ceil"](m / f), k.settings.normalizeOffset && this.getBoundingClientRect) { var s = this.getBoundingClientRect(); o = b.clientX - s.left, p = b.clientY - s.top } return b.deltaX = l, b.deltaY = m, b.deltaFactor = f, b.offsetX = o, b.offsetY = p, b.deltaMode = 0, h.unshift(b, j, l, m), e && clearTimeout(e), e = setTimeout(c, 200), (a.event.dispatch || a.event.handle).apply(this, h) } } function c() { f = null } function d(a, b) { return k.settings.adjustOldDeltas && "mousewheel" === a.type && b % 120 === 0 } var e, f, g = ["wheel", "mousewheel", "DOMMouseScroll", "MozMousePixelScroll"], h = "onwheel" in document || document.documentMode >= 9 ? ["wheel"] : ["mousewheel", "DomMouseScroll", "MozMousePixelScroll"], i = Array.prototype.slice; if (a.event.fixHooks) for (var j = g.length; j;)a.event.fixHooks[g[--j]] = a.event.mouseHooks; var k = a.event.special.mousewheel = { version: "3.1.12", setup: function () { if (this.addEventListener) for (var c = h.length; c;)this.addEventListener(h[--c], b, !1); else this.onmousewheel = b; a.data(this, "mousewheel-line-height", k.getLineHeight(this)), a.data(this, "mousewheel-page-height", k.getPageHeight(this)) }, teardown: function () { if (this.removeEventListener) for (var c = h.length; c;)this.removeEventListener(h[--c], b, !1); else this.onmousewheel = null; a.removeData(this, "mousewheel-line-height"), a.removeData(this, "mousewheel-page-height") }, getLineHeight: function (b) { var c = a(b), d = c["offsetParent" in a.fn ? "offsetParent" : "parent"](); return d.length || (d = a("body")), parseInt(d.css("fontSize"), 10) || parseInt(c.css("fontSize"), 10) || 16 }, getPageHeight: function (b) { return a(b).height() }, settings: { adjustOldDeltas: !0, normalizeOffset: !0 } }; a.fn.extend({ mousewheel: function (a) { return a ? this.bind("mousewheel", a) : this.trigger("mousewheel") }, unmousewheel: function (a) { return this.unbind("mousewheel", a) } }) });
/* == malihu jquery custom scrollbar plugin == Version: 3.1.5, License: MIT License (MIT) */
!function (e) { "function" === typeof define && define.amd ? define(["jquery"], e) : "undefined" != typeof module && module.exports ? module.exports = e : e(jQuery, window, document) }(function (e) {
    !function (t) { var o = "function" === typeof define && define.amd, a = "undefined" !== typeof module && module.exports, n = "https:" == document.location.protocol ? "https:" : "http:", i = "cdnjs.cloudflare.com/ajax/libs/jquery-mousewheel/3.1.13/jquery.mousewheel.min.js"; o || (a ? require("jquery-mousewheel")(e) : e.event.special.mousewheel || e("head").append(decodeURI("%3Cscript src=" + n + "//" + i + "%3E%3C/script%3E"))), t() }(function () {
        var t, o = "mCustomScrollbar", a = "mCS", n = ".mCustomScrollbar", i = { setTop: 0, setLeft: 0, axis: "y", scrollbarPosition: "inside", scrollInertia: 950, autoDraggerLength: !0, alwaysShowScrollbar: 0, snapOffset: 0, mouseWheel: { enable: !0, scrollAmount: "auto", axis: "y", deltaFactor: "auto", disableOver: ["select", "option", "keygen", "datalist", "textarea"] }, scrollButtons: { scrollType: "stepless", scrollAmount: "auto" }, keyboard: { enable: !0, scrollType: "stepless", scrollAmount: "auto" }, contentTouchScroll: 25, documentTouchScroll: !0, advanced: { autoScrollOnFocus: "input,textarea,select,button,datalist,keygen,a[tabindex],area,object,[contenteditable='true']", updateOnContentResize: !0, updateOnImageLoad: "auto", autoUpdateTimeout: 60 }, theme: "light", callbacks: { onTotalScrollOffset: 0, onTotalScrollBackOffset: 0, alwaysTriggerOffsets: !0 } }, r = 0, l = {}, s = window.attachEvent && !window.addEventListener ? 1 : 0, c = !1, d = ["mCSB_dragger_onDrag", "mCSB_scrollTools_onDrag", "mCS_img_loaded", "mCS_disabled", "mCS_destroyed", "mCS_no_scrollbar", "mCS-autoHide", "mCS-dir-rtl", "mCS_no_scrollbar_y", "mCS_no_scrollbar_x", "mCS_y_hidden", "mCS_x_hidden", "mCSB_draggerContainer", "mCSB_buttonUp", "mCSB_buttonDown", "mCSB_buttonLeft", "mCSB_buttonRight"], u = { init: function (t) { var t = e.extend(!0, {}, i, t), o = f.call(this); if (t.live) { var s = t.liveSelector || this.selector || n, c = e(s); if ("off" === t.live) return void m(s); l[s] = setTimeout(function () { c.mCustomScrollbar(t), "once" === t.live && c.length && m(s) }, 500) } else m(s); return t.setWidth = t.set_width ? t.set_width : t.setWidth, t.setHeight = t.set_height ? t.set_height : t.setHeight, t.axis = t.horizontalScroll ? "x" : p(t.axis), t.scrollInertia = t.scrollInertia > 0 && t.scrollInertia < 17 ? 17 : t.scrollInertia, "object" != typeof t.mouseWheel && 1 == t.mouseWheel && (t.mouseWheel = { enable: !0, scrollAmount: "auto", axis: "y", preventDefault: !1, deltaFactor: "auto", normalizeDelta: !1, invert: !1 }), t.mouseWheel.scrollAmount = t.mouseWheelPixels ? t.mouseWheelPixels : t.mouseWheel.scrollAmount, t.mouseWheel.normalizeDelta = t.advanced.normalizeMouseWheelDelta ? t.advanced.normalizeMouseWheelDelta : t.mouseWheel.normalizeDelta, t.scrollButtons.scrollType = g(t.scrollButtons.scrollType), h(t), e(o).each(function () { var o = e(this); if (!o.data(a)) { o.data(a, { idx: ++r, opt: t, scrollRatio: { y: null, x: null }, overflowed: null, contentReset: { y: null, x: null }, bindEvents: !1, tweenRunning: !1, sequential: {}, langDir: o.css("direction"), cbOffsets: null, trigger: null, poll: { size: { o: 0, n: 0 }, img: { o: 0, n: 0 }, change: { o: 0, n: 0 } } }); var n = o.data(a), i = n.opt, l = o.data("mcs-axis"), s = o.data("mcs-scrollbar-position"), c = o.data("mcs-theme"); l && (i.axis = l), s && (i.scrollbarPosition = s), c && (i.theme = c, h(i)), v.call(this), n && i.callbacks.onCreate && "function" == typeof i.callbacks.onCreate && i.callbacks.onCreate.call(this), e("#mCSB_" + n.idx + "_container img:not(." + d[2] + ")").addClass(d[2]), u.update.call(null, o) } }) }, update: function (t, o) { var n = t || f.call(this); return e(n).each(function () { var t = e(this); if (t.data(a)) { var n = t.data(a), i = n.opt, r = e("#mCSB_" + n.idx + "_container"), l = e("#mCSB_" + n.idx), s = [e("#mCSB_" + n.idx + "_dragger_vertical"), e("#mCSB_" + n.idx + "_dragger_horizontal")]; if (!r.length) return; n.tweenRunning && Q(t), o && n && i.callbacks.onBeforeUpdate && "function" == typeof i.callbacks.onBeforeUpdate && i.callbacks.onBeforeUpdate.call(this), t.hasClass(d[3]) && t.removeClass(d[3]), t.hasClass(d[4]) && t.removeClass(d[4]), l.css("max-height", "none"), l.height() !== t.height() && l.css("max-height", t.height()), _.call(this), "y" === i.axis || i.advanced.autoExpandHorizontalScroll || r.css("width", x(r)), n.overflowed = y.call(this), M.call(this), i.autoDraggerLength && S.call(this), b.call(this), T.call(this); var c = [Math.abs(r[0].offsetTop), Math.abs(r[0].offsetLeft)]; "x" !== i.axis && (n.overflowed[0] ? s[0].height() > s[0].parent().height() ? B.call(this) : (G(t, c[0].toString(), { dir: "y", dur: 0, overwrite: "none" }), n.contentReset.y = null) : (B.call(this), "y" === i.axis ? k.call(this) : "yx" === i.axis && n.overflowed[1] && G(t, c[1].toString(), { dir: "x", dur: 0, overwrite: "none" }))), "y" !== i.axis && (n.overflowed[1] ? s[1].width() > s[1].parent().width() ? B.call(this) : (G(t, c[1].toString(), { dir: "x", dur: 0, overwrite: "none" }), n.contentReset.x = null) : (B.call(this), "x" === i.axis ? k.call(this) : "yx" === i.axis && n.overflowed[0] && G(t, c[0].toString(), { dir: "y", dur: 0, overwrite: "none" }))), o && n && (2 === o && i.callbacks.onImageLoad && "function" == typeof i.callbacks.onImageLoad ? i.callbacks.onImageLoad.call(this) : 3 === o && i.callbacks.onSelectorChange && "function" == typeof i.callbacks.onSelectorChange ? i.callbacks.onSelectorChange.call(this) : i.callbacks.onUpdate && "function" == typeof i.callbacks.onUpdate && i.callbacks.onUpdate.call(this)), N.call(this) } }) }, scrollTo: function (t, o) { if ("undefined" != typeof t && null != t) { var n = f.call(this); return e(n).each(function () { var n = e(this); if (n.data(a)) { var i = n.data(a), r = i.opt, l = { trigger: "external", scrollInertia: r.scrollInertia, scrollEasing: "mcsEaseInOut", moveDragger: !1, timeout: 60, callbacks: !0, onStart: !0, onUpdate: !0, onComplete: !0 }, s = e.extend(!0, {}, l, o), c = Y.call(this, t), d = s.scrollInertia > 0 && s.scrollInertia < 17 ? 17 : s.scrollInertia; c[0] = X.call(this, c[0], "y"), c[1] = X.call(this, c[1], "x"), s.moveDragger && (c[0] *= i.scrollRatio.y, c[1] *= i.scrollRatio.x), s.dur = ne() ? 0 : d, setTimeout(function () { null !== c[0] && "undefined" != typeof c[0] && "x" !== r.axis && i.overflowed[0] && (s.dir = "y", s.overwrite = "all", G(n, c[0].toString(), s)), null !== c[1] && "undefined" != typeof c[1] && "y" !== r.axis && i.overflowed[1] && (s.dir = "x", s.overwrite = "none", G(n, c[1].toString(), s)) }, s.timeout) } }) } }, stop: function () { var t = f.call(this); return e(t).each(function () { var t = e(this); t.data(a) && Q(t) }) }, disable: function (t) { var o = f.call(this); return e(o).each(function () { var o = e(this); if (o.data(a)) { o.data(a); N.call(this, "remove"), k.call(this), t && B.call(this), M.call(this, !0), o.addClass(d[3]) } }) }, destroy: function () { var t = f.call(this); return e(t).each(function () { var n = e(this); if (n.data(a)) { var i = n.data(a), r = i.opt, l = e("#mCSB_" + i.idx), s = e("#mCSB_" + i.idx + "_container"), c = e(".mCSB_" + i.idx + "_scrollbar"); r.live && m(r.liveSelector || e(t).selector), N.call(this, "remove"), k.call(this), B.call(this), n.removeData(a), $(this, "mcs"), c.remove(), s.find("img." + d[2]).removeClass(d[2]), l.replaceWith(s.contents()), n.removeClass(o + " _" + a + "_" + i.idx + " " + d[6] + " " + d[7] + " " + d[5] + " " + d[3]).addClass(d[4]) } }) } }, f = function () { return "object" != typeof e(this) || e(this).length < 1 ? n : this }, h = function (t) { var o = ["rounded", "rounded-dark", "rounded-dots", "rounded-dots-dark"], a = ["rounded-dots", "rounded-dots-dark", "3d", "3d-dark", "3d-thick", "3d-thick-dark", "inset", "inset-dark", "inset-2", "inset-2-dark", "inset-3", "inset-3-dark"], n = ["minimal", "minimal-dark"], i = ["minimal", "minimal-dark"], r = ["minimal", "minimal-dark"]; t.autoDraggerLength = e.inArray(t.theme, o) > -1 ? !1 : t.autoDraggerLength, t.autoExpandScrollbar = e.inArray(t.theme, a) > -1 ? !1 : t.autoExpandScrollbar, t.scrollButtons.enable = e.inArray(t.theme, n) > -1 ? !1 : t.scrollButtons.enable, t.autoHideScrollbar = e.inArray(t.theme, i) > -1 ? !0 : t.autoHideScrollbar, t.scrollbarPosition = e.inArray(t.theme, r) > -1 ? "outside" : t.scrollbarPosition }, m = function (e) { l[e] && (clearTimeout(l[e]), $(l, e)) }, p = function (e) { return "yx" === e || "xy" === e || "auto" === e ? "yx" : "x" === e || "horizontal" === e ? "x" : "y" }, g = function (e) { return "stepped" === e || "pixels" === e || "step" === e || "click" === e ? "stepped" : "stepless" }, v = function () { var t = e(this), n = t.data(a), i = n.opt, r = i.autoExpandScrollbar ? " " + d[1] + "_expand" : "", l = ["<div id='mCSB_" + n.idx + "_scrollbar_vertical' class='mCSB_scrollTools mCSB_" + n.idx + "_scrollbar mCS-" + i.theme + " mCSB_scrollTools_vertical" + r + "'><div class='" + d[12] + "'><div id='mCSB_" + n.idx + "_dragger_vertical' class='mCSB_dragger' style='position:absolute;'><div class='mCSB_dragger_bar' /></div><div class='mCSB_draggerRail' /></div></div>", "<div id='mCSB_" + n.idx + "_scrollbar_horizontal' class='mCSB_scrollTools mCSB_" + n.idx + "_scrollbar mCS-" + i.theme + " mCSB_scrollTools_horizontal" + r + "'><div class='" + d[12] + "'><div id='mCSB_" + n.idx + "_dragger_horizontal' class='mCSB_dragger' style='position:absolute;'><div class='mCSB_dragger_bar' /></div><div class='mCSB_draggerRail' /></div></div>"], s = "yx" === i.axis ? "mCSB_vertical_horizontal" : "x" === i.axis ? "mCSB_horizontal" : "mCSB_vertical", c = "yx" === i.axis ? l[0] + l[1] : "x" === i.axis ? l[1] : l[0], u = "yx" === i.axis ? "<div id='mCSB_" + n.idx + "_container_wrapper' class='mCSB_container_wrapper' />" : "", f = i.autoHideScrollbar ? " " + d[6] : "", h = "x" !== i.axis && "rtl" === n.langDir ? " " + d[7] : ""; i.setWidth && t.css("width", i.setWidth), i.setHeight && t.css("height", i.setHeight), i.setLeft = "y" !== i.axis && "rtl" === n.langDir ? "989999px" : i.setLeft, t.addClass(o + " _" + a + "_" + n.idx + f + h).wrapInner("<div id='mCSB_" + n.idx + "' class='mCustomScrollBox mCS-" + i.theme + " " + s + "'><div id='mCSB_" + n.idx + "_container' class='mCSB_container' style='position:relative; top:" + i.setTop + "; left:" + i.setLeft + ";' dir='" + n.langDir + "' /></div>"); var m = e("#mCSB_" + n.idx), p = e("#mCSB_" + n.idx + "_container"); "y" === i.axis || i.advanced.autoExpandHorizontalScroll || p.css("width", x(p)), "outside" === i.scrollbarPosition ? ("static" === t.css("position") && t.css("position", "relative"), t.css("overflow", "visible"), m.addClass("mCSB_outside").after(c)) : (m.addClass("mCSB_inside").append(c), p.wrap(u)), w.call(this); var g = [e("#mCSB_" + n.idx + "_dragger_vertical"), e("#mCSB_" + n.idx + "_dragger_horizontal")]; g[0].css("min-height", g[0].height()), g[1].css("min-width", g[1].width()) }, x = function (t) { var o = [t[0].scrollWidth, Math.max.apply(Math, t.children().map(function () { return e(this).outerWidth(!0) }).get())], a = t.parent().width(); return o[0] > a ? o[0] : o[1] > a ? o[1] : "100%" }, _ = function () { var t = e(this), o = t.data(a), n = o.opt, i = e("#mCSB_" + o.idx + "_container"); if (n.advanced.autoExpandHorizontalScroll && "y" !== n.axis) { i.css({ width: "auto", "min-width": 0, "overflow-x": "scroll" }); var r = Math.ceil(i[0].scrollWidth); 3 === n.advanced.autoExpandHorizontalScroll || 2 !== n.advanced.autoExpandHorizontalScroll && r > i.parent().width() ? i.css({ width: r, "min-width": "100%", "overflow-x": "inherit" }) : i.css({ "overflow-x": "inherit", position: "absolute" }).wrap("<div class='mCSB_h_wrapper' style='position:relative; left:0; width:999999px;' />").css({ width: Math.ceil(i[0].getBoundingClientRect().right + .4) - Math.floor(i[0].getBoundingClientRect().left), "min-width": "100%", position: "relative" }).unwrap() } }, w = function () { var t = e(this), o = t.data(a), n = o.opt, i = e(".mCSB_" + o.idx + "_scrollbar:first"), r = oe(n.scrollButtons.tabindex) ? "tabindex='" + n.scrollButtons.tabindex + "'" : "", l = ["<a href='#' class='" + d[13] + "' " + r + " />", "<a href='#' class='" + d[14] + "' " + r + " />", "<a href='#' class='" + d[15] + "' " + r + " />", "<a href='#' class='" + d[16] + "' " + r + " />"], s = ["x" === n.axis ? l[2] : l[0], "x" === n.axis ? l[3] : l[1], l[2], l[3]]; n.scrollButtons.enable && i.prepend(s[0]).append(s[1]).next(".mCSB_scrollTools").prepend(s[2]).append(s[3]) }, S = function () { var t = e(this), o = t.data(a), n = e("#mCSB_" + o.idx), i = e("#mCSB_" + o.idx + "_container"), r = [e("#mCSB_" + o.idx + "_dragger_vertical"), e("#mCSB_" + o.idx + "_dragger_horizontal")], l = [n.height() / i.outerHeight(!1), n.width() / i.outerWidth(!1)], c = [parseInt(r[0].css("min-height")), Math.round(l[0] * r[0].parent().height()), parseInt(r[1].css("min-width")), Math.round(l[1] * r[1].parent().width())], d = s && c[1] < c[0] ? c[0] : c[1], u = s && c[3] < c[2] ? c[2] : c[3]; r[0].css({ height: d, "max-height": r[0].parent().height() - 10 }).find(".mCSB_dragger_bar").css({ "line-height": c[0] + "px" }), r[1].css({ width: u, "max-width": r[1].parent().width() - 10 }) }, b = function () { var t = e(this), o = t.data(a), n = e("#mCSB_" + o.idx), i = e("#mCSB_" + o.idx + "_container"), r = [e("#mCSB_" + o.idx + "_dragger_vertical"), e("#mCSB_" + o.idx + "_dragger_horizontal")], l = [i.outerHeight(!1) - n.height(), i.outerWidth(!1) - n.width()], s = [l[0] / (r[0].parent().height() - r[0].height()), l[1] / (r[1].parent().width() - r[1].width())]; o.scrollRatio = { y: s[0], x: s[1] } }, C = function (e, t, o) { var a = o ? d[0] + "_expanded" : "", n = e.closest(".mCSB_scrollTools"); "active" === t ? (e.toggleClass(d[0] + " " + a), n.toggleClass(d[1]), e[0]._draggable = e[0]._draggable ? 0 : 1) : e[0]._draggable || ("hide" === t ? (e.removeClass(d[0]), n.removeClass(d[1])) : (e.addClass(d[0]), n.addClass(d[1]))) }, y = function () { var t = e(this), o = t.data(a), n = e("#mCSB_" + o.idx), i = e("#mCSB_" + o.idx + "_container"), r = null == o.overflowed ? i.height() : i.outerHeight(!1), l = null == o.overflowed ? i.width() : i.outerWidth(!1), s = i[0].scrollHeight, c = i[0].scrollWidth; return s > r && (r = s), c > l && (l = c), [r > n.height(), l > n.width()] }, B = function () { var t = e(this), o = t.data(a), n = o.opt, i = e("#mCSB_" + o.idx), r = e("#mCSB_" + o.idx + "_container"), l = [e("#mCSB_" + o.idx + "_dragger_vertical"), e("#mCSB_" + o.idx + "_dragger_horizontal")]; if (Q(t), ("x" !== n.axis && !o.overflowed[0] || "y" === n.axis && o.overflowed[0]) && (l[0].add(r).css("top", 0), G(t, "_resetY")), "y" !== n.axis && !o.overflowed[1] || "x" === n.axis && o.overflowed[1]) { var s = dx = 0; "rtl" === o.langDir && (s = i.width() - r.outerWidth(!1), dx = Math.abs(s / o.scrollRatio.x)), r.css("left", s), l[1].css("left", dx), G(t, "_resetX") } }, T = function () { function t() { r = setTimeout(function () { e.event.special.mousewheel ? (clearTimeout(r), W.call(o[0])) : t() }, 100) } var o = e(this), n = o.data(a), i = n.opt; if (!n.bindEvents) { if (I.call(this), i.contentTouchScroll && D.call(this), E.call(this), i.mouseWheel.enable) { var r; t() } P.call(this), U.call(this), i.advanced.autoScrollOnFocus && H.call(this), i.scrollButtons.enable && F.call(this), i.keyboard.enable && q.call(this), n.bindEvents = !0 } }, k = function () { var t = e(this), o = t.data(a), n = o.opt, i = a + "_" + o.idx, r = ".mCSB_" + o.idx + "_scrollbar", l = e("#mCSB_" + o.idx + ",#mCSB_" + o.idx + "_container,#mCSB_" + o.idx + "_container_wrapper," + r + " ." + d[12] + ",#mCSB_" + o.idx + "_dragger_vertical,#mCSB_" + o.idx + "_dragger_horizontal," + r + ">a"), s = e("#mCSB_" + o.idx + "_container"); n.advanced.releaseDraggableSelectors && l.add(e(n.advanced.releaseDraggableSelectors)), n.advanced.extraDraggableSelectors && l.add(e(n.advanced.extraDraggableSelectors)), o.bindEvents && (e(document).add(e(!A() || top.document)).unbind("." + i), l.each(function () { e(this).unbind("." + i) }), clearTimeout(t[0]._focusTimeout), $(t[0], "_focusTimeout"), clearTimeout(o.sequential.step), $(o.sequential, "step"), clearTimeout(s[0].onCompleteTimeout), $(s[0], "onCompleteTimeout"), o.bindEvents = !1) }, M = function (t) { var o = e(this), n = o.data(a), i = n.opt, r = e("#mCSB_" + n.idx + "_container_wrapper"), l = r.length ? r : e("#mCSB_" + n.idx + "_container"), s = [e("#mCSB_" + n.idx + "_scrollbar_vertical"), e("#mCSB_" + n.idx + "_scrollbar_horizontal")], c = [s[0].find(".mCSB_dragger"), s[1].find(".mCSB_dragger")]; "x" !== i.axis && (n.overflowed[0] && !t ? (s[0].add(c[0]).add(s[0].children("a")).css("display", "block"), l.removeClass(d[8] + " " + d[10])) : (i.alwaysShowScrollbar ? (2 !== i.alwaysShowScrollbar && c[0].css("display", "none"), l.removeClass(d[10])) : (s[0].css("display", "none"), l.addClass(d[10])), l.addClass(d[8]))), "y" !== i.axis && (n.overflowed[1] && !t ? (s[1].add(c[1]).add(s[1].children("a")).css("display", "block"), l.removeClass(d[9] + " " + d[11])) : (i.alwaysShowScrollbar ? (2 !== i.alwaysShowScrollbar && c[1].css("display", "none"), l.removeClass(d[11])) : (s[1].css("display", "none"), l.addClass(d[11])), l.addClass(d[9]))), n.overflowed[0] || n.overflowed[1] ? o.removeClass(d[5]) : o.addClass(d[5]) }, O = function (t) { var o = t.type, a = t.target.ownerDocument !== document && null !== frameElement ? [e(frameElement).offset().top, e(frameElement).offset().left] : null, n = A() && t.target.ownerDocument !== top.document && null !== frameElement ? [e(t.view.frameElement).offset().top, e(t.view.frameElement).offset().left] : [0, 0]; switch (o) { case "pointerdown": case "MSPointerDown": case "pointermove": case "MSPointerMove": case "pointerup": case "MSPointerUp": return a ? [t.originalEvent.pageY - a[0] + n[0], t.originalEvent.pageX - a[1] + n[1], !1] : [t.originalEvent.pageY, t.originalEvent.pageX, !1]; case "touchstart": case "touchmove": case "touchend": var i = t.originalEvent.touches[0] || t.originalEvent.changedTouches[0], r = t.originalEvent.touches.length || t.originalEvent.changedTouches.length; return t.target.ownerDocument !== document ? [i.screenY, i.screenX, r > 1] : [i.pageY, i.pageX, r > 1]; default: return a ? [t.pageY - a[0] + n[0], t.pageX - a[1] + n[1], !1] : [t.pageY, t.pageX, !1] } }, I = function () { function t(e, t, a, n) { if (h[0].idleTimer = d.scrollInertia < 233 ? 250 : 0, o.attr("id") === f[1]) var i = "x", s = (o[0].offsetLeft - t + n) * l.scrollRatio.x; else var i = "y", s = (o[0].offsetTop - e + a) * l.scrollRatio.y; G(r, s.toString(), { dir: i, drag: !0 }) } var o, n, i, r = e(this), l = r.data(a), d = l.opt, u = a + "_" + l.idx, f = ["mCSB_" + l.idx + "_dragger_vertical", "mCSB_" + l.idx + "_dragger_horizontal"], h = e("#mCSB_" + l.idx + "_container"), m = e("#" + f[0] + ",#" + f[1]), p = d.advanced.releaseDraggableSelectors ? m.add(e(d.advanced.releaseDraggableSelectors)) : m, g = d.advanced.extraDraggableSelectors ? e(!A() || top.document).add(e(d.advanced.extraDraggableSelectors)) : e(!A() || top.document); m.bind("contextmenu." + u, function (e) { e.preventDefault() }).bind("mousedown." + u + " touchstart." + u + " pointerdown." + u + " MSPointerDown." + u, function (t) { if (t.stopImmediatePropagation(), t.preventDefault(), ee(t)) { c = !0, s && (document.onselectstart = function () { return !1 }), L.call(h, !1), Q(r), o = e(this); var a = o.offset(), l = O(t)[0] - a.top, u = O(t)[1] - a.left, f = o.height() + a.top, m = o.width() + a.left; f > l && l > 0 && m > u && u > 0 && (n = l, i = u), C(o, "active", d.autoExpandScrollbar) } }).bind("touchmove." + u, function (e) { e.stopImmediatePropagation(), e.preventDefault(); var a = o.offset(), r = O(e)[0] - a.top, l = O(e)[1] - a.left; t(n, i, r, l) }), e(document).add(g).bind("mousemove." + u + " pointermove." + u + " MSPointerMove." + u, function (e) { if (o) { var a = o.offset(), r = O(e)[0] - a.top, l = O(e)[1] - a.left; if (n === r && i === l) return; t(n, i, r, l) } }).add(p).bind("mouseup." + u + " touchend." + u + " pointerup." + u + " MSPointerUp." + u, function () { o && (C(o, "active", d.autoExpandScrollbar), o = null), c = !1, s && (document.onselectstart = null), L.call(h, !0) }) }, D = function () { function o(e) { if (!te(e) || c || O(e)[2]) return void (t = 0); t = 1, b = 0, C = 0, d = 1, y.removeClass("mCS_touch_action"); var o = I.offset(); u = O(e)[0] - o.top, f = O(e)[1] - o.left, z = [O(e)[0], O(e)[1]] } function n(e) { if (te(e) && !c && !O(e)[2] && (T.documentTouchScroll || e.preventDefault(), e.stopImmediatePropagation(), (!C || b) && d)) { g = K(); var t = M.offset(), o = O(e)[0] - t.top, a = O(e)[1] - t.left, n = "mcsLinearOut"; if (E.push(o), W.push(a), z[2] = Math.abs(O(e)[0] - z[0]), z[3] = Math.abs(O(e)[1] - z[1]), B.overflowed[0]) var i = D[0].parent().height() - D[0].height(), r = u - o > 0 && o - u > -(i * B.scrollRatio.y) && (2 * z[3] < z[2] || "yx" === T.axis); if (B.overflowed[1]) var l = D[1].parent().width() - D[1].width(), h = f - a > 0 && a - f > -(l * B.scrollRatio.x) && (2 * z[2] < z[3] || "yx" === T.axis); r || h ? (U || e.preventDefault(), b = 1) : (C = 1, y.addClass("mCS_touch_action")), U && e.preventDefault(), w = "yx" === T.axis ? [u - o, f - a] : "x" === T.axis ? [null, f - a] : [u - o, null], I[0].idleTimer = 250, B.overflowed[0] && s(w[0], R, n, "y", "all", !0), B.overflowed[1] && s(w[1], R, n, "x", L, !0) } } function i(e) { if (!te(e) || c || O(e)[2]) return void (t = 0); t = 1, e.stopImmediatePropagation(), Q(y), p = K(); var o = M.offset(); h = O(e)[0] - o.top, m = O(e)[1] - o.left, E = [], W = [] } function r(e) { if (te(e) && !c && !O(e)[2]) { d = 0, e.stopImmediatePropagation(), b = 0, C = 0, v = K(); var t = M.offset(), o = O(e)[0] - t.top, a = O(e)[1] - t.left; if (!(v - g > 30)) { _ = 1e3 / (v - p); var n = "mcsEaseOut", i = 2.5 > _, r = i ? [E[E.length - 2], W[W.length - 2]] : [0, 0]; x = i ? [o - r[0], a - r[1]] : [o - h, a - m]; var u = [Math.abs(x[0]), Math.abs(x[1])]; _ = i ? [Math.abs(x[0] / 4), Math.abs(x[1] / 4)] : [_, _]; var f = [Math.abs(I[0].offsetTop) - x[0] * l(u[0] / _[0], _[0]), Math.abs(I[0].offsetLeft) - x[1] * l(u[1] / _[1], _[1])]; w = "yx" === T.axis ? [f[0], f[1]] : "x" === T.axis ? [null, f[1]] : [f[0], null], S = [4 * u[0] + T.scrollInertia, 4 * u[1] + T.scrollInertia]; var y = parseInt(T.contentTouchScroll) || 0; w[0] = u[0] > y ? w[0] : 0, w[1] = u[1] > y ? w[1] : 0, B.overflowed[0] && s(w[0], S[0], n, "y", L, !1), B.overflowed[1] && s(w[1], S[1], n, "x", L, !1) } } } function l(e, t) { var o = [1.5 * t, 2 * t, t / 1.5, t / 2]; return e > 90 ? t > 4 ? o[0] : o[3] : e > 60 ? t > 3 ? o[3] : o[2] : e > 30 ? t > 8 ? o[1] : t > 6 ? o[0] : t > 4 ? t : o[2] : t > 8 ? t : o[3] } function s(e, t, o, a, n, i) { e && G(y, e.toString(), { dur: t, scrollEasing: o, dir: a, overwrite: n, drag: i }) } var d, u, f, h, m, p, g, v, x, _, w, S, b, C, y = e(this), B = y.data(a), T = B.opt, k = a + "_" + B.idx, M = e("#mCSB_" + B.idx), I = e("#mCSB_" + B.idx + "_container"), D = [e("#mCSB_" + B.idx + "_dragger_vertical"), e("#mCSB_" + B.idx + "_dragger_horizontal")], E = [], W = [], R = 0, L = "yx" === T.axis ? "none" : "all", z = [], P = I.find("iframe"), H = ["touchstart." + k + " pointerdown." + k + " MSPointerDown." + k, "touchmove." + k + " pointermove." + k + " MSPointerMove." + k, "touchend." + k + " pointerup." + k + " MSPointerUp." + k], U = void 0 !== document.body.style.touchAction && "" !== document.body.style.touchAction; I.bind(H[0], function (e) { o(e) }).bind(H[1], function (e) { n(e) }), M.bind(H[0], function (e) { i(e) }).bind(H[2], function (e) { r(e) }), P.length && P.each(function () { e(this).bind("load", function () { A(this) && e(this.contentDocument || this.contentWindow.document).bind(H[0], function (e) { o(e), i(e) }).bind(H[1], function (e) { n(e) }).bind(H[2], function (e) { r(e) }) }) }) }, E = function () { function o() { return window.getSelection ? window.getSelection().toString() : document.selection && "Control" != document.selection.type ? document.selection.createRange().text : 0 } function n(e, t, o) { d.type = o && i ? "stepped" : "stepless", d.scrollAmount = 10, j(r, e, t, "mcsLinearOut", o ? 60 : null) } var i, r = e(this), l = r.data(a), s = l.opt, d = l.sequential, u = a + "_" + l.idx, f = e("#mCSB_" + l.idx + "_container"), h = f.parent(); f.bind("mousedown." + u, function () { t || i || (i = 1, c = !0) }).add(document).bind("mousemove." + u, function (e) { if (!t && i && o()) { var a = f.offset(), r = O(e)[0] - a.top + f[0].offsetTop, c = O(e)[1] - a.left + f[0].offsetLeft; r > 0 && r < h.height() && c > 0 && c < h.width() ? d.step && n("off", null, "stepped") : ("x" !== s.axis && l.overflowed[0] && (0 > r ? n("on", 38) : r > h.height() && n("on", 40)), "y" !== s.axis && l.overflowed[1] && (0 > c ? n("on", 37) : c > h.width() && n("on", 39))) } }).bind("mouseup." + u + " dragend." + u, function () { t || (i && (i = 0, n("off", null)), c = !1) }) }, W = function () { function t(t, a) { if (Q(o), !z(o, t.target)) { var r = "auto" !== i.mouseWheel.deltaFactor ? parseInt(i.mouseWheel.deltaFactor) : s && t.deltaFactor < 100 ? 100 : t.deltaFactor || 100, d = i.scrollInertia; if ("x" === i.axis || "x" === i.mouseWheel.axis) var u = "x", f = [Math.round(r * n.scrollRatio.x), parseInt(i.mouseWheel.scrollAmount)], h = "auto" !== i.mouseWheel.scrollAmount ? f[1] : f[0] >= l.width() ? .9 * l.width() : f[0], m = Math.abs(e("#mCSB_" + n.idx + "_container")[0].offsetLeft), p = c[1][0].offsetLeft, g = c[1].parent().width() - c[1].width(), v = "y" === i.mouseWheel.axis ? t.deltaY || a : t.deltaX; else var u = "y", f = [Math.round(r * n.scrollRatio.y), parseInt(i.mouseWheel.scrollAmount)], h = "auto" !== i.mouseWheel.scrollAmount ? f[1] : f[0] >= l.height() ? .9 * l.height() : f[0], m = Math.abs(e("#mCSB_" + n.idx + "_container")[0].offsetTop), p = c[0][0].offsetTop, g = c[0].parent().height() - c[0].height(), v = t.deltaY || a; "y" === u && !n.overflowed[0] || "x" === u && !n.overflowed[1] || ((i.mouseWheel.invert || t.webkitDirectionInvertedFromDevice) && (v = -v), i.mouseWheel.normalizeDelta && (v = 0 > v ? -1 : 1), (v > 0 && 0 !== p || 0 > v && p !== g || i.mouseWheel.preventDefault) && (t.stopImmediatePropagation(), t.preventDefault()), t.deltaFactor < 5 && !i.mouseWheel.normalizeDelta && (h = t.deltaFactor, d = 17), G(o, (m - v * h).toString(), { dir: u, dur: d })) } } if (e(this).data(a)) { var o = e(this), n = o.data(a), i = n.opt, r = a + "_" + n.idx, l = e("#mCSB_" + n.idx), c = [e("#mCSB_" + n.idx + "_dragger_vertical"), e("#mCSB_" + n.idx + "_dragger_horizontal")], d = e("#mCSB_" + n.idx + "_container").find("iframe"); d.length && d.each(function () { e(this).bind("load", function () { A(this) && e(this.contentDocument || this.contentWindow.document).bind("mousewheel." + r, function (e, o) { t(e, o) }) }) }), l.bind("mousewheel." + r, function (e, o) { t(e, o) }) } }, R = new Object, A = function (t) { var o = !1, a = !1, n = null; if (void 0 === t ? a = "#empty" : void 0 !== e(t).attr("id") && (a = e(t).attr("id")), a !== !1 && void 0 !== R[a]) return R[a]; if (t) { try { var i = t.contentDocument || t.contentWindow.document; n = i.body.innerHTML } catch (r) { } o = null !== n } else { try { var i = top.document; n = i.body.innerHTML } catch (r) { } o = null !== n } return a !== !1 && (R[a] = o), o }, L = function (e) { var t = this.find("iframe"); if (t.length) { var o = e ? "auto" : "none"; t.css("pointer-events", o) } }, z = function (t, o) { var n = o.nodeName.toLowerCase(), i = t.data(a).opt.mouseWheel.disableOver, r = ["select", "textarea"]; return e.inArray(n, i) > -1 && !(e.inArray(n, r) > -1 && !e(o).is(":focus")) }, P = function () { var t, o = e(this), n = o.data(a), i = a + "_" + n.idx, r = e("#mCSB_" + n.idx + "_container"), l = r.parent(), s = e(".mCSB_" + n.idx + "_scrollbar ." + d[12]); s.bind("mousedown." + i + " touchstart." + i + " pointerdown." + i + " MSPointerDown." + i, function (o) { c = !0, e(o.target).hasClass("mCSB_dragger") || (t = 1) }).bind("touchend." + i + " pointerup." + i + " MSPointerUp." + i, function () { c = !1 }).bind("click." + i, function (a) { if (t && (t = 0, e(a.target).hasClass(d[12]) || e(a.target).hasClass("mCSB_draggerRail"))) { Q(o); var i = e(this), s = i.find(".mCSB_dragger"); if (i.parent(".mCSB_scrollTools_horizontal").length > 0) { if (!n.overflowed[1]) return; var c = "x", u = a.pageX > s.offset().left ? -1 : 1, f = Math.abs(r[0].offsetLeft) - u * (.9 * l.width()) } else { if (!n.overflowed[0]) return; var c = "y", u = a.pageY > s.offset().top ? -1 : 1, f = Math.abs(r[0].offsetTop) - u * (.9 * l.height()) } G(o, f.toString(), { dir: c, scrollEasing: "mcsEaseInOut" }) } }) }, H = function () { var t = e(this), o = t.data(a), n = o.opt, i = a + "_" + o.idx, r = e("#mCSB_" + o.idx + "_container"), l = r.parent(); r.bind("focusin." + i, function () { var o = e(document.activeElement), a = r.find(".mCustomScrollBox").length, i = 0; o.is(n.advanced.autoScrollOnFocus) && (Q(t), clearTimeout(t[0]._focusTimeout), t[0]._focusTimer = a ? (i + 17) * a : 0, t[0]._focusTimeout = setTimeout(function () { var e = [ae(o)[0], ae(o)[1]], a = [r[0].offsetTop, r[0].offsetLeft], s = [a[0] + e[0] >= 0 && a[0] + e[0] < l.height() - o.outerHeight(!1), a[1] + e[1] >= 0 && a[0] + e[1] < l.width() - o.outerWidth(!1)], c = "yx" !== n.axis || s[0] || s[1] ? "all" : "none"; "x" === n.axis || s[0] || G(t, e[0].toString(), { dir: "y", scrollEasing: "mcsEaseInOut", overwrite: c, dur: i }), "y" === n.axis || s[1] || G(t, e[1].toString(), { dir: "x", scrollEasing: "mcsEaseInOut", overwrite: c, dur: i }) }, t[0]._focusTimer)) }) }, U = function () { var t = e(this), o = t.data(a), n = a + "_" + o.idx, i = e("#mCSB_" + o.idx + "_container").parent(); i.bind("scroll." + n, function () { 0 === i.scrollTop() && 0 === i.scrollLeft() || e(".mCSB_" + o.idx + "_scrollbar").css("visibility", "hidden") }) }, F = function () { var t = e(this), o = t.data(a), n = o.opt, i = o.sequential, r = a + "_" + o.idx, l = ".mCSB_" + o.idx + "_scrollbar", s = e(l + ">a"); s.bind("contextmenu." + r, function (e) { e.preventDefault() }).bind("mousedown." + r + " touchstart." + r + " pointerdown." + r + " MSPointerDown." + r + " mouseup." + r + " touchend." + r + " pointerup." + r + " MSPointerUp." + r + " mouseout." + r + " pointerout." + r + " MSPointerOut." + r + " click." + r, function (a) { function r(e, o) { i.scrollAmount = n.scrollButtons.scrollAmount, j(t, e, o) } if (a.preventDefault(), ee(a)) { var l = e(this).attr("class"); switch (i.type = n.scrollButtons.scrollType, a.type) { case "mousedown": case "touchstart": case "pointerdown": case "MSPointerDown": if ("stepped" === i.type) return; c = !0, o.tweenRunning = !1, r("on", l); break; case "mouseup": case "touchend": case "pointerup": case "MSPointerUp": case "mouseout": case "pointerout": case "MSPointerOut": if ("stepped" === i.type) return; c = !1, i.dir && r("off", l); break; case "click": if ("stepped" !== i.type || o.tweenRunning) return; r("on", l) } } }) }, q = function () { function t(t) { function a(e, t) { r.type = i.keyboard.scrollType, r.scrollAmount = i.keyboard.scrollAmount, "stepped" === r.type && n.tweenRunning || j(o, e, t) } switch (t.type) { case "blur": n.tweenRunning && r.dir && a("off", null); break; case "keydown": case "keyup": var l = t.keyCode ? t.keyCode : t.which, s = "on"; if ("x" !== i.axis && (38 === l || 40 === l) || "y" !== i.axis && (37 === l || 39 === l)) { if ((38 === l || 40 === l) && !n.overflowed[0] || (37 === l || 39 === l) && !n.overflowed[1]) return; "keyup" === t.type && (s = "off"), e(document.activeElement).is(u) || (t.preventDefault(), t.stopImmediatePropagation(), a(s, l)) } else if (33 === l || 34 === l) { if ((n.overflowed[0] || n.overflowed[1]) && (t.preventDefault(), t.stopImmediatePropagation()), "keyup" === t.type) { Q(o); var f = 34 === l ? -1 : 1; if ("x" === i.axis || "yx" === i.axis && n.overflowed[1] && !n.overflowed[0]) var h = "x", m = Math.abs(c[0].offsetLeft) - f * (.9 * d.width()); else var h = "y", m = Math.abs(c[0].offsetTop) - f * (.9 * d.height()); G(o, m.toString(), { dir: h, scrollEasing: "mcsEaseInOut" }) } } else if ((35 === l || 36 === l) && !e(document.activeElement).is(u) && ((n.overflowed[0] || n.overflowed[1]) && (t.preventDefault(), t.stopImmediatePropagation()), "keyup" === t.type)) { if ("x" === i.axis || "yx" === i.axis && n.overflowed[1] && !n.overflowed[0]) var h = "x", m = 35 === l ? Math.abs(d.width() - c.outerWidth(!1)) : 0; else var h = "y", m = 35 === l ? Math.abs(d.height() - c.outerHeight(!1)) : 0; G(o, m.toString(), { dir: h, scrollEasing: "mcsEaseInOut" }) } } } var o = e(this), n = o.data(a), i = n.opt, r = n.sequential, l = a + "_" + n.idx, s = e("#mCSB_" + n.idx), c = e("#mCSB_" + n.idx + "_container"), d = c.parent(), u = "input,textarea,select,datalist,keygen,[contenteditable='true']", f = c.find("iframe"), h = ["blur." + l + " keydown." + l + " keyup." + l]; f.length && f.each(function () { e(this).bind("load", function () { A(this) && e(this.contentDocument || this.contentWindow.document).bind(h[0], function (e) { t(e) }) }) }), s.attr("tabindex", "0").bind(h[0], function (e) { t(e) }) }, j = function (t, o, n, i, r) { function l(e) { u.snapAmount && (f.scrollAmount = u.snapAmount instanceof Array ? "x" === f.dir[0] ? u.snapAmount[1] : u.snapAmount[0] : u.snapAmount); var o = "stepped" !== f.type, a = r ? r : e ? o ? p / 1.5 : g : 1e3 / 60, n = e ? o ? 7.5 : 40 : 2.5, s = [Math.abs(h[0].offsetTop), Math.abs(h[0].offsetLeft)], d = [c.scrollRatio.y > 10 ? 10 : c.scrollRatio.y, c.scrollRatio.x > 10 ? 10 : c.scrollRatio.x], m = "x" === f.dir[0] ? s[1] + f.dir[1] * (d[1] * n) : s[0] + f.dir[1] * (d[0] * n), v = "x" === f.dir[0] ? s[1] + f.dir[1] * parseInt(f.scrollAmount) : s[0] + f.dir[1] * parseInt(f.scrollAmount), x = "auto" !== f.scrollAmount ? v : m, _ = i ? i : e ? o ? "mcsLinearOut" : "mcsEaseInOut" : "mcsLinear", w = !!e; return e && 17 > a && (x = "x" === f.dir[0] ? s[1] : s[0]), G(t, x.toString(), { dir: f.dir[0], scrollEasing: _, dur: a, onComplete: w }), e ? void (f.dir = !1) : (clearTimeout(f.step), void (f.step = setTimeout(function () { l() }, a))) } function s() { clearTimeout(f.step), $(f, "step"), Q(t) } var c = t.data(a), u = c.opt, f = c.sequential, h = e("#mCSB_" + c.idx + "_container"), m = "stepped" === f.type, p = u.scrollInertia < 26 ? 26 : u.scrollInertia, g = u.scrollInertia < 1 ? 17 : u.scrollInertia; switch (o) { case "on": if (f.dir = [n === d[16] || n === d[15] || 39 === n || 37 === n ? "x" : "y", n === d[13] || n === d[15] || 38 === n || 37 === n ? -1 : 1], Q(t), oe(n) && "stepped" === f.type) return; l(m); break; case "off": s(), (m || c.tweenRunning && f.dir) && l(!0) } }, Y = function (t) { var o = e(this).data(a).opt, n = []; return "function" == typeof t && (t = t()), t instanceof Array ? n = t.length > 1 ? [t[0], t[1]] : "x" === o.axis ? [null, t[0]] : [t[0], null] : (n[0] = t.y ? t.y : t.x || "x" === o.axis ? null : t, n[1] = t.x ? t.x : t.y || "y" === o.axis ? null : t), "function" == typeof n[0] && (n[0] = n[0]()), "function" == typeof n[1] && (n[1] = n[1]()), n }, X = function (t, o) { if (null != t && "undefined" != typeof t) { var n = e(this), i = n.data(a), r = i.opt, l = e("#mCSB_" + i.idx + "_container"), s = l.parent(), c = typeof t; o || (o = "x" === r.axis ? "x" : "y"); var d = "x" === o ? l.outerWidth(!1) - s.width() : l.outerHeight(!1) - s.height(), f = "x" === o ? l[0].offsetLeft : l[0].offsetTop, h = "x" === o ? "left" : "top"; switch (c) { case "function": return t(); case "object": var m = t.jquery ? t : e(t); if (!m.length) return; return "x" === o ? ae(m)[1] : ae(m)[0]; case "string": case "number": if (oe(t)) return Math.abs(t); if (-1 !== t.indexOf("%")) return Math.abs(d * parseInt(t) / 100); if (-1 !== t.indexOf("-=")) return Math.abs(f - parseInt(t.split("-=")[1])); if (-1 !== t.indexOf("+=")) { var p = f + parseInt(t.split("+=")[1]); return p >= 0 ? 0 : Math.abs(p) } if (-1 !== t.indexOf("px") && oe(t.split("px")[0])) return Math.abs(t.split("px")[0]); if ("top" === t || "left" === t) return 0; if ("bottom" === t) return Math.abs(s.height() - l.outerHeight(!1)); if ("right" === t) return Math.abs(s.width() - l.outerWidth(!1)); if ("first" === t || "last" === t) { var m = l.find(":" + t); return "x" === o ? ae(m)[1] : ae(m)[0] } return e(t).length ? "x" === o ? ae(e(t))[1] : ae(e(t))[0] : (l.css(h, t), void u.update.call(null, n[0])) } } }, N = function (t) {
            function o() { return clearTimeout(f[0].autoUpdate), 0 === l.parents("html").length ? void (l = null) : void (f[0].autoUpdate = setTimeout(function () { return c.advanced.updateOnSelectorChange && (s.poll.change.n = i(), s.poll.change.n !== s.poll.change.o) ? (s.poll.change.o = s.poll.change.n, void r(3)) : c.advanced.updateOnContentResize && (s.poll.size.n = l[0].scrollHeight + l[0].scrollWidth + f[0].offsetHeight + l[0].offsetHeight + l[0].offsetWidth, s.poll.size.n !== s.poll.size.o) ? (s.poll.size.o = s.poll.size.n, void r(1)) : !c.advanced.updateOnImageLoad || "auto" === c.advanced.updateOnImageLoad && "y" === c.axis || (s.poll.img.n = f.find("img").length, s.poll.img.n === s.poll.img.o) ? void ((c.advanced.updateOnSelectorChange || c.advanced.updateOnContentResize || c.advanced.updateOnImageLoad) && o()) : (s.poll.img.o = s.poll.img.n, void f.find("img").each(function () { n(this) })) }, c.advanced.autoUpdateTimeout)) } function n(t) {
                function o(e, t) {
                    return function () {
                        return t.apply(e, arguments);
                    };
                } function a() { this.onload = null, e(t).addClass(d[2]), r(2) } if (e(t).hasClass(d[2])) return void r(); var n = new Image; n.onload = o(n, a), n.src = t.src
            } function i() { c.advanced.updateOnSelectorChange === !0 && (c.advanced.updateOnSelectorChange = "*"); var e = 0, t = f.find(c.advanced.updateOnSelectorChange); return c.advanced.updateOnSelectorChange && t.length > 0 && t.each(function () { e += this.offsetHeight + this.offsetWidth }), e } function r(e) { clearTimeout(f[0].autoUpdate), u.update.call(null, l[0], e) } var l = e(this), s = l.data(a), c = s.opt, f = e("#mCSB_" + s.idx + "_container"); return t ? (clearTimeout(f[0].autoUpdate), void $(f[0], "autoUpdate")) : void o()
        }, V = function (e, t, o) { return Math.round(e / t) * t - o; }, Q = function (t) { var o = t.data(a), n = e("#mCSB_" + o.idx + "_container,#mCSB_" + o.idx + "_container_wrapper,#mCSB_" + o.idx + "_dragger_vertical,#mCSB_" + o.idx + "_dragger_horizontal"); n.each(function () { Z.call(this) }) }, G = function (t, o, n) { function i(e) { return s && c.callbacks[e] && "function" == typeof c.callbacks[e] } function r() { return [c.callbacks.alwaysTriggerOffsets || w >= S[0] + y, c.callbacks.alwaysTriggerOffsets || -B >= w] } function l() { var e = [h[0].offsetTop, h[0].offsetLeft], o = [x[0].offsetTop, x[0].offsetLeft], a = [h.outerHeight(!1), h.outerWidth(!1)], i = [f.height(), f.width()]; t[0].mcs = { content: h, top: e[0], left: e[1], draggerTop: o[0], draggerLeft: o[1], topPct: Math.round(100 * Math.abs(e[0]) / (Math.abs(a[0]) - i[0])), leftPct: Math.round(100 * Math.abs(e[1]) / (Math.abs(a[1]) - i[1])), direction: n.dir } } var s = t.data(a), c = s.opt, d = { trigger: "internal", dir: "y", scrollEasing: "mcsEaseOut", drag: !1, dur: c.scrollInertia, overwrite: "all", callbacks: !0, onStart: !0, onUpdate: !0, onComplete: !0 }, n = e.extend(d, n), u = [n.dur, n.drag ? 0 : n.dur], f = e("#mCSB_" + s.idx), h = e("#mCSB_" + s.idx + "_container"), m = h.parent(), p = c.callbacks.onTotalScrollOffset ? Y.call(t, c.callbacks.onTotalScrollOffset) : [0, 0], g = c.callbacks.onTotalScrollBackOffset ? Y.call(t, c.callbacks.onTotalScrollBackOffset) : [0, 0]; if (s.trigger = n.trigger, 0 === m.scrollTop() && 0 === m.scrollLeft() || (e(".mCSB_" + s.idx + "_scrollbar").css("visibility", "visible"), m.scrollTop(0).scrollLeft(0)), "_resetY" !== o || s.contentReset.y || (i("onOverflowYNone") && c.callbacks.onOverflowYNone.call(t[0]), s.contentReset.y = 1), "_resetX" !== o || s.contentReset.x || (i("onOverflowXNone") && c.callbacks.onOverflowXNone.call(t[0]), s.contentReset.x = 1), "_resetY" !== o && "_resetX" !== o) { if (!s.contentReset.y && t[0].mcs || !s.overflowed[0] || (i("onOverflowY") && c.callbacks.onOverflowY.call(t[0]), s.contentReset.x = null), !s.contentReset.x && t[0].mcs || !s.overflowed[1] || (i("onOverflowX") && c.callbacks.onOverflowX.call(t[0]), s.contentReset.x = null), c.snapAmount) { var v = c.snapAmount instanceof Array ? "x" === n.dir ? c.snapAmount[1] : c.snapAmount[0] : c.snapAmount; o = V(o, v, c.snapOffset) } switch (n.dir) { case "x": var x = e("#mCSB_" + s.idx + "_dragger_horizontal"), _ = "left", w = h[0].offsetLeft, S = [f.width() - h.outerWidth(!1), x.parent().width() - x.width()], b = [o, 0 === o ? 0 : o / s.scrollRatio.x], y = p[1], B = g[1], T = y > 0 ? y / s.scrollRatio.x : 0, k = B > 0 ? B / s.scrollRatio.x : 0; break; case "y": var x = e("#mCSB_" + s.idx + "_dragger_vertical"), _ = "top", w = h[0].offsetTop, S = [f.height() - h.outerHeight(!1), x.parent().height() - x.height()], b = [o, 0 === o ? 0 : o / s.scrollRatio.y], y = p[0], B = g[0], T = y > 0 ? y / s.scrollRatio.y : 0, k = B > 0 ? B / s.scrollRatio.y : 0 }b[1] < 0 || 0 === b[0] && 0 === b[1] ? b = [0, 0] : b[1] >= S[1] ? b = [S[0], S[1]] : b[0] = -b[0], t[0].mcs || (l(), i("onInit") && c.callbacks.onInit.call(t[0])), clearTimeout(h[0].onCompleteTimeout), J(x[0], _, Math.round(b[1]), u[1], n.scrollEasing), !s.tweenRunning && (0 === w && b[0] >= 0 || w === S[0] && b[0] <= S[0]) || J(h[0], _, Math.round(b[0]), u[0], n.scrollEasing, n.overwrite, { onStart: function () { n.callbacks && n.onStart && !s.tweenRunning && (i("onScrollStart") && (l(), c.callbacks.onScrollStart.call(t[0])), s.tweenRunning = !0, C(x), s.cbOffsets = r()) }, onUpdate: function () { n.callbacks && n.onUpdate && i("whileScrolling") && (l(), c.callbacks.whileScrolling.call(t[0])) }, onComplete: function () { if (n.callbacks && n.onComplete) { "yx" === c.axis && clearTimeout(h[0].onCompleteTimeout); var e = h[0].idleTimer || 0; h[0].onCompleteTimeout = setTimeout(function () { i("onScroll") && (l(), c.callbacks.onScroll.call(t[0])), i("onTotalScroll") && b[1] >= S[1] - T && s.cbOffsets[0] && (l(), c.callbacks.onTotalScroll.call(t[0])), i("onTotalScrollBack") && b[1] <= k && s.cbOffsets[1] && (l(), c.callbacks.onTotalScrollBack.call(t[0])), s.tweenRunning = !1, h[0].idleTimer = 0, C(x, "hide") }, e) } } }) } }, J = function (e, t, o, a, n, i, r) { function l() { S.stop || (x || m.call(), x = K() - v, s(), x >= S.time && (S.time = x > S.time ? x + f - (x - S.time) : x + f - 1, S.time < x + 1 && (S.time = x + 1)), S.time < a ? S.id = h(l) : g.call()) } function s() { a > 0 ? (S.currVal = u(S.time, _, b, a, n), w[t] = Math.round(S.currVal) + "px") : w[t] = o + "px", p.call() } function c() { f = 1e3 / 60, S.time = x + f, h = window.requestAnimationFrame ? window.requestAnimationFrame : function (e) { return s(), setTimeout(e, .01) }, S.id = h(l) } function d() { null != S.id && (window.requestAnimationFrame ? window.cancelAnimationFrame(S.id) : clearTimeout(S.id), S.id = null) } function u(e, t, o, a, n) { switch (n) { case "linear": case "mcsLinear": return o * e / a + t; case "mcsLinearOut": return e /= a, e-- , o * Math.sqrt(1 - e * e) + t; case "easeInOutSmooth": return e /= a / 2, 1 > e ? o / 2 * e * e + t : (e-- , -o / 2 * (e * (e - 2) - 1) + t); case "easeInOutStrong": return e /= a / 2, 1 > e ? o / 2 * Math.pow(2, 10 * (e - 1)) + t : (e-- , o / 2 * (-Math.pow(2, -10 * e) + 2) + t); case "easeInOut": case "mcsEaseInOut": return e /= a / 2, 1 > e ? o / 2 * e * e * e + t : (e -= 2, o / 2 * (e * e * e + 2) + t); case "easeOutSmooth": return e /= a, e-- , -o * (e * e * e * e - 1) + t; case "easeOutStrong": return o * (-Math.pow(2, -10 * e / a) + 1) + t; case "easeOut": case "mcsEaseOut": default: var i = (e /= a) * e, r = i * e; return t + o * (.499999999999997 * r * i + -2.5 * i * i + 5.5 * r + -6.5 * i + 4 * e) } } e._mTween || (e._mTween = { top: {}, left: {} }); var f, h, r = r || {}, m = r.onStart || function () { }, p = r.onUpdate || function () { }, g = r.onComplete || function () { }, v = K(), x = 0, _ = e.offsetTop, w = e.style, S = e._mTween[t]; "left" === t && (_ = e.offsetLeft); var b = o - _; S.stop = 0, "none" !== i && d(), c() }, K = function () { return window.performance && window.performance.now ? window.performance.now() : window.performance && window.performance.webkitNow ? window.performance.webkitNow() : Date.now ? Date.now() : (new Date).getTime() }, Z = function () { var e = this; e._mTween || (e._mTween = { top: {}, left: {} }); for (var t = ["top", "left"], o = 0; o < t.length; o++) { var a = t[o]; e._mTween[a].id && (window.requestAnimationFrame ? window.cancelAnimationFrame(e._mTween[a].id) : clearTimeout(e._mTween[a].id), e._mTween[a].id = null, e._mTween[a].stop = 1) } }, $ = function (e, t) { try { delete e[t] } catch (o) { e[t] = null } }, ee = function (e) { return !(e.which && 1 !== e.which) }, te = function (e) { var t = e.originalEvent.pointerType; return !(t && "touch" !== t && 2 !== t) }, oe = function (e) { return !isNaN(parseFloat(e)) && isFinite(e) }, ae = function (e) { var t = e.parents(".mCSB_container"); return [e.offset().top - t.offset().top, e.offset().left - t.offset().left] }, ne = function () { function e() { var e = ["webkit", "moz", "ms", "o"]; if ("hidden" in document) return "hidden"; for (var t = 0; t < e.length; t++)if (e[t] + "Hidden" in document) return e[t] + "Hidden"; return null } var t = e(); return t ? document[t] : !1 }; e.fn[o] = function (t) { return u[t] ? u[t].apply(this, Array.prototype.slice.call(arguments, 1)) : "object" != typeof t && t ? void e.error("Method " + t + " does not exist") : u.init.apply(this, arguments) }, e[o] = function (t) { return u[t] ? u[t].apply(this, Array.prototype.slice.call(arguments, 1)) : "object" != typeof t && t ? void e.error("Method " + t + " does not exist") : u.init.apply(this, arguments) }, e[o].defaults = i, window[o] = !0, e(window).bind("load", function () { e(n)[o](), e.extend(e.expr[":"], { mcsInView: e.expr[":"].mcsInView || function (t) { var o, a, n = e(t), i = n.parents(".mCSB_container"); if (i.length) return o = i.parent(), a = [i[0].offsetTop, i[0].offsetLeft], a[0] + ae(n)[0] >= 0 && a[0] + ae(n)[0] < o.height() - n.outerHeight(!1) && a[1] + ae(n)[1] >= 0 && a[1] + ae(n)[1] < o.width() - n.outerWidth(!1) }, mcsInSight: e.expr[":"].mcsInSight || function (t, o, a) { var n, i, r, l, s = e(t), c = s.parents(".mCSB_container"), d = "exact" === a[3] ? [[1, 0], [1, 0]] : [[.9, .1], [.6, .4]]; if (c.length) return n = [s.outerHeight(!1), s.outerWidth(!1)], r = [c[0].offsetTop + ae(s)[0], c[0].offsetLeft + ae(s)[1]], i = [c.parent()[0].offsetHeight, c.parent()[0].offsetWidth], l = [n[0] < i[0] ? d[0] : d[1], n[1] < i[1] ? d[0] : d[1]], r[0] - i[0] * l[0][0] < 0 && r[0] + n[0] - i[0] * l[0][1] >= 0 && r[1] - i[1] * l[1][0] < 0 && r[1] + n[1] - i[1] * l[1][1] >= 0 }, mcsOverflow: e.expr[":"].mcsOverflow || function (t) { var o = e(t).data(a); if (o) return o.overflowed[0] || o.overflowed[1] } }) })
    });
});