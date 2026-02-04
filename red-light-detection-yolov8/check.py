import cv2
from tkinter import Tk, filedialog
#by Truong Viet Tran , do not reup ,sdt:0877973723
# === Hộp thoại chọn video ===
root = Tk()
root.withdraw()  # Ẩn cửa sổ chính của Tkinter
video_path = filedialog.askopenfilename(
    title="Chọn video để kiểm tra tọa độ",
    filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
)
root.destroy()

if not video_path:
    print("❌ Không có video được chọn.")
    exit()

# === Callback khi click chuột ===
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"👉 Click tại: x={x}, y={y}")
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)  # tạo ra chấm đỏ
        cv2.putText(param, f"({x},{y})", (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow("Pick Points", param)

# === Mở video ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Không thể mở video.")
    exit()

# Lấy frame đầu tiên
ret, frame = cap.read()
if not ret:
    print("❌ Không thể đọc frame đầu tiên.")
    exit()

cv2.namedWindow("Pick Points", cv2.WINDOW_NORMAL)
cv2.imshow("Pick Points", frame)

# Gắn hàm click
cv2.setMouseCallback("Pick Points", click_event, frame)

print("✅ Click chuột trái để xem tọa độ. Nhấn 'q' để thoát.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
