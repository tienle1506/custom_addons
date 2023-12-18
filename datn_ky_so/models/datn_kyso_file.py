# -*- coding:utf-8 -*-
import os
import pdfplumber
from odoo.http import request
import PyPDF2
import re
import logging
import datetime
import fitz
import base64
from odoo import http, tools, _
_logger = logging.getLogger(__name__)

import base64
import tempfile
import xlrd
import xlsxwriter
import time
import calendar
import json
from odoo.addons import decimal_precision as dp
from io import BytesIO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError

def validate_input_api(kwargs, dict_key_required):
    if 'access_token' in kwargs:
        user = http.request.env()['res.users'].sudo(2).search([('access_token', '=', kwargs['access_token'])],
                                                              limit=1)
        if user:
            for k, v in dict_key_required.items():
                if k not in kwargs:
                    return False, f'Vui lòng truyền "{k}"'
                else:
                    if v == 'number':
                        try:
                            float(kwargs[k])
                        except:
                            return False, f'Vui lòng truyền "{k}" đúng định dạng'
                    if v == 'date':
                        try:
                            datetime.strptime(kwargs[k], '%d/%m/%Y').date()
                        except:
                            return False, f'Vui lòng truyền "{k}" đúng định dạng "DD/MM/YYYY"'
                    if type(v) is list:
                        if kwargs[k] not in v:
                            return False, f'Vui lòng truyền "{k}" là một trong {str(v)}'
            return True, 'Input hợp lệ'
        else:
            return False, 'Vui lòng truyền access_token hợp lệ'
    else:
        return False, 'Vui lòng truyền access_token'


def _generate_sign_file(base64_file, _text_search):
    _list_image_attribute = {}
    _doc = fitz.open(stream=base64.b64decode(base64_file), filetype='pdf')
    for _page in _doc:
        # _text_search => Chữ cần tìm
        _text_instances = _page.search_for(_text_search)
        if len(_text_instances) > 0:
            page_height = _page.rect.height
            # Tạo vị trí vẽ
            for _inst in _text_instances:
                _list_image_attribute.update({
                    'position': {'x0': int(_inst.x0) - 63,
                                 'x1': int(_inst.x0) - 63 + 186,
                                 'y0': int(page_height - int(_inst.y0) - 70),
                                 'y1': int(page_height - int(_inst.y0) - 70 + 69)},
                    'Page': _page.number + 1
                })
                break
            break
    _doc.close()
    return _list_image_attribute

def _get_file_name(name):
    filename = '{ten_khong_dau}_SYLL_Signed_{ngay_gio_ky}.pdf' \
        .format(ten_khong_dau=no_accent_vietnamese(name).replace(' ', ''),
                ngay_gio_ky=datetime.now().strftime('%d%m%Y%H%M'))
    return filename


def get_view_error(self, message, success=False):
    view = self.env.ref('datn_ky_so.message_thongbao_error_kyso')
    view_id = view and view.id or False
    return {
        'success': success,
        'view_id': view_id,
        'message': message
    }


def get_key_token(self):
    return self.env['ir.config_parameter'].sudo().get_param('key_kyso_token')


def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

class HrDepartmentHaNoi(models.Model):
    _inherit = 'hr.department'

    chu_ky = fields.Binary(string="Dấu cơ quan, đơn vị (Dạng .png)", attachment=True, filters="*.png")
    file_name = fields.Char()

class DATNHrKySoFile(models.Model):
    _name = 'datn.kyso.file'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Ký số file'
    _order = "ngay_ky DESC"


    name = fields.Char(string=u'Bảng chấm công tháng', size=128, track_visibility='always', )
    file_kyso = fields.Binary(string='SYLL ký số', attachment=True)
    file_name = fields.Char(u'Tên tệp tin')
    ngay_ky = fields.Date(u'Ngày tạo', widget='date', format='%Y-%m-%d', default=fields.Date.today)
    is_ky_ca_nhan = fields.Boolean(string="Đã ký cá nhân", default=False)
    is_ky_co_quan = fields.Boolean(string="Đã ký cơ quan", default=False)
    is_ky_dau_co_quan = fields.Boolean(string="Đã ký dấu cơ quan", default=False)
    so_lan_ky_nhay = fields.Integer(string="Số lần ký nháy", default=0)

    @api.constrains('file_kyso')
    def check_chu_ky(self):
        if self.file_kyso:
            file_name_split = self.file_name.split('.')
            if file_name_split and file_name_split[-1] != 'pdf':
                raise ValidationError('Chữ ký không đúng định dạng pdf')

    def get_2c_hopnhat_pdf_base_64(self, edition_id):
            loai_ky = request.session.get('loai_ky')
            record = self.browse(edition_id)
            _2c_base_64 = record.file_kyso
            x = 0
            y = 0
            if loai_ky == 'action_kyso_dau_coquan':
                vitris = _generate_sign_file(_2c_base_64, '(Ký tên, đóng dấu)')
                x = 0
                y = 24
            elif loai_ky == 'action_kyso_canhan':
                vitris = _generate_sign_file(_2c_base_64, '(Ký tên, ghi rõ họ tên)')
            elif loai_ky == 'action_kyso_coquan':
                vitris = _generate_sign_file(_2c_base_64, '(Ký tên, đóng dấu)')
            elif loai_ky == 'action_kyso_kynhay':
                vitris = _generate_sign_file(_2c_base_64, '(Ký tên, đóng dấu)')
                x = 80
                y = 80 - 80*int(record.so_lan_ky_nhay) if record.so_lan_ky_nhay else 0
            position = vitris.get('position')
            signature = [{
                'x': position['x0'] + x,
                'y': position['y0'] + y,
                'width': 220,
                'height': 80,
                'page': vitris.get('Page'),
            }]
            return  signature

    @api.model
    def send_to_approve_kyso(self, edition_id, loai_ky):
        request.session['loai_ky'] = loai_ky
        record = self.browse(edition_id)
        user = self.env.user
        user = self.env['hr.employee'].search([('user_id', '=', user.id)])

        if not user.chu_ky:
            raise ValidationError('Chưa có cấu hình ký số của nhân sự này')
        else:
            hinhthuc_kyso_user = user.hinhthuc_kyso_ids
            if not hinhthuc_kyso_user or len(hinhthuc_kyso_user.ids) > 1:
                raise ValidationError('Chưa có cấu hình loại ký số của nhân sự này')
            else:
                try:
                    _2c_base_64 = record.file_kyso
                    signature = self.get_2c_hopnhat_pdf_base_64(edition_id)
                    key = get_key_token(self)
                    chu_ky = user.chu_ky
                    if loai_ky == 'action_kyso_dau_coquan':
                        dau_co_quan = self.env['hr.department'].search([('id', 'parent_of', user.department_id.id),('chu_ky', '!=', False)], order='department_level desc', limit=1)
                        if not dau_co_quan:
                            raise ValidationError('Chưa có cấu hình dấu cơ quan của nhân sự này')
                        chu_ky = dau_co_quan.chu_ky
                    return {
                        'is_config': True,
                        '_2c_base_64': _2c_base_64,
                        'signature': signature,
                        'chu_ky': chu_ky,
                        'key': key,
                        'hinhthuc_kyso': hinhthuc_kyso_user[0].code
                    }
                except Exception as e:
                    return {
                        'render': 'fail',
                        'message': str(e)
                    }
        if view:
            view_id = view and view.id or False
            return {
                'is_config': False,
                'view_id': view_id,
            }

    @api.model
    def complete_kyso(self, edition_id, _base64_daky):
        record = self.browse(edition_id)
        loai_ky = request.session.get('loai_ky')
        is_ky_ca_nhan = record.is_ky_ca_nhan
        is_ky_co_quan = record.is_ky_co_quan
        is_ky_dau_co_quan = record.is_ky_dau_co_quan
        so_lan_ky_nhay = record.so_lan_ky_nhay
        if loai_ky == 'action_kyso_dau_coquan':
            record.is_ky_dau_co_quan = True
        elif loai_ky == 'action_kyso_canhan':
            record.is_ky_ca_nhan = True
        elif loai_ky == 'action_kyso_coquan':
            record.is_ky_co_quan = True
        elif loai_ky == 'action_kyso_kynhay':
            record.so_lan_ky_nhay = record.so_lan_ky_nhay + 1
            x = 80
            y = 80 - 80 * int(record.so_lan_ky_nhay) if record.so_lan_ky_nhay else 0
        if record:
            filename = _get_file_name(record.name)
            record.sudo().write({'file_kyso': _base64_daky, 'file_name': filename,
                                    'is_ky_ca_nhan': is_ky_ca_nhan,
                                    'is_ky_co_quan': is_ky_co_quan,
                                    'is_ky_dau_co_quan': is_ky_dau_co_quan,
                                    'is_ky_dau_co_quan': is_ky_dau_co_quan,
                                    'so_lan_ky_nhay': so_lan_ky_nhay
                                 })
            self.env.cr.execute('''update ir_attachment set name = %s, store_fname = %s where res_id = %s
                                        and res_field = 'file_kyso' and res_model = 'datn.kyso.file'
                                  returning id;''', (filename, filename, edition_id, ))
            result = self.env.cr.dictfetchone()
            view = self.env.ref('datn_ky_so.complete_kyso_view')
            view_id = view and view.id or False
            return {
                'success': True,
                'attachment_id': result.get('id') if result else None,
                'file_name': filename,
                'edition_id': edition_id,
                'view_id': view_id
            }
        return get_view_error(self, 'Không tồn tại hồ sơ')

    @api.model
    def get_id_attachment(self, res_id):
        self.env.cr.execute('''select id from ir_attachment where res_id = %s and res_field = 'file_kyso'
                            and res_model = 'datn.kyso.file' limit 1;''', (res_id, ))
        result = self.env.cr.dictfetchone()
        return result


