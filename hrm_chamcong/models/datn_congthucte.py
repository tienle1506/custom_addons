import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError



def _default_date_from(self):
    return datetime.today().strftime('%Y-%m-01')


def _default_date_to(self):
    return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')
class DATNCongThucTe(models.Model):
    _name = 'datn.congthucte'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Công thực tế'
    _order = "date_from DESC"

    name = fields.Char(string=u'Bảng chấm công tháng', size=128, track_visibility='always', )
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from, )
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    department_id = fields.Many2one('hr.department',ondelete='cascade', string=u'Đơn vị/ Phòng ban', required=True)
    item_ids = fields.One2many('datn.congthucte.line', 'congthucte_id')
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    chamcong_id = fields.Integer(string='Bảng chấm công tháng', required=True)
    create_date = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d', default=fields.Date.today)

    _sql_constraints = [
        ('unique_chamcong_id', 'unique(chamcong_id)', u'Bản ghi này đã được tạo')
    ]
    @api.onchange('date_from')
    def onchange_date_from(self):
        if self.date_from:
            date_from_str = self.date_from.strftime('%Y-%m-%d')
            year, month, _ = map(int, date_from_str.split('-'))
            _, last_day = calendar.monthrange(year, month)
            date_to = f'{year}-{month:02d}-{last_day:02d}'
            date_from = datetime.strptime(str(self.date_from), '%Y-%m-%d').replace(day=1)
            self.date_to = date_to
            self.date_from = date_from

    def unlink(self):
        if self._context['view_from_action'] == 'datn_congthucte':
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được tạo từ bảng công tháng, Nếu muốn xoá, bạn thực hiên xoá bảng chấm công tháng.")
        return super(DATNCongThucTe, self).unlink()




class DATNCongThucTeLine(models.Model):
    _name = 'datn.congthucte.line'
    _inherit = ['mail.thread']
    _description = u'Công thực tế chi tiết'
    _order = "date_from DESC"

    employee_id = fields.Many2one('hr.employee', ondelete='cascade', string=u'Nhân viên', required=True)
    department_id = fields.Many2one('hr.department', ondelete='cascade', related='employee_id.department_id', store=True, string=u'Đơn vị/ Phòng ban', required=True)
    congthucte_id = fields.Many2one('datn.congthucte', ondelete='cascade', string=u'Công thực tế')
    date_from = fields.Date(u'Từ ngày', related='congthucte_id.date_from', store=True)
    date_to = fields.Date(u'Đến ngày', related='congthucte_id.date_from', store=True)
    cong_chuan = fields.Float(u'Công chuẩn')
    cong_thuc_te = fields.Float(u'Công thực tế')
    cong_phep = fields.Float(u'Công phép')
    cong_khong_luong = fields.Float(u'Công không lương')
    cong_co_luong = fields.Float(u'Công có lương')
    cong_tang_ca = fields.Float(u'Công tăng ca')
    cong_nghi_khong_ly_do = fields.Float(u'Công nghỉ không lý do')
    def unlink(self):
        if self._context['view_from_action'] == 'datn_congthucte_line':
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được tạo từ bảng công tháng, Nếu muốn xoá, bạn thực hiện xoá bảng chấm công tháng.")
        return super(DATNCongThucTeLine, self).unlink()
