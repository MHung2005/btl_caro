# PHƯƠNG PHÁP TRIỂN KHAI AI

## 1. Mô Hình Hóa Bàn Cờ

Bàn cờ được mô hình hóa dưới dạng **ma trận 2D kích thước 10×10** bằng NumPy:
- **Giá trị 0**: Ô trống (chưa có quân cờ)
- **Giá trị 1**: Quân của người chơi (X)
- **Giá trị -1**: Quân của AI (O)

Cấu trúc này cho phép các thuật toán dễ dàng truy cập, kiểm tra, và cập nhật trạng thái của bàn cờ.

---

## 2. Ràng Buộc & Điều Kiện Kết Thúc

Trò chơi kết thúc khi một trong các điều kiện sau được thỏa mãn:
- **Chiến thắng**: Một người chơi có 5 quân liên tiếp theo chiều ngang, dọc, hoặc đường chéo
- **Thua cuộc**: Đối thủ đạt 5 quân liên tiếp trên bàn cờ
- **Hoà**: Bàn cờ đầy mà không có người thắng

Hàm `check_win_all()` kiểm tra tất cả 4 hướng (ngang, dọc, 2 đường chéo) để xác định trạng thái thắng/thua/hoà.

---

## 3. Hàm Đánh Giá (Evaluation Function)

### 3.1 Nguyên Lý Hoạt Động

Hàm đánh giá `evaluate_window()` tính điểm cho mỗi "cửa sổ" 5 ô liên tiếp trên bàn cờ dựa trên số lượng quân của mỗi bên:

```
Điểm = f(quân_AI, quân_người, ô_trống)
```

### 3.2 Bảng Điểm Chi Tiết

| Mô tả | Điểm |
|-------|------|
| AI có 5 quân liên tiếp | +100000 (Chiến thắng) |
| AI có 4 quân + 1 ô trống | +1000 (Sắp thắng) |
| AI có 3 quân + 2 ô trống | +100 |
| AI có 2 quân + 3 ô trống | +10 |
| AI có 1 quân + 4 ô trống | +1 |
| Người chơi có 5 quân liên tiếp | -100000 (Sắp thua) |
| Người chơi có 4 quân + 1 ô trống | -1000 (Cần chặn) |
| Người chơi có 3 quân + 2 ô trống | -100 |
| Người chơi có 2 quân + 3 ô trống | -10 |

### 3.3 Hàm Tính Tổng Điểm

Hàm `get_total_score()` quét toàn bộ bàn cờ trong 4 hướng:
1. **Quét ngang**: Tất cả cửa sổ 5 ô liên tiếp theo hàng
2. **Quét dọc**: Tất cả cửa sổ 5 ô liên tiếp theo cột
3. **Quét đường chéo chính (↘)**: Tất cả cửa sổ từ trên-trái sang dưới-phải
4. **Quét đường chéo phụ (↙)**: Tất cả cửa sổ từ trên-phải sang dưới-trái

Điểm cuối cùng = Tổng tất cả điểm từ các cửa sổ.

---

## 4. Nước Đi Tiềm Năng (Move Generation)

### 4.1 Chiến Lược Giảm Không Gian Tìm Kiếm

Hàm `get_potential_moves()` **không xét tất cả ô trống**, mà chỉ xét những ô **lân cận với quân cờ đã đặt** (khoảng cách ≤ 1 ô):

```
Nước đi tiềm năng = {(r,c) | board[r,c] = 0 và ∃(r',c') láng giềng với board[r',c'] ≠ 0}
```

**Lợi ích**:
- Giảm đáng kể số lượng nước đi cần xét (từ ~100 xuống ~10-20 ô)
- Tập trung vào vùng chiến đấu chính
- Tăng tốc độ tìm kiếm cho các thuật toán

---

## 5. Ba Chế Độ AI

### 5.1 Chế Độ Heuristic (Tham Lam - Greedy)

#### Mô Tả
AI lựa chọn nước đi **tốt nhất ngay lập tức** dựa trên heuristic, **không tìm kiếm sâu** vào các nước đi sau:

```
Chọn nước (r,c) = argmax{điểm_tấn_công - điểm_phòng_thủ}
```

#### Thuật Toán
```
Với mỗi nước đi tiềm năng (r,c):
  1. Đặt quân AI tại (r,c) → Tính điểm tấn công (với quân AI)
  2. Hoàn tác, đặt quân người chơi → Tính điểm phòng thủ
  3. Hoàn tác
  4. Tính điểm tổng = tấn công - phòng thủ
  5. Chọn nước với điểm cao nhất
```

#### Ưu điểm
✓ **Cực nhanh**: O(n), với n = số nước đi tiềm năng  
✓ **Phù hợp cho trò chơi trực tuyến**: Phản ứng lập tức  
✓ **Tránh các bẫy cơ bản**: Chặn 4 quân, tấn công 4 quân  

#### Nhược điểm
✗ **Không tối ưu**: Có thể mắc bẫy trong 2-3 nước  
✗ **Không nhìn trước**: Không dự đoán nước của đối thủ  
✗ **Dễ bị đánh bại**: Đối thủ có kỹ năng tốt có thể thắng  

#### Độ Phức Tạp
- **Thời gian**: O(n × m²) trong đó n = số nước tiềm năng, m = chiều dài bàn cờ (10)
- **Không gian**: O(1) ngoài bàn cờ

---

### 5.2 Chế Độ Minimax (Tìm Kiếm Min-Max)

#### Mô Tả
AI **tìm kiếm toàn bộ cây trò chơi** đến độ sâu cố định và lựa chọn nước đi **đảm bảo tốt nhất** trong cả chuỗi nước sau:

```
Minimax(state, depth) = 
  {
    điểm_trạng_thái,                           nếu depth = 0 hoặc game_kết_thúc
    max{Minimax(child, depth-1)},              nếu AI tối đa hóa
    min{Minimax(child, depth-1)},              nếu đối thủ tối thiểu hóa
  }
```

#### Thuật Toán

**Bước 1: Gọi Minimax từ gốc**
```
AI chọn nước = argmax{Minimax(board_sau_nước, depth-1)}
```

**Bước 2: Minimax đệ quy**
- Nếu `depth = 0` hoặc game kết thúc → Trả về giá trị heuristic của trạng thái
- Nếu là lượt AI tối đa hóa (-1):
  - Với mỗi nước đi tiềm năng: Đặt quân AI, gọi đệ quy với đối thủ, hoàn tác
  - Trả về **max** của tất cả kết quả
- Nếu là lượt người chơi tối thiểu hóa (1):
  - Với mỗi nước đi tiềm năng: Đặt quân người, gọi đệ quy với AI, hoàn tác
  - Trả về **min** của tất cả kết quả

#### Ví Dụ Cây Tìm Kiếm (depth=2)
```
                    MAX (AI)
                   /    |    \
                MIN   MIN   MIN  (người chơi)
               / | \  / | \ / | \
             [val] (độ sâu = 0, đánh giá)
```

#### Ưu điểm
✓ **Tối ưu**: Đảm bảo tìm nước tốt nhất trong depth cho trước  
✓ **Nhìn trước**: Dự đoán được 2-3 nước tiếp theo  
✓ **Hợp lý**: Vừa tấn công vừa phòng thủ  

#### Nhược điểm
✗ **Cực chậm**: Độ phức tạp exponential O(b^d) với b = nhánh, d = độ sâu  
✗ **Giới hạn độ sâu**: Chỉ có thể tìm 3-4 nước trên bàn cờ 10×10  
✗ **Nhiều tính toán**: Hàng trăm hoặc hàng nghìn nút được đánh giá  

#### Độ Phức Tạp
- **Thời gian**: O(b^d) trong đó b ≈ 15-20 (nhánh trung bình), d = độ sâu
- **Không gian**: O(b×d) cho ngăn xếp đệ quy
- **Nút đánh giá**: ~5,000 - 50,000 nút tùy vào depth

---

### 5.3 Chế Độ Minimax với Cắt Tỉa Alpha-Beta

#### Mô Tả
**Cải tiến Minimax** bằng cách **cắt bỏ nhánh vô ích** mà không cần đánh giá chi tiết:

```
Nếu điểm tạm thời của MIN đã ≤ alpha (ngưỡng MAX)
→ Không cần xét các nước khác (chiều máy này)

Nếu điểm tạm thời của MAX đã ≥ beta (ngưỡng MIN)  
→ Không cần xét các nước khác (chiều máy này)
```

#### Thuật Toán

**Alpha-Beta với ngưỡng**:
```
minimax_alpha_beta(board, depth, alpha, beta, player):
  
  if depth = 0 or game_kết_thúc:
    return heuristic_value(board)
  
  if player = AI (tối đa hóa):
    maxVal = -∞
    for mỗi nước (r,c):
      board[r,c] = -1
      val = minimax_alpha_beta(board, depth-1, alpha, beta, đối_thủ)
      board[r,c] = 0
      maxVal = max(maxVal, val)
      alpha = max(alpha, val)
      
      if beta ≤ alpha:      # CẮT BETA ✂️
        break
    return maxVal
  
  else:  # người chơi (tối thiểu hóa)
    minVal = +∞
    for mỗi nước (r,c):
      board[r,c] = 1
      val = minimax_alpha_beta(board, depth-1, alpha, beta, AI)
      board[r,c] = 0
      minVal = min(minVal, val)
      beta = min(beta, val)
      
      if beta ≤ alpha:      # CẮT ALPHA ✂️
        break
    return minVal
```

**Gọi từ gốc**:
```
best_move = argmax{minimax_alpha_beta(board_sau_nước, depth-1, -∞, +∞)}
```

#### Ví Dụ Cắt Tỉa

```
Minimax bình thường:    Với alpha-beta:
Đánh giá 15 nút        Đánh giá 7 nút (cắt 50%)
```

Nếu nhánh phải của một MAX node đã có giá trị nhỏ hơn giá trị tốt nhất MAX node cha, thì không cần đánh giá các con của MIN node cha (vì MIN sẽ chọn giá trị nhỏ hơn đó dù sao).

#### Ưu điểm
✓ **Nhanh hơn Minimax**: Giảm 30-50% số nút đánh giá (thường 50% trong trường hợp tốt nhất)  
✓ **Vẫn tối ưu**: Kết quả giống Minimax nhưng nhanh hơn  
✓ **Độ sâu lớn hơn**: Có thể tìm 4-5 nước thay vì 3-4  
✓ **Không tổn thất**: Không hy sinh chất lượng nước đi  

#### Nhược điểm
✗ **Phức tạp hơn**: Logic cắt tỉa khó hiểu và debug  
✗ **Phụ thuộc thứ tự**: Nước được xét trước ảnh hưởng hiệu quả cắt  
✗ **Vẫn chậm**: Trên bàn cờ lớn, vẫn cần thuật toán nâng cao hơn  

#### Độ Phức Tạp
- **Thời gian tốt nhất**: O(b^(d/2)) - Tốc độ tăng gấp đôi!
- **Thời gian trường hợp trung bình**: O(b^(3d/4))
- **Thời gian tồi tệ nhất**: O(b^d) (nếu không cắt được)
- **Không gian**: O(b×d) giống Minimax
- **Nút đánh giá**: ~2,500 - 25,000 nút (giảm ~50% so với Minimax)

---

## 6. Bảng So Sánh Ba Chế Độ

| Tiêu Chí | Heuristic | Minimax | Alpha-Beta |
|----------|-----------|---------|-----------|
| **Tốc độ** | Rất nhanh O(n) | Chậm O(b^d) | Nhanh O(b^(d/2)) |
| **Chất lượng** | Trung bình | Tối ưu | Tối ưu |
| **Tìm kiếm sâu** | 0 nước | 3-4 nước | 4-5 nước |
| **Xử lý bẫy** | Kém | Tốt | Tốt |
| **Phối hợp tấn-phòng** | Cân bằng | Hoàn hảo | Hoàn hảo |
| **Độ phức tạp code** | Rất đơn | Trung bình | Phức tạp |
| **Nút đánh giá** | ~20 | ~20,000 | ~10,000 |
| **Thời gian/nước** | <10ms | >1s | 200-500ms |

---

## 7. Luồng Xử Lý Chính

```
Chương trình chính:
  1. Vẽ bàn cờ, hiển thị 3 nút chế độ (Heuristic, Minimax, Alpha-Beta)
  2. Người chơi click ô → Đặt quân người (X)
  3. Kiểm tra thắng/thua → Nếu có → Kết thúc
  4. Dựa trên chế độ đã chọn:
     - HEURISTIC:  get_heristic_moves(board)
     - MINIMAX:    get_minimax_moves(board, depth=3)
     - ALPHA_BETA: get_alpha_beta_moves(board, depth=4)
  5. Đặt quân AI (O)
  6. Kiểm tra thắng/thua → Quay lại bước 2
```

---

## 8. Cải Tiến & Phát Triển Trong Tương Lai

1. **Sắp xếp nước đi theo heuristic** trước khi tìm kiếm → Tăng hiệu quả cắt tỉa
2. **Transposition Table (TT)**: Lưu cache kết quả các bàn cờ đã tính → Tránh tính lại
3. **Iterative Deepening**: Tìm kiếm sâu dần → Tối ưu thời gian
4. **Killer Move**: Nước tốt ở nhánh khác → Ưu tiên kiểm tra
5. **Mở rộng bàn cờ**: Từ 10×10 lên 15×15 để phức tạp hơn
6. **Học máy (Neural Network)**: Huấn luyện để đánh giá nước đi chính xác hơn

---

## 9. Kết Luận

Ba chế độ AI cung cấp **mức độ khó chơi khác nhau**:
- **Heuristic**: Dễ (AI ngu), người chơi trung bình có thể thắng
- **Minimax**: Khó (AI mạnh), cần kỹ thuật cao để thắng
- **Alpha-Beta**: Cực khó (AI siêu mạnh + nhanh), cân bằng giữa sức mạnh và tốc độ

Dự án thành công trong việc triển khai **3 thuật toán AI khác nhau** với độ phức tạp tăng dần, từ tham lam đơn giản đến tìm kiếm tối ưu với cắt tỉa.
