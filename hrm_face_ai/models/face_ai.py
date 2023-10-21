from odoo import models, fields, api, _
from odoo.http import request

#FACE AI
import cv2, os
import numpy as np
from PIL import Image


class EmployeeProfile(models.Model):
    _inherit = 'hrm.employee.profile'
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
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        # Lấy các khuôn mặt và ID từ thư mục dataSet
        faceSamples, Ids = self.getImagesAndLabels('custom_addons/hrm_face_ai/dataSet')
        # Train model để trích xuất đặc trưng các khuôn mặt và gán với từng nahan viên
        recognizer.train(faceSamples, np.array(Ids))
        # Lưu model
        recognizer.save('custom_addons/hrm_face_ai/recognizer/trainner.yml')
        print("Trained!")

    def getProfile(self, id):
        SQL = ''
        SQL += '''SELECT * FROM hrm_employee_profile WHERE id=%s'''%(id)
        cr = self.env.cr
        cr.execute(SQL)
        datas = cr.dictfetchall()
        profile = None
        for row in datas:
            profile = row
        return profile

    def chamcong_face_ai(self):
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
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Thông báo điểm danh'),
                    'message': 'Điểm danh thành công',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': True,  # True/False will display for few seconds if false
                },
            }
            return notification
        else:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Thông báo điểm danh'),
                    'message': 'Bạn chưa điểm danh thành công, và bạn đã thoát điểm danh!',
                    'type': 'warningq',  # types: success,warning,danger,info
                    'sticky': True,  # True/False will display for few seconds if false
                },
            }
            return notification






