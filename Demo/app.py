import tkinter as tk
from tkinter import filedialog, OptionMenu, StringVar
from tkinter.ttk import Treeview, Scrollbar
from PIL import Image, ImageTk
import cv2
import dlib
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

def detect_faces(img):
    # Sử dụng dlib để nhận diện khuôn mặt
    detector = dlib.get_frontal_face_detector()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_img)
    return faces

def extract_text_and_table_data(image_path, language):
    # Đọc hình ảnh từ đường dẫn
    img = cv2.imread(image_path)

    # Nhận diện khuôn mặt từ hình ảnh
    faces = detect_faces(img)

    # Hiển thị số lượng khuôn mặt nhận diện được
    display_text(f"Number of faces detected: {len(faces)}")

    # Nhận diện văn bản từ hình ảnh
    text = pytesseract.image_to_string(img, lang=language)

    # Hiển thị văn bản nhận diện được
    display_text(text)

    # Phân tích số liệu từ hình ảnh
    table_data = extract_table_data(img)

    # Hiển thị kết quả phân tích số liệu
    display_table_data(table_data)

def extract_table_data(img):
    # Chuyển đổi ảnh sang ảnh đen trắng để nhận diện văn bản dễ dàng hơn
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện văn bản từ hình ảnh
    text = pytesseract.image_to_string(gray_img)

    # Tách dòng để có danh sách các dòng trong bảng
    lines = text.split('\n')

    # Tạo danh sách chứa các dòng số liệu
    table_data = []

    # Lặp qua từng dòng và phân tích số liệu
    for line in lines:
        # Tách số liệu từ dòng sử dụng khoảng trắng làm dấu phân cách
        data = line.split()

        # Kiểm tra xem dòng có chứa số liệu hay không
        if data:
            table_data.append(data)

    return table_data

def display_text(text):
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)

def display_table_data(table_data):
    # Xoá items cũ trong Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Thêm các items mới vào Treeview
    for i, row in enumerate(table_data, start=1):
        tree.insert("", "end", values=(i, *row))

def process_image():
    # Hỏi người dùng chọn hình ảnh
    image_path = filedialog.askopenfilename(title="Chọn hình ảnh", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])

    if image_path:
        # Hiển thị hình ảnh được chọn
        display_image(image_path)

        # Thực hiện phân tích và hiển thị kết quả
        selected_language = language_var.get()
        extract_text_and_table_data(image_path, selected_language)

def display_image(image_path):
    # Hiển thị hình ảnh trên giao diện
    img = Image.open(image_path)
    img = img.resize((900, 500))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("AI phân tích hình ảnh")

# Tạo các thành phần giao diện
process_button = tk.Button(root, text="Tải hình từ tệp", command=process_image)
process_button.pack(pady=10)

language_var = StringVar(root)
language_var.set("eng")  # Ngôn ngữ mặc định là tiếng Anh
language_menu = OptionMenu(root, language_var, "eng", "jpn", "vie")
language_menu.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

# Tạo Treeview cho kết quả phân tích số liệu
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)
tree = Treeview(tree_frame, columns=("Index", "Data"), show="headings")
tree.heading("Index", text="Index")
tree.heading("Data", text="Data")
tree.column("Index", width=50, anchor="center")
tree.column("Data", width=800, anchor="center")
tree.pack(side=tk.LEFT, fill=tk.Y)

# Tạo thanh cuộn cho Treeview
scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Tạo TextBox cho kết quả nhận diện văn bản
text_box = tk.Text(root, height=10, width=100, wrap=tk.WORD)
text_box.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
