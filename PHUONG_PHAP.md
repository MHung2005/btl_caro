# PHƯƠNG PHÁP TRIỂN KHAI AI

## 1. Mô Hình Hóa Bàn Cờ

Bàn cờ: **ma trận 2D (10×10)** với giá trị:
- 0: ô trống | 1: quân người (X) | -1: quân AI (O)

---

## 2. Ràng Buộc (Điều Kiện Kết Thúc)

Trò chơi kết thúc khi:
- **Thắng/Thua**: Có 5 quân liên tiếp (ngang, dọc, chéo)
- **Hoà**: Bàn cờ đầy mà không có người thắng

---

## 3. Hàm Đánh Giá Trạng Thái

Tính điểm cho mỗi "cửa sổ" 5 ô liên tiếp dựa trên mô hình:
- AI có 5 quân: +100000 (thắng)
- AI có 4 quân + 1 ô trống: +1000 (sắp thắng)
- Người chơi có 4 quân + 1 ô trống: -1000 (cần chặn)
- Quét cả 4 hướng (ngang, dọc, chéo) → tổng điểm trạng thái

---

## 4. Nước Đi Tiềm Năng

Chỉ xét những ô **lân cận với quân đã đặt** (khoảng cách ≤ 1): giảm từ ~100 xuống ~10-20 ô.

---

## 5. Ba Chế Độ AI

## 5. Ba Chế Độ AI

### 5.1 Chế Độ Heuristic (Tham Lam - Greedy)

**Ý tưởng**: Chọn nước **tốt nhất hiện tại** dựa trên heuristic, không tìm kiếm sâu:

```
best_move = argmax{điểm_tấn_công - điểm_phòng_thủ}
```

**Thuật toán**: 
- Với mỗi nước tiềm năng: tính điểm nếu AI đặt + điểm nếu người chơi đặt
- Chọn nước có điểm tổng cao nhất

**Ưu điểm** | **Nhược điểm**
---|---
Cực nhanh O(n) | Không tối ưu, dễ mắc bẫy
Phản ứng lập tức | Không dự đoán nước đối thủ
Chặn/tấn công cơ bản | Dễ bị đánh bại

---

### 5.2 Chế Độ Minimax (Tìm Kiếm Min-Max)

**Ý tưởng**: Tìm kiếm **cây trò chơi đến độ sâu cố định**, chọn nước **tốt nhất toàn cục**:

```
Minimax(board, depth) = 
  - Nếu depth=0 hoặc game_kết_thúc → trả về điểm heuristic
  - Nếu lượt AI (max) → trả về max{Minimax(child, depth-1)}
  - Nếu lượt người (min) → trả về min{Minimax(child, depth-1)}
```

**Thuật toán**:
1. Gọi `Minimax(board, depth)` cho tất cả nước tiềm năng từ gốc
2. Chọn nước có giá trị cao nhất

**Ưu điểm** | **Nhược điểm**
---|---
Tối ưu, nhìn trước 2-3 nước | Chậm O(b^d) - độ phức tạp mũ
Vừa tấn công vừa phòng thủ | Giới hạn độ sâu trên bàn cờ lớn

---

### 5.3 Chế Độ Alpha-Beta (Minimax + Cắt Tỉa)

**Ý tưởng**: Cải tiến Minimax bằng **cắt bỏ nhánh vô ích** mà không ảnh hưởng kết quả:

```
Nếu MAX node đã tìm thấy giá trị tốt ≥ giá trị cực đại của MIN cha
  → Không cần xét các nước con khác (CẮT BETA)

Nếu MIN node đã tìm thấy giá trị tệ ≤ giá trị cực tiểu của MAX cha
  → Không cần xét các nước con khác (CẮT ALPHA)
```

**Thuật toán**:
```
alpha_beta(board, depth, alpha, beta, player):
  if depth=0 or game_kết_thúc:
    return heuristic_value(board)
  
  if player = AI (max):
    for mỗi nước (r,c):
      giá_trị = alpha_beta(board_sau_nước, depth-1, alpha, beta, người)
      alpha = max(alpha, giá_trị)
      if beta ≤ alpha: break (CẮT)
    return alpha
  else:  # người (min)
    for mỗi nước (r,c):
      giá_trị = alpha_beta(board_sau_nước, depth-1, alpha, beta, AI)
      beta = min(beta, giá_trị)
      if beta ≤ alpha: break (CẮT)
    return beta
```

**Ưu điểm** | **Nhược điểm**
---|---
Nhanh hơn Minimax 50% | Logic cắt tỉa phức tạp hơn
Kết quả vẫn tối ưu | Phụ thuộc thứ tự nước đi xét

---

## 6. So Sánh Ba Chế Độ

| Tiêu Chí | Heuristic | Minimax | Alpha-Beta |
|----------|-----------|---------|-----------|
| **Tốc độ** | O(n) - rất nhanh | O(b^d) - chậm | O(b^(d/2)) - nhanh |
| **Chất lượng** | Trung bình | Tối ưu | Tối ưu |
| **Tìm kiếm sâu** | 0 nước | 3-4 nước | 4-5 nước |
| **Thời gian/nước** | <10ms | >1s | 200-500ms |
| **Độ khó** | Dễ | Khó | Cực khó |

---

## 7. Luồng Xử Lý Chính

```
1. Hiển thị bàn cờ & 3 nút chế độ (Heuristic, Minimax, Alpha-Beta)
2. Người chơi click ô → Đặt quân X
3. Kiểm tra thắng/thua → Nếu có → Kết thúc
4. AI tính nước đi:
   - Heuristic: Lựa chọn nước tốt nhất hiện tại
   - Minimax: Tìm kiếm depth=3
   - Alpha-Beta: Tìm kiếm depth=4 (nhanh hơn)
5. AI đặt quân O
6. Kiểm tra thắng/thua → Quay lại bước 2
```

---

## 8. Kết Luận

Ba chế độ AI cung cấp **mức độ khó chơi khác nhau**:
- **Heuristic**: Dễ - AI tham lam, không nhìn trước
- **Minimax**: Khó - AI nhìn trước 3-4 nước, tối ưu
- **Alpha-Beta**: Cực khó - AI nhìn trước 4-5 nước, tối ưu + nhanh

Dự án thành công triển khai **3 thuật toán AI** với độ phức tạp tăng dần từ tham lam đơn giản đến tìm kiếm tối ưu với cắt tỉa.

