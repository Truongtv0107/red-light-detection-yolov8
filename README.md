Traffic Violation Detection using YOLOv8 
Giới thiệu

Dự án này xây dựng hệ thống nhận diện vi phạm giao thông sử dụng YOLOv8 và Computer Vision.
Được xây dựng bởi : Trần Việt Trường ( SĐT 0333999726)
Hệ thống có khả năng:

Phát hiện phương tiện giao thông

Theo dõi phương tiện

Phát hiện vượt đèn đỏ

Nhận diện biển số xe

Xuất báo cáo vi phạm

Ứng dụng trong:

Camera giao thông thông minh

Giám sát giao thông tự động

Nghiên cứu AI & Computer Vision

Công nghệ sử dụng

Python

YOLOv8 (Ultralytics)

OpenCV

Deep Learning

Object Tracking

Cấu trúc dự án
traffic-violation-detection
│
├── check.py
├── detect.py
├── license_plate.py
├── license_plate_detector.pt
│
├── redlight.py
├── redlight_violation.py
│
├── tracking_redlight_violation.py
│
├── report.py
│
├── main.py
│
└── yolov8n.pt
Mô tả các file
main.py

File chạy chính của chương trình, kết hợp tất cả các module để phát hiện vi phạm giao thông.

detect.py

Sử dụng YOLOv8 để phát hiện các phương tiện giao thông trong video hoặc camera.

tracking_redlight_violation.py

Theo dõi phương tiện và xác định phương tiện nào vượt qua vạch dừng khi đèn đỏ.

redlight_violation.py

Kiểm tra và xác định hành vi vượt đèn đỏ.

redlight.py

Xử lý trạng thái đèn giao thông (đỏ, vàng, xanh).

license_plate.py

Phát hiện và nhận diện biển số xe từ phương tiện vi phạm.

check.py

Kiểm tra vị trí phương tiện so với vạch dừng hoặc vùng vi phạm.

report.py

Tạo báo cáo vi phạm giao thông.
