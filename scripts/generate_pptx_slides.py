"""Script to generate a professional 16:9 PowerPoint (.pptx) presentation for the project defense.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(15, 23, 42)      # #0F172A
    C_BLUE = RGBColor(37, 99, 235)     # #2563EB
    C_SLATE = RGBColor(71, 85, 105)    # #475569
    C_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    C_GREEN = RGBColor(5, 150, 105)    # #059669
    C_AMBER = RGBColor(217, 119, 6)    # #D97706
    C_RED = RGBColor(220, 38, 38)      # #DC2626

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, tag: str, title: str):
        # Header Badge
        badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8), Inches(0.4))
        p0 = badge.text_frame.paragraphs[0]
        p0.text = tag.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE

        # Title
        tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        p1 = tbox.text_frame.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

    # SLIDE 1: Title Slide
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = C_BORDER

    tb1 = s1.shapes.add_textbox(Inches(2.0), Inches(1.6), Inches(9.333), Inches(4.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "BÁO CÁO BÀI TẬP LỚN MÔN CÔNG NGHỆ CHUỖI KHỐI — PTIT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    p = tf1.add_paragraph()
    p.text = "DeFi Liquidation Cascade Simulator"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Mô phỏng Động học Lây lan Rủi ro Thanh lý Chéo Tài sản và Trượt giá AMM bằng Agent-Based Model"
    p.font.size = Pt(14)
    p.font.color.rgb = C_SLATE
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "• Thành viên 1: Core Simulator Lead (Kiến trúc Nghiệp vụ & Mô hình Toán học)"
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY

    p = tf1.add_paragraph()
    p.text = "• Thành viên 2: UI & Data Viz Lead (Giao diện Streamlit & Trực quan hóa Dữ liệu)"
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY

    s1.notes_slide.notes_text_frame.text = "Kính chào Thầy/Cô. Hôm nay nhóm em xin trình bày đề tài Mô phỏng lây lan rủi ro thanh lý chéo trong DeFi Lending."

    # SLIDE 2: Problem Statement
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Đặt vấn đề & Động lực thực tiễn", "Vòng xoáy sụp đổ thanh lý (Liquidation Feedback Loop) trong DeFi")
    
    col_w = Inches(3.6)
    left_start = Inches(0.8)
    gap = Inches(0.35)

    boxes = [
        ("1. Thanh lý vị thế nợ", "Khi giá tài sản thế chấp sụt giảm mạnh, Health Factor < 1.0. Liquidator thanh toán nợ thay cho người vay để nhận tài sản thế chấp với mức thưởng 5%."),
        ("2. Xả tài sản lên AMM", "Liquidator lập tức bán tháo lượng collateral vừa tịch thu lên các sàn AMM (Pool A & Pool B) để chốt lời sang đồng tiền định giá (USDC)."),
        ("3. Trượt giá & Lây lan chéo", "Lực bán lớn tạo trượt giá nghiêm trọng theo x*y=k. Giá tiếp tục giảm sâu, kéo stETH mất peg và kích hoạt các đợt thanh lý domino tiếp theo.")
    ]

    for idx, (head, desc) in enumerate(boxes):
        x = left_start + idx * (col_w + gap)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), col_w, Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER
        
        tb = s2.shapes.add_textbox(x + Inches(0.2), Inches(2.3), col_w - Inches(0.4), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(12)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = C_SLATE

    # SLIDE 3: Architecture & SDD
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Phương pháp luận & Kiến trúc phần mềm", "Clean Architecture & Spec-Driven Development (SDD)")
    
    # Left Card: SDD
    c_left = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = C_WHITE
    c_left.line.color.rgb = C_BORDER
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Spec-Driven Development (10 Đặc tả EARS)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    items_sdd = [
        "001: Simulation Config & 10 Ràng buộc C-01..C-10",
        "002: Khởi tạo 100 Tác tử tất định theo Seed",
        "003: Định giá Health Factor & Tiêu chí Thanh lý",
        "004: Partial Liquidation Engine (Close factor 50%)",
        "005: 2 Pool AMM Constant-Product (Phí zero-fee)",
        "006: Điều phối vòng lặp mô phỏng 3 kịch bản",
        "007: Trích xuất KPI & Bảng so sánh Delta",
        "008: 4 Biểu đồ Plotly phân tích động thái",
        "009: Xuất bảng dữ liệu và 2 file CSV chuẩn",
        "010: Giao diện Streamlit Dashboard & Tab Cơ chế"
    ]
    for it in items_sdd:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    # Right Card: Clean Architecture
    c_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = C_WHITE
    c_right.line.color.rgb = C_BORDER
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Phân tầng Clean Architecture & Nguyên tắc Bất biến"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    items_ca = [
        "domain/: Thực thể bất biến (BorrowerAgent, AMMPool, LiquidationEvent, BlockResult, SimulationResult).",
        "usecase/: Động cơ tính toán độc lập hoàn toàn với UI (agent_generator, health_factor, liquidation, amm).",
        "infra/: Module xuất CSV và ghi nhận dữ liệu.",
        "interface/: Streamlit UI một trang chuẩn Light Mode.",
        "Nguyên tắc 1: 100% kết quả tính từ code, không hardcode.",
        "Nguyên tắc 2: Bảo toàn toán học AMM x*y=k qua mọi swap.",
        "Nguyên tắc 3: Tất định 100% nhờ hạt giống seed=42."
    ]
    for it in items_ca:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    # SLIDE 4: Mathematical Foundations
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Cơ sở lý thuyết & Mô hình toán học", "Các công thức nền tảng trong hệ thống mô phỏng")
    
    math_cards = [
        ("1. Health Factor (HF)", "HF = Σ(Collateral_i × Price_i × LT_i) / Debt\n• LT(ETH) = LT(stETH) = 0.80 (80%).\n• Vị thế đủ điều kiện thanh lý khi và chỉ khi HF < 1.0.\n• Ban đầu toàn bộ 100 tác tử có HF > 1.0 (an toàn tuyệt đối)."),
        ("2. Thanh lý một phần (Partial Liquidation)", "Close Factor = 50% | Penalty Bonus = 5%\n• Nợ trả: DebtRepaid = Debt × 50%.\n• Tài sản tịch thu: Seized = (DebtRepaid × 1.05) / Price.\n• Nếu thiếu collateral -> Ghi nhận Nợ xấu (Bad Debt)."),
        ("3. AMM Constant-Product (Zero-Fee)", "x · y = k => y_out = (y · Δx) / (x + Δx)\n• Giá giao ngay mới: P' = y' / x'.\n• Không thu phí giao dịch để cách ly thuần túy độ trượt giá cơ bản (Price Slippage)."),
        ("4. Chiết khấu stETH (Discount / Depeg)", "Discount(%) = (P_ETH - P_stETH) / P_ETH × 100%\n• Đo lường mức độ mất cân bằng tỷ giá giữa stETH và ETH do áp lực bán tháo vào Pool B.")
    ]

    for idx, (title, content) in enumerate(math_cards):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * Inches(5.9)
        y = Inches(1.9) + row * Inches(2.6)
        
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER
        
        tb = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.2), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_BLUE
        p.space_after = Pt(4)
        
        for line in content.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = C_SLATE

    # SLIDE 5: Benchmark Results Table
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Kết quả thực nghiệm định lượng", "Bảng so sánh đối chứng 3 kịch bản mô phỏng")
    
    rows = 7
    cols = 6
    tbl_shape = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.9), Inches(11.7), Inches(4.8))
    table = tbl_shape.table

    table_data = [
        ["Chỉ số Khảo sát", "SC01 Baseline", "SC02 Direct Shock", "SC03 Cascade", "Chênh lệch (SC03 - SC02)", "Tỷ lệ Tăng tương đối"],
        ["Giá ETH cuối cùng ($)", "$3,000.00", "$2,550.00 (-15.0%)", "$988.92", "-$1,561.08", "-61.22% (Lao dốc sâu)"],
        ["Giá stETH cuối cùng ($)", "$2,970.00", "$2,524.50 (-15.0%)", "$318.72", "-$2,205.78", "-87.37% (Sụp đổ)"],
        ["Chiết khấu stETH (%)", "1.00%", "1.00%", "67.77%", "+66.77%", "+66.77% (Mất peg nặng)"],
        ["Số Agent bị thanh lý", "0 / 100 (0%)", "17 / 100 (17%)", "100 / 100 (100%)", "+83 agents", "+488.24% (Toàn bộ)"],
        ["Tổng số lượt thanh lý", "0 lượt", "17 lượt", "214 lượt", "+197 lượt", "+1,158.82%"],
        ["Nợ xấu Giao thức ($)", "$0.00", "$0.00", "$14,265,389.56", "+$14.27M", "Bùng nổ nợ xấu"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
            else:
                p.font.color.rgb = C_NAVY
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else C_LIGHT
                if c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = C_RED

    # SLIDE 6: UI & Dashboard Demo
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Giao diện người dùng & Trực quan hóa dữ liệu", "Streamlit Dashboard — Humanized Light Theme")

    c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Đặc điểm Thiết kế Giao diện (Humanized)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    ui_feats = [
        "Light Mode tối giản: Nền trắng sạch, viền xám mảnh, độ tương phản cao, phong cách Stripe / Dune Light.",
        "Loại bỏ triệt để AI Emojis phèn: Dùng nhãn kỹ thuật gãy gọn, văn phong học thuật trung tính chuẩn Humanizer.",
        "Nạp sẵn dữ liệu tức thời: Tự động chạy trong 0.007 giây khi mở trang, không để màn hình trống.",
        "Hệ thống 6 thẻ KPI tài chính: Phông số JetBrains Mono, badge phần trăm chênh lệch so sánh trực tiếp SC03 vs SC02.",
        "Kịch bản mẫu 1-click: Nút Căng thẳng cao (Shock 30%) và Thanh khoản sâu (Pool dày $300M)."
    ]
    for it in ui_feats:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Cấu trúc 4 Tabs Chuyên biệt"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    tabs_feats = [
        "Tab 1: Biến động giá và chiết khấu: Biểu đồ đường giá ETH (vạch shock Block 1) và biểu đồ tỷ lệ depeg stETH.",
        "Tab 2: Diễn biến thanh lý: Biểu đồ cột chồng phân bổ ETH/stETH, đường lũy kế người vay vỡ nợ và Bảng đối chứng chỉ số.",
        "Tab 3: Bảng dữ liệu chi tiết & Xuất CSV: Data Grid 12 cột Block Results và 10 cột Liquidation Events, hỗ trợ tải file CSV.",
        "Tab 4: Cơ sở phương pháp luận: Sơ đồ chu trình cascade dạng hộp, công thức toán học KaTeX và 5 giả định giới hạn."
    ]
    for it in tabs_feats:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    # SLIDE 7: Testing & CI/CD
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Kiểm thử & Đảm bảo chất lượng", "73/73 Tests Pass Rate (100%) & GitHub CI/CD Pipeline")

    c1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Hệ thống Kiểm thử Pytest Toàn diện"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    test_feats = [
        "73 bài kiểm thử tự động, 100% Pass trong 2.15 giây.",
        "test_config: 21 test kiểm chứng 10 ràng buộc C-01..C-10.",
        "test_agent_generator: 5 test kiểm tra tính tất định seed.",
        "test_health_factor: 5 test đối chiếu tính tay và ranh giới HF=1.0.",
        "test_amm_engine: 6 test bảo toàn tích số k và trượt giá.",
        "test_liquidation_engine: 5 test close factor và nợ xấu.",
        "test_scenario_runner: 5 test độc lập 3 kịch bản.",
        "test_system_scenarios: 7 test bất biến thực nghiệm ST-01..ST-07."
    ]
    for it in test_feats:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    c2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Tự động hóa & Xuất bản Đa nền tảng"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    cicd_feats = [
        "GitHub Actions CI: Tự động chạy Pytest trên Python 3.10, 3.11, 3.12 khi push code.",
        "GitHub Pages WebAssembly (stlite): Xuất bản web không cần server tại thanhtuanfptse05.github.io/blockchain-BTL-ptit/.",
        "Streamlit Cloud Ready: Sẵn sàng triển khai 1-click.",
        "Quy chuẩn dòng code: 100% file code <= 249 dòng (dưới trần 300 dòng theo Definition of Done).",
        "Mã nguồn mở giấy phép MIT đầy đủ trên GitHub."
    ]
    for it in cicd_feats:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

    # SLIDE 8: Conclusion
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Tổng kết & Hướng phát triển", "Đóng góp khoa học và Khả năng ứng dụng thực tiễn")

    c1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tb = s8.shapes.add_textbox(Inches(1.8), Inches(2.0), Inches(9.7), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "1. Kết luận Đề tài"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Đề tài đã mô hình hóa và chứng minh thành công bằng thực nghiệm: Cơ chế thanh lý bán tháo vào AMM có thể khuếch đại rủi ro gấp 5 lần (+488% số vị thế vỡ nợ) và gây ra hiện tượng mất peg nghiêm trọng của stETH."
    p.font.size = Pt(12)
    p.font.color.rgb = C_SLATE

    p = tf.add_paragraph()
    p.text = "2. Hướng phát triển Mở rộng"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_before = Pt(12)
    p.space_after = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Bổ sung tác tử Arbitrageur để tìm kiếm ngưỡng thanh khoản tối thiểu có thể phục hồi lại peg của stETH.\n• Mô phỏng lãi suất vay biến đổi (Dynamic Borrow Rate) theo tỷ lệ sử dụng vốn (Utilization Rate).\n• Mở rộng sang mô hình thanh khoản tập trung Uniswap v3."
    p.font.size = Pt(12)
    p.font.color.rgb = C_SLATE

    p = tf.add_paragraph()
    p.text = "Cảm ơn Thầy/Cô và Hội đồng đã lắng nghe. Nhóm xin sẵn sàng trả lời các câu hỏi phản biện!"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_before = Pt(18)

    out_path = Path("docs/Slide_Thuyet_Trinh_DeFi_Liquidation_Cascade.pptx")
    prs.save(out_path)
    print(f"Presentation saved successfully to {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_deck()

