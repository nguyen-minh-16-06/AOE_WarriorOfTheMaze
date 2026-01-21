# AOE – CHIẾN BINH MÊ CUNG (Q-Learning Maze Solver)
Dự án này là một hệ thống mô phỏng giải mê cung sử dụng học tăng cường với thuật toán Q-Learning. Chiến binh sẽ học cách di chuyển trong mê cung để tìm và tiêu diệt các mục tiêu trong mê cung một cách hiệu quả nhất. Hệ thống cung cấp giao diện trực quan bằng PyGame, đồng thời ghi log và trực quan hóa kết quả huấn luyện bằng Matplotlib.

## Cấu trúc thư mục dự án
```
.
├── src/
│   ├── environment.py        # Môi trường mê cung (Maze Environment)
│   ├── q_learning.py         # Cài đặt thuật toán Q-Learning
│   ├── renderer.py           # Hiển thị và animation
│   ├── asset_manager.py      # Quản lý hình ảnh, tài nguyên
│   └── config.py             # Các tham số cấu hình (kích thước màn hình, ...)
│
├── main.py                   # Chạy mô phỏng mê cung với Agent đã huấn luyện
├── train.py                  # Huấn luyện agent bằng Q-Learning
├── requirements.txt          # Danh sách thư viện cần cài đặt
└── README.md
```

## Cài đặt và thiết lập

### 1. Yêu cầu hệ thống

- Python 3.10.11 hoặc cao hơn.
- `pip` và `venv`.

### 2. Cài đặt thư viện

Clone project và cài đặt các thư viện cần thiết:

```bash
# Clone kho lưu trữ về máy tính của bạn
git clone https://github.com/nguyen-minh-16-06/AOE_WarriorOfTheMaze.git

# Điều hướng đến thư mục của dự án
cd AOE_WarriorOfTheMaze

# Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

## Huấn luyện mô hình (Q-Learning)

Trước khi chạy mô phỏng, bạn cần huấn luyện Agent để tạo Q-Table (q_table.pkl).

```bash
python train.py
```

Quá trình huấn luyện sẽ:

- Chạy 10.000 episode.

- Lưu log huấn luyện tại:

```bash
results/training/training_log.csv
```

- Sinh các biểu đổ:
    - Số Epsilon trong một Eposide
 
    - Số bước trong một Episode
  
    - Phần thưởng trung bình trong 100 tập

- Lưu model huấn luyện tại:

```bash
q_table.pkl
```

## Chạy mô phỏng mê cung

Sau khi đã huấn luyện xong, thực thi câu lệnh sau:

```bash
python main.py
```

### Điều khiển trong lúc chơi:

- SPACE: Bật / tắt chế độ Agent thực hiện nhiệm vụ.
- S: Lưu lại Q-table.
- R: Reset toàn bộ mê cung.
- Q: Thoát chương trình.

## Quy trình hoạt động của hệ thống

### 1. Huấn luyện (`train.py`)

- Khởi tạo môi trường mê cung (`MazeEnv`).

- Agent học cách:

  - Di chuyển tối ưu.
  
  - Tránh lặp vô hạn.
  
  - Tiêu diệt toàn bộ mục tiêu.
  
- Q-table được cập nhật liên tục dựa trên:

```bash
(state, action, reward, next_state)
```

### 2. Mô phỏng & đánh giá (`main.py`)

- Load Q-table đã huấn luyện.

- Agent tự động:

  - Chọn mục tiêu.
  
  - Di chuyển trong mê cung.
  
  - Ghi lại các thông số, bao gồm:

    - Số bước.

    - Thời gian đi tìm và kết liễu cho mỗi mục tiêu.

- Kết quả được lưu tại:

```bash
results/test/
├── run_log.csv
├── Thời gian tìm ra mục tiêu của 1 Episode
└── Số bước trong một Episode
```

## Kết quả đầu ra
- CSV log:

  - Thời gian hoàn thành từng mục tiêu
 
- Biểu đồ:

  - Thời gian tìm mục tiêu.
  
  - Số bước trên mỗi episode.

- Mô phỏng trực quan:

  - Hiển thị mê cung, Agent và mục tiêu theo thời gian thực.

## Thư viện sử dụng

- pygame

- numpy

- matplotlib

- pillow

(chi tiết xem trong `requirements.txt`)

## Ghi chú:

- Dự án phù hợp cho:

  - Học Reinforcement Learning.
 
  - Mô phỏng AI tìm đường.
 
  - Demo Q-learning trực quan.

- Có thể mở rộng:

  - Deep Q-Learning (DQN).
  
  - Thêm nhiều Agent.
  
  - Bản đồ động.
