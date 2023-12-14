
import calendar
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError

class DATNHrLuongThang(models.Model):
    _name = 'datn.luongthang'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Chấm công theo tháng'
    _order = "date_from DESC"

    def _default_date_from(self):
        return datetime.today().strftime('%Y-%m-01')

    def _default_date_to(self):
        return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')


    name = fields.Char(string=u'Bảng tính lương tháng', size=128, track_visibility='always', )
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from,)
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    department_id = fields.Many2one('hr.department',ondelete='cascade', string=u'Đơn vị/ Phòng ban', required=True)
    item_ids = fields.One2many('datn.luongthang.line', string='Danh sách nhân viên', inverse_name='luongthang_id',track_visibility='always')
    nguoi_duyet = fields.Many2many('hr.employee', 'employee_duyet_luong_rel', 'luongthang_id', 'employee_id', string="Người duyệt")
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'),
                              ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ngay_chi_tra = fields.Date(u'Ngày chi trả', required=True)

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        nguoi_duyet = []
        for emp in self.nguoi_duyet:
            if emp.personal_email:
                nguoi_duyet.append(emp.personal_email.strip())
        header = '''Thông báo phê duyệt đơn tăng ca của %s''' % (self.employee_id.name)
        content = u'Nhân viên %s tạo đơn tăng ca \nLý do: %s \nSố giờ tăng ca:%s\nTừ ngày: %s - đến ngày: %s \nTrang web: http://localhost:8088/web' % (
        str(self.employee_id.name), str(self.ly_do), str(self.so_gio_tang_ca),
        self.date_from.strftime('%d/%m/%Y'), self.date_to.strftime('%d/%m/%Y'))
        if nguoi_duyet and len(nguoi_duyet) > 0:
            self.env['my.mail.sender'].send_mail_to_customer(nguoi_duyet, header, content)
        self.state = 'confirmed'

    def action_refuse(self):
        self.state = 'refused'

    def action_approve(self):
        self.state = 'approved'

    def unlink(self):
        # Kiểm tra điều kiện trước khi thực hiện unlink
        if self.state == 'draft':
            # Thực hiện unlink chỉ khi điều kiện đúng
            super().unlink()  # Gọi phương thức unlink gốc
        else:
            # Xử lý khi điều kiện không đúng
            # ví dụ:
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")
    def action_loaddata(self):
        self.item_ids.unlink()
        self.item_ids.item_ids.unlink()
        cr = self.env.cr
        SQL = ''
        SQL += '''SELECT ckl.* FROM datn_congthucte_line ckl
                            LEFT JOIN datn_congthucte ck ON ck.id = ckl.congthucte_id
                            WHERE ckl.department_id = ANY(ARRAY(SELECT child_ids FROM child_department WHERE parent_id = %s)) AND ck.date_from = '%s'
                            AND  ck.date_to = '%s'
                            AND ckl.employee_id not in (SELECT ccl.employee_id FROM datn_luongthang cc INNER JOIN datn_luongthang_line ccl ON ccl.luongthang_id = cc.id 
                    where cc.date_from >= '%s' and cc.date_to <= '%s')
                            ORDER BY ckl.employee_id
                    ''' % (self.department_id.id, self.date_from, self.date_to, self.date_from, self.date_to)
        cr.execute(SQL)
        employees = cr.dictfetchall()
        mang_quy_tacs = self.env['datn.quytacluong'].search([('hieuluc', '=', True)], order='index')
        LCB = 0

        if employees:
            for i in range(0, len(employees)):
                SQL = ''
                SQL += '''SELECT*FROM datn_dieuchinh_line WHERE type='luong' and ngay_hieu_luc <= '%s' and (ngay_ket_thuc >= '%s' OR ngay_ket_thuc ISNULL) AND employee_id = %s '''%(self.date_from, self.date_to, employees[i].get('employee_id'))
                cr.execute(SQL)
                muc_luong = cr.dictfetchall()
                if muc_luong:
                    LCB = int(muc_luong.get('muc_huong'))
                else:
                    LCB = 0
                lines = {
                    'employee_id': employees[i].get('employee_id'),
                    'department_id': employees[i].get('department_id'),
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'tong_tien': 0,
                    'luongthang_id': self.id
                }
                new_luong_line = self.env['datn.luongthang.line'].create(lines)
                namespace = {

                }
                if mang_quy_tacs:
                    for j in range(0, len(mang_quy_tacs)):
                        mang_quy_tac = {}
                        namespace['luong_co_ban'] = LCB
                        namespace['cong_chuan'] = employees[i].get('cong_chuan')
                        namespace['cong_thuc_te'] = employees[i].get('cong_thuc_te')
                        mang_quy_tac['bangluong_id'] = new_luong_line.id
                        # Thực thi chuỗi mã bằng hàm exec() trong namespace
                        exec(mang_quy_tacs[j].mapython, namespace)
                        mang_quy_tac['code'] = mang_quy_tacs[j].code
                        mang_quy_tac['tong_tien'] = namespace.get('result')
                        # Xóa phần tử thứ hai từ dưới lên
                        index2 = len(namespace) - 1
                        namespace.pop(list(namespace.keys())[index2])

                        # Xóa phần tử thứ ba từ dưới lên
                        index3 = len(namespace) - 1
                        namespace.pop(list(namespace.keys())[index3])
                        namespace[mang_quy_tacs[j].code] = mang_quy_tac['tong_tien']
                        mang_quy_tac['name'] = mang_quy_tacs[j].name
                        mang_quy_tac['index'] = mang_quy_tacs[j].index

                        if mang_quy_tac['code'] == 'TTNTN':
                            new_luong_line.write({
                                'tong_tien': mang_quy_tac['tong_tien']
                            })

                        self.env['datn.bangluong'].create(mang_quy_tac)

    @api.onchange('date_from', 'department_id')
    def onchange_name(self):
        name = 'Bảng tính lương tháng %s năm %s Đơn vị/ phòng ban %s'%(str(self.date_from.month), str(self.date_from.year), self.department_id.name)
        self.name = name

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


class DATNHrLuongThangLine(models.Model):
    _name = 'datn.luongthang.line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Danh sách nhân viên'
    _order = "date_from DESC"

    employee_id = fields.Many2one('hr.employee', string="Nhân viên", ondelete='cascade')
    department_id = fields.Many2one('hr.department', string="Đơn vị/ phòng ban", ondelete='cascade',
                                    related='employee_id.department_id', store=True)
    luongthang_id = fields.Many2one('datn.luongthang', string="Danh sách nhân sự", ondelete='cascade')
    date_from = fields.Date(u'Từ ngày', related='luongthang_id.date_from', stored=True)
    date_to = fields.Date(u'Đến ngày', related='luongthang_id.date_to', stored=True)
    tong_tien = fields.Integer(u'Tổng tiền',)
    item_ids = fields.One2many('datn.bangluong', string='Chi tiết bảng lương', inverse_name='bangluong_id',track_visibility='always')

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNHrLuongThangLine, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNHrLuongThangLine, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrLuongThangLine, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrLuongThangLine, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNHrLuongThangLine, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
    def check_employee_view(self):
        context = self.env.context or {}
        emp_domain = []
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        return emp_domain


class DATNHrBangLuong(models.Model):
    _name = 'datn.bangluong'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Bảng lương'
    _order = "index DESC"

    bangluong_id = fields.Many2one('datn.luongthang.line', string="Nhân viên", ondelete='cascade')
    code = fields.Char('Mã')
    name = fields.Char('Tên')
    index = fields.Integer('Thứ tự')
    tong_tien = fields.Integer('Tổng tiền')

    _sql_constraints = [
        ('unique_code', 'unique(bangluong_id,code)', u'Mã quy tắc đã được tạo')
    ]