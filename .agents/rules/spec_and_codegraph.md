---
trigger: always_on
description: "Quy tắc bắt buộc: Phải viết Spec trước khi viết Code (Spec-First) và dùng CodeGraph khi đọc code."
---

# MANDATORY WORKFLOW RULES: SPEC-FIRST & CODEGRAPH

## 1. QUY TẮC BẮT BUỘC: SPEC-FIRST (KHÔNG CÓ SPEC, CẤM VIẾT CODE)
Khi nhận bất kỳ yêu cầu lập trình nào (tính năng mới, sửa đổi hàm, tái cấu trúc logic):
1. **NGHIÊM CẤM VIẾT CODE TRỰC TIẾP:**
   - Agent **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** sinh mã nguồn hoặc chỉnh sửa file code trong `src/` khi chưa có file đặc tả tương ứng đã được duyệt.
   - Bất kỳ yêu cầu code nào cũng phải đi qua Cổng Đặc Tả (Specification Gate) trước.
2. **QUY TRÌNH 3 BƯỚC BẮT BUỘC TRƯỚC KHI CHẠM VÀO CODE:**
   - **Bước 1 (Đặc tả EARS):** Dùng `/speckit-specify` để soạn thảo `SPEC.md` với đầy đủ 8 thành phần cốt lõi và 5 mẫu câu EARS (*Ubiquitous, Event-driven, State-driven, Optional, Unwanted*), định nghĩa rõ "Out of Scope".
   - **Bước 2 (Lập kế hoạch kiến trúc & Rủi ro):** Dùng `/speckit-plan` để tạo `PLAN.md` và xác định ranh giới giữa các tầng.
   - **Bước 3 (Phân rã Task):** Dùng `/speckit-tasks` để tạo danh sách công việc nguyên tử trong `TASKS.md` (mỗi task $\le 4$h, có EARS ref và Done Criteria).
3. **CHỈ TRIỂN KHAI CODE KHI SPEC ĐƯỢC DUYỆT:**
   - Chỉ khi Spec và Tasks đã sẵn sàng, Agent mới được phép gọi `/speckit-implement` để viết code và unit test.
4. **NGUYÊN TẮC "FIX THE SPEC, NOT THE CODE":**
   - Khi test thất bại hoặc phát hiện bug: CẤM sửa code trực tiếp làm sai lệch đặc tả (Spec-Code Drift). Phải tìm nguyên nhân trong Spec, cập nhật lại Spec, sau đó mới sinh lại code.

## 2. QUY TẮC ĐỌC VÀ KHÁM PHÁ MÃ NGUỒN: BẮT BUỘC DÙNG CODEGRAPH
Khi cần đọc hiểu, tìm kiếm hoặc phân tích mã nguồn:
1. **First Choice:** Sử dụng MCP tool `codegraph_explore` hoặc CLI `codegraph explore "<query>"`.
2. **Truy vết chuyên sâu:**
   - Hàm gọi đến: `codegraph callers <symbol>`
   - Hàm được gọi bởi: `codegraph callees <symbol>`
   - Phân tích ảnh hưởng: `codegraph impact <symbol>`
   - Tìm test bị ảnh hưởng: `codegraph affected [files...]`
3. **CẤM:** Không được duyệt từng file bằng grep/find/read thủ công làm cạn kiệt context window khi đã có chỉ mục `.codegraph/`.
