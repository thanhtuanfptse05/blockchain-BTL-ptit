"""Methodology Tab Component for Streamlit Dashboard.

Presents academic background, contagion loop diagrams, mathematical formulas (KaTeX),
scenario objectives, and model assumptions/limitations.

# Implements FR-10, FR-10-03, SRS §4.3, §11, §13
"""

import streamlit as st


def render_methodology_tab() -> None:
    """Render the Methodology & Academic Foundations Tab.

    # Implements FR-10, FR-10-03
    """
    st.markdown("## Cơ sở lý thuyết và phương pháp luận")
    st.caption("Khung mô hình hóa tác tử (Agent-Based Model) khảo sát rủi ro thanh lý chéo và trượt giá AMM.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 1. Cơ chế lây lan thanh lý chéo")
        st.markdown(
            """
            ```text
            [ 1. Cú sốc ngoại sinh tại Block 1 ]
                           ↓
            [ 2. Giá ETH giảm ] ────────────→ Làm giảm giá trị tài sản thế chấp
                           ↓
            [ 3. Health Factor < 1.0 ] ────→ Kích hoạt điều kiện thanh lý vị thế
                           ↓
            [ 4. Thanh lý từng phần 50% ] ──→ Thu hồi nợ, thu giữ tài sản kèm thưởng 5%
                           ↓
            [ 5. Bán tài sản vào AMM ]
                 ├── ETH   → Bán vào Pool A (ETH/USDC)
                 └── stETH → Bán vào Pool B (stETH/ETH) → Bán tiếp ETH vào Pool A
                           ↓
            [ 6. Trượt giá AMM x*y=k ] ────→ Giá ETH giảm thêm và stETH mất giá so với ETH
                           ↓
            [ 7. Chuyển sang khối kế tiếp ] ─→ Kích hoạt thêm các đợt thanh lý mới
            ```
            """
        )

    with col2:
        st.markdown("### 2. Các công thức toán học")

        st.markdown("**Hệ số an toàn vị thế (Health Factor - HF):**")
        st.latex(r"HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}")
        st.caption("Ngưỡng thanh lý $LT_{ETH} = LT_{stETH} = 0.80$. Vị thế đủ điều kiện thanh lý khi $HF < 1.0$.")

        st.markdown("**Mô hình AMM tích số không đổi (Zero-Fee Constant Product):**")
        st.latex(r"x \cdot y = k \implies y_{out} = \frac{y \cdot \Delta x}{x + \Delta x}")
        st.caption("Bảo toàn tích số $k$, giá giao ngay $P = y / x$ biến động theo tỷ lệ dự trữ sau swap.")

        st.markdown("**Tỷ lệ chiết khấu stETH so với ETH:**")
        st.latex(r"\text{Discount}(\%) = \frac{P_{ETH} - P_{stETH}}{P_{ETH}} \times 100\%")
        st.caption("Đo lường mức độ mất cân bằng tỷ giá giữa stETH và ETH do áp lực bán tại Pool B.")

    st.markdown("---")

    st.markdown("### 3. Phân loại mục đích của 3 kịch bản")
    st.markdown(
        """
        | Kịch bản | Tên gọi | Cơ chế giá | Mục đích kiểm chứng |
        | :--- | :--- | :--- | :--- |
        | **SC01** | Baseline | Giá ổn định ($3,000) | Môi trường đối chứng tĩnh: 0 thanh lý, 0 nợ xấu. |
        | **SC02** | Direct Shock | Giảm một lần tại block 1, không bán vào AMM | Đo lường số lượng thanh lý gây ra thuần túy bởi cú sốc ban đầu. |
        | **SC03** | Cascade Contagion | Giảm tại block 1 và bán tài sản thế chấp vào AMM | Khảo sát tác động cộng dồn của cơ chế trượt giá AMM lên chuỗi thanh lý. |
        """
    )

    st.markdown("---")

    st.markdown("### 4. Giả định và giới hạn nghiên cứu (SRS §13)")
    st.markdown(
        r"""
        1. **Mô hình AMM cơ bản**: Áp dụng mô hình Constant-Product $x \cdot y = k$ không phí giao dịch để cách ly tác động của trượt giá cơ bản; chưa xét đến mô hình thanh khoản tập trung (Concentrated Liquidity).
        2. **Không xét Arbitrageur**: Giả định không có tác tử kinh doanh chênh lệch giá bơm vốn cân bằng hai pool; phản ánh điều kiện thị trường chịu căng thẳng thanh khoản cao.
        3. **Thanh lý tức thời trong khối**: Người thanh lý hấp thụ và bán toàn bộ tài sản thế chấp ngay trong khối mà không có độ trễ huy động vốn.
        4. **Chi phí Gas bằng 0**: Không xét phí mạng lưới để tập trung vào động lực kinh tế học của việc thanh lý.
        5. **Lãi suất vay cố định**: Chưa mô phỏng biến động lãi suất vay theo tỷ lệ sử dụng vốn trong pool cho vay.
        """
    )
