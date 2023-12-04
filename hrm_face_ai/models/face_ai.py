from odoo import models, fields, api, _
from odoo.http import request
from datetime import datetime,time, timedelta
from dateutil.relativedelta import relativedelta

#FACE AI
import cv2, os
import numpy as np
from PIL import Image
import shutil


class EmployeeProfile(models.Model):
    _inherit = 'hr.employee'
    _description = 'Bảng thông tin nhân viên'

    def loaf_face_ai_user_new(self):
        cam = cv2.VideoCapture(0)
        # Tạo một cửa sổ pop-up mới và di chuyển nó lên đầu tiên
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)
        detector = cv2.CascadeClassifier('custom_addons/hrm_face_ai/views/haarcascade_frontalface_alt.xml')
        sampleNum = 0
        id = self.id

        while (True):

            ret, img = cam.read()

            # Lật ảnh cho đỡ bị ngược
            img = cv2.flip(img, 1)

            # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
            centerH = img.shape[0] // 2
            centerW = img.shape[1] // 2
            sizeboxW = 300
            sizeboxH = 400
            cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                          (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

            # Đưa ảnh về ảnh xám
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Nhận diện khuôn mặt
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                # Vẽ hình chữ nhật quanh mặt nhận được
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                # Ghi dữ liệu khuôn mặt vào thư mục dataSet
                cv2.imwrite("custom_addons/hrm_face_ai/dataSet/User." + str(id) + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

            cv2.imshow('frame', img)
            # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break

        cam.release()
        cv2.destroyAllWindows()

    def getImagesAndLabels(self, path):
        detector = cv2.CascadeClassifier("custom_addons/hrm_face_ai/views/haarcascade_frontalface_alt.xml")
        # Lấy tất cả các file trong thư mục
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empth face list
        faceSamples = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            if (imagePath[-3:] == "jpg"):
                print(imagePath[-3:])
                # loading the image and converting it to gray scale
                pilImage = Image.open(imagePath).convert('L')
                # Now we are converting the PIL image into numpy array
                imageNp = np.array(pilImage, 'uint8')
                # getting the Id from the image
                Id = int(os.path.split(imagePath)[-1].split(".")[1])
                # extract the face from the training image sample
                faces = detector.detectMultiScale(imageNp)
                # If a face is there then append that in the list as well as Id of it
                for (x, y, w, h) in faces:
                    faceSamples.append(imageNp[y:y + h, x:x + w])
                    Ids.append(Id)
        return faceSamples, Ids


    def accept_face_ai(self):
        try:
            # #Code xóa thi thêm mới
            # recognizer = cv2.face.LBPHFaceRecognizer_create()
            # # Lấy các khuôn mặt và ID từ thư mục dataSet
            # faceSamples, Ids = self.getImagesAndLabels('custom_addons/hrm_face_ai/dataSet')
            # # Train model để trích xuất đặc trưng các khuôn mặt và gán với từng nahan viên
            # recognizer.train(faceSamples, np.array(Ids))
            # # Lưu model
            # recognizer.save('custom_addons/hrm_face_ai/recognizer/trainner.yml')

            model_path = 'custom_addons/hrm_face_ai/recognizer/trainner.yml'

            if os.path.exists(model_path):
                # Nếu tệp model đã tồn tại, đọc model từ tệp
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(model_path)
            else:
                # Nếu tệp model không tồn tại, tạo mới model
                recognizer = cv2.face.LBPHFaceRecognizer_create()

            # Lấy các khuôn mặt và ID từ thư mục dataSet
            faceSamples, Ids = self.getImagesAndLabels('custom_addons/hrm_face_ai/dataSet')

            if os.path.exists(model_path):
                # Nếu tệp model đã tồn tại, ghi thêm vào model hiện có
                recognizer.update(faceSamples, np.array(Ids))
            else:
                # Nếu tệp model không tồn tại, train model từ đầu
                recognizer.train(faceSamples, np.array(Ids))

            # Lưu model
            recognizer.save(model_path)
            #Xóa ảnh
            folder_path = 'custom_addons/hrm_face_ai/dataSet'

            # Kiểm tra xem thư mục tồn tại
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                # Lặp qua tất cả các file và thư mục trong thư mục
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    # Kiểm tra xem nó là tệp tin hay thư mục
                    if os.path.isfile(file_path):
                        # Xóa tệp tin
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        # Xóa thư mục (với tất cả các tệp tin và thư mục con bên trong)
                        shutil.rmtree(file_path)

            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Duyệt chấm công FaceAi!'),
                    'message': 'Duyệt thành công',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification
        except:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Duyệt chấm công FaceAi!'),
                    'message': 'Bạn chưa duyệt thành công, vui lòng kiểm tra lại!!',
                    'type': 'danger',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    def getProfile(self, id):
        SQL = ''
        SQL += '''SELECT * FROM hr_employee WHERE id=%s'''%(id)
        cr = self.env.cr
        cr.execute(SQL)
        datas = cr.dictfetchall()
        profile = None
        for row in datas:
            profile = row
        return profile

    def chamcong_face_ai(self):
        try:
            # Khởi tạo bộ phát hiện khuôn mặt
            faceDetect = cv2.CascadeClassifier('custom_addons/hrm_face_ai/views/haarcascade_frontalface_alt.xml')

            # Khởi tạo bộ nhận diện khuôn mặt
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read('custom_addons/hrm_face_ai/recognizer/trainner.yml')

            id = 0
            # set text style
            fontface = cv2.FONT_HERSHEY_SIMPLEX
            fontscale = 1
            fontcolor = (0, 255, 0)
            fontcolor1 = (0, 0, 255)

            # Hàm lấy thông tin người dùng qua ID

            # Khởi tạo camera
            cam = cv2.VideoCapture(0)
            check_thoat = False

            # Tạo một cửa sổ pop-up mới và di chuyển nó lên đầu tiên
            cv2.namedWindow('Face', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Face', cv2.WND_PROP_TOPMOST, 1)
            name_employee = ''
            employee_id_login = 0
            while True:
                # Đọc ảnh từ camera
                ret, img = cam.read()

                # Lật ảnh cho đỡ bị ngược
                img = cv2.flip(img, 1)

                # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
                centerH = img.shape[0] // 2
                centerW = img.shape[1] // 2
                sizeboxW = 300
                sizeboxH = 400
                cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                              (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

                # Chuyển ảnh về xám
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Phát hiện các khuôn mặt trong ảnh camera
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)

                # Lặp qua các khuôn mặt nhận được để hiện thông tin
                for (x, y, w, h) in faces:
                    # Vẽ hình chữ nhật quanh mặt
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (dộ sai khác)
                    id, dist = recognizer.predict(gray[y:y + h, x:x + w])

                    profile = None

                    # Nếu độ sai khác < 25% thì lấy profile
                    if dist <= 70:
                        profile = self.getProfile(id)

                    # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
                    if profile is not None:
                        cv2.putText(img, "Name: " + str(profile['name']), (x, y + h + 30), fontface, fontscale, fontcolor,
                                    2)
                        name_employee = str(profile['name'])
                        employee_id_login = profile['id']
                        check_thoat = True
                    else:
                        cv2.putText(img, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)

                cv2.imshow('Face', img)

                # Nếu nhấn q thì thoát
                if cv2.waitKey(1) == ord('q') or check_thoat:
                    break

            cam.release()
            cv2.destroyAllWindows()

            if check_thoat:
                SQL = ''
                SQL += '''SELECT emp.id AS employee_id, hrbl.id as department_id, hrbl.name as department_name
                       FROM hr_employee emp INNER JOIN res_users lg ON lg.id = emp.acc_id 
                       INNER JOIN hr_department hrbl ON hrbl.id = emp.department_id
                       WHERE lg.id = %s;'''%(self.env.user.id, )
                cr = self.env.cr
                cr.execute(SQL)
                datas = cr.dictfetchall()
                data = datas[0]
                if data['employee_id'] == employee_id_login:
                    self.create_or_write_checkin_checkout(data.get('employee_id'), data.get('department_id'), data.get('department_name'))
                    notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': ('Thông báo điểm danh'),
                            'message': 'Điểm danh thành công nhân viên %s' % (name_employee),
                            'type': 'success',  # types: success,warning,danger,info
                            'sticky': False,  # True/False will display for few seconds if false
                        },
                    }
                else:
                    notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': ('Thông báo điểm danh'),
                            'message': 'Điểm danh không thành công thành công nhân viên %s' % (name_employee),
                            'type': 'warning',  # types: success,warning,danger,info
                            'sticky': False,  # True/False will display for few seconds if false
                        },
                    }
                return notification

        except:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Thông báo điểm danh'),
                    'message': 'Điểm danh thất bại. Nếu đây là lỗi hãy báo lại nhân viên phòng máy.',
                    'type': 'danger',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    def create_or_write_checkin_checkout(self, employee_id, department_id, department_name):
        #Check xem có bản ghi đó chưa
        current_date = datetime.today().date()
        employee = self.env['datn.hr.checkin.checkout.line'].search([('day', '=', current_date),('employee_id', '=', employee_id)])
        now = datetime.now()  # Lấy thời gian hiện tại
        start_month = now.replace(day=1).date()
        end_month = start_month + relativedelta(day=31)
        cr = self.env.cr
        SQL1 = '''select*from datn_hr_checkin_checkout where date_from = '%s' and department_id = %s '''% (start_month, department_id)
        cr.execute(SQL1)
        datas = cr.dictfetchall()
        if len(datas) > 0:
            parent_checkin_checkout = datas[0]
        else:
            parent_checkin_checkout = []
        if not parent_checkin_checkout:
            name = 'Bảng chấm công tháng %s của Đơn vị/ phòng ban %s'%(start_month, department_name)
            SQL2 = '''INSERT INTO datn_hr_checkin_checkout (name, department_id, date_from, date_to, state) VALUES (%s, %s, %s,%s, %s)'''
            values = (name, department_id, start_month, end_month, 'draft')
            cr.execute(SQL2, values)

            cr.execute(SQL1)
            datas = cr.dictfetchall()
            if len(datas) > 0:
                parent_checkin_checkout = datas[0]
            else:
                parent_checkin_checkout = []
        if not employee:
            target_time = time(hour=10)
            checkin_time_io = datetime.now()
            # Giá trị thời gian muốn so sánh
            checkin_time = datetime.now().time() # Trích xuất giá trị thời gian hiện tại
            SQL3 = '''INSERT INTO datn_hr_checkin_checkout_line (checkin_checkout_id, employee_id, checkin, day, note) VALUES (%s, %s, '%s', '%s', '%s');''' %(parent_checkin_checkout['id'], employee_id, checkin_time_io, current_date, 'Quên chấm công ra')
            if target_time <= checkin_time:
                SQL3 = ''
                SQL3 +='''INSERT INTO datn_hr_checkin_checkout_line (checkin_checkout_id, employee_id, checkout, day, note) VALUES (%s, %s, '%s','%s','%s');'''%(parent_checkin_checkout['id'], employee_id, checkin_time_io, current_date, 'Quên chấm công vào')
            cr.execute(SQL3)
        else:
            #nếu đã tồn tại thì sẽ đc update vào checkout
            line = self.env['datn.hr.checkin.checkout.line'].sudo().browse(employee.id)
            note = ''
            if line.checkin:
                time_difference = datetime.now() - line.checkin
                timeofday = round(time_difference.total_seconds() / 3600, 2)
            else:
                timeofday = 0
                note = 'Quên chấm công vào'
            values = {
                'day': current_date,
                'checkout': datetime.now(),
                'checkin': line.checkin,
                'timeofday': timeofday,
                'note': note
            }
            line.write(values)
            return line










