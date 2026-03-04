# External-Merge-Sort

Bà tập môn học: Ứng dụng thuật toán K-Way Merge để sắp xếp các tập tin dữ liệu nhị phân có kích thước lớn (External Sorting). 

Được phát triển bằng **C++** và giao diện người dùng bằng **Python (CustomTkinter)**.

---

## Tính năng nổi bật (Features)

* **Lõi xử lý siêu tốc (High-Performance Core):** Đọc/ghi nhị phân trực tiếp (`double` - 8 bytes) và sử dụng cấu trúc dữ liệu **Min-Heap** cho quá trình K-Way Merge.
* **Quản lý RAM động (Dynamic Memory Allocation):** Cho phép người dùng giới hạn chính xác lượng RAM cấp phát (hỗ trợ các mốc từ GiB, MiB, KiB xuống tận Byte). Tự động phân chia khối dữ liệu (Chunks) tối ưu.
* **Giao diện Song ngữ (Bilingual UI):** Chuyển đổi mượt mà giữa Tiếng Việt (VI) và Tiếng Anh (EN) ngay trong lúc chạy (Runtime) mà không cần khởi động lại.
* **Chế độ minh họa (Illustrate Mode):** Tự động theo dõi và in chi tiết từng bước cắt/trộn dữ liệu ra Console Log đối với các tập tin nhỏ ($\le$ 100 phần tử), hỗ trợ tối đa cho việc trình bày thuật toán.
* **Tích hợp công cụ kiểm tra (Verification Tool):** Nút bấm một chạm để xác minh tập tin kết quả đã được sắp xếp tăng dần chuẩn xác hay chưa.

## Công nghệ sử dụng (Tech Stack)

* **Core:** C++ (Standard Template Library: `<queue>`, `<algorithm>`, `<fstream>`).
* **GUI:** Python 3 (Thư viện `customtkinter`, `tkinter`, `psutil`, `struct`, `subprocess`).
* **Packaging:** PyInstaller (Đóng gói lõi C++ và môi trường Python thành tệp thực thi độc lập).

## Cài đặt và Sử dụng (Installation & Usage)

### Tải bản chạy trực tiếp (Dành cho Windows)
Hệ thống đã được đóng gói sẵn thành tệp `.exe`, không cần cài đặt môi trường.
1. Truy cập vào mục [Releases](../../releases) bên góc phải của Repository này.
2. Tải xuống tệp `SapXepNhiPhan.exe`.
3. Chạy trực tiếp trên Windows và sử dụng.
