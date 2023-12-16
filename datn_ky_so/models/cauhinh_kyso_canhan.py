# -*- coding:utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import re
from datetime import datetime
import requests
import json
import uuid
import base64
import time
from odoo import http, tools, _
# -*- coding: utf-8 -*-
import logging
import datetime
import fitz
import base64
from datetime import datetime
from odoo import http, tools, _
_logger = logging.getLogger(__name__)


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
    view = self.env.ref('vnpt_ky_so.message_thongbao_error_kyso')
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


class HinhThucKySo(models.Model):
    _name = 'hinhthuc_kyso'
    _order = 'stt'

    code = fields.Char(string='Mã', required=True)
    name = fields.Char(string='Tên', required=True)
    is_active = fields.Boolean(string='Áp dụng', default=True)
    stt = fields.Integer(string='STT')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Mã hình thức ký số phải là duy nhất')),
    ]


class ResUsersExt(models.Model):
    _inherit = 'hr.employee'

    hinhthuc_kyso_ids = fields.Many2many(comodel_name='hinhthuc_kyso', string='Hình thức ký số')
    mang_sim_ky_so = fields.Selection(string='Mạng sim ký số PKI', selection=[('vinaphone', 'Vinaphone'),
                                                                              ('viettel', 'Viettel'), ],
                                      required=False, )
    sdt_pki = fields.Char(string='Số điện thoại PKI')
    taikhoan_smartca = fields.Char(string='Số CCCD/CMND (dùng cho SmartCA)')
    chu_ky = fields.Binary(string="Chữ ký", attachment=True, filters="*.png")
    file_name = fields.Char()
    is_kyso_mobile = fields.Boolean(string='Dùng ký số mobile', compute='_compute_kyso')
    is_kyso_smartca = fields.Boolean(string='Dùng ký số Smartca', compute='_compute_kyso')

    @api.onchange('hinhthuc_kyso_ids')
    def onchange_hinhthuc_kyso(self):
        if self.taikhoan_smartca:
            return
        else:
            for item in self.hinhthuc_kyso_ids:
                if item.code == 'smart_ca':
                    self.env.cr.execute('''select coalesce(socancuoc, identification_id) as tk_smart_ca
                                        from hr_employee where user_id = %s;''', (self.env.user.id, ))
                    result = self.env.cr.dictfetchone()
                    if result and result.get('tk_smart_ca'):
                        self.taikhoan_smartca = result.get('tk_smart_ca')
                    break

    @api.constrains('chu_ky')
    def check_chu_ky(self):
        if self.chu_ky:
            file_name_split = self.file_name.split('.')
            if file_name_split and file_name_split[len(file_name_split) - 1] != 'png':
                raise ValidationError(_('Chữ ký không đúng định dạng png'))

    @api.depends('hinhthuc_kyso_ids')
    def _compute_kyso(self):
        is_kyso_mobile = False
        is_kyso_smartca = False
        if self.hinhthuc_kyso_ids:
            for item in self.hinhthuc_kyso_ids:
                if item.code == 'mobile_pki':
                    is_kyso_mobile = True
                if item.code == 'smart_ca':
                    is_kyso_smartca = True
        self.is_kyso_mobile = is_kyso_mobile
        self.is_kyso_smartca = is_kyso_smartca

    @api.constrains('sdt_pki')
    def check_sdt_pki(self):
        if not self.sdt_pki:
            return
        if self.sdt_pki[0] != '0':
            raise ValidationError(_(u'Lỗi thông tin số điện thoại.\nSố điện thoại phải bắt đầu là số 0'))
        if re.match("^[-+]?[0-9]+$", self.sdt_pki) is None:
            raise ValidationError(_(u'Lỗi thông tin số điện thoại.\nSố điện thoại chỉ được nhập số 0-9'))
        if len(self.sdt_pki) != 10:
            raise ValidationError(_(u'Lỗi thông tin số điện thoại.\nĐộ dài số điện thoại di động bằng 10 chữ số'))
        return


class SelectHinhThucKySo(models.TransientModel):
    _name = 'temp_model_kyso'

    def get_selection(self):
        user = self.env.user
        user = self.env['hr.employee'].search([('user_id', '=',user.id)])
        if user.hinhthuc_kyso_ids:
            hinhthuc_kyso_ids = user.hinhthuc_kyso_ids
        else:
            hinhthuc_kyso_ids = self.env['hinhthuc_kyso'].search([('is_active', '=', True)])
        result = []
        for item in hinhthuc_kyso_ids:
            result.append((item.code, item.name))
        return result

    def get_default(self):
        result = self.get_selection()
        return result[0][0]

    hinhthuc_kyso = fields.Selection(
        string='Hình thức ký số',
        selection=get_selection,
        required=True, default=get_default)
    name = fields.Text(string='Thông báo')
    is_next_default = fields.Boolean(string='Đặt làm mặc định cho lần tiếp theo')

    def open_config(self):
        view = self.env.ref('base.view_users_form_simple_modif')
        view_id = view and view.id or False
        return {
            'name': 'Thay đổi tùy chỉnh cá nhân',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.env.user.id,
            'res_model': 'res.users',
            'views': [(view.id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }

    @api.model
    def get_view_tai_plugin(self):
        view = self.env.ref('vnpt_ky_so.tai_plugin_kyso_view')
        view_id = view and view.id or False
        return {
            'name': 'Thông báo',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'temp_model_kyso',
            'views': [(view.id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }


