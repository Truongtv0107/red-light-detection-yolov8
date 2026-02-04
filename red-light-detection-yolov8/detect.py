import cv2
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QImage, QPixmap
from ultralytics import YOLO

#by Truong Viet Tran , do not reup ,sdt:0877973723
# =============================
# Luồng xử lý video song song
# =============================
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, source):
        super().__init__()
        self.source = source
        self.running = True
        self.model = YOLO("yolov8n.pt")  # Model nhẹ, nhận diện COCO (xe, người, ô tô...)

    def run(self):
        cap = cv2.VideoCapture(self.source)
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Nhận diện đối tượng
            results = self.model(frame)
            annotated = results[0].plot()

            # Chuyển khung hình sang định dạng PyQt hiển thị
            rgb_image = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            scaled = qt_image.scaled(640, 360, Qt.AspectRatioMode.KeepAspectRatio)
            self.change_pixmap_signal.emit(scaled)

        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


# =============================
# Giao diện nhận diện phương tiện
# =============================
class DetectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Nhận diện phương tiện")
        self.setFixedSize(700, 500)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("🚗 NHẬN DIỆN PHƯƠNG TIỆN TRÊN VIDEO")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_label = QLabel("Chưa có video hiển thị")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: #000; color: white;")
        self.video_label.setFixedSize(640, 360)

        self.btn_open = QPushButton("📂 Chọn video để phân tích")
        self.btn_open.clicked.connect(self.open_video)

        self.btn_stop = QPushButton("⏹ Dừng lại")
        self.btn_stop.clicked.connect(self.stop_video)
        self.btn_stop.setEnabled(False)

        self.layout.addWidget(title)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.video_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.btn_stop)
        self.setLayout(self.layout)

        self.thread = None

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Video Files (*.mp4 *.avi)")
        if file_path:
            self.btn_open.setEnabled(False)
            self.btn_stop.setEnabled(True)
            QMessageBox.information(self, "Đang xử lý", f"Phân tích video:\n{file_path}")

            self.thread = VideoThread(file_path)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()

    def update_image(self, qt_image):
        """Hiển thị khung hình lên QLabel"""
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def stop_video(self):
        if self.thread:
            self.thread.stop()
            self.btn_open.setEnabled(True)
            self.btn_stop.setEnabled(False)
            QMessageBox.information(self, "Tạm dừng", "Đã dừng phát video.")

    def closeEvent(self, event):
        """Dừng luồng khi đóng cửa sổ"""
        if self.thread:
            self.thread.stop()
        event.accept()
