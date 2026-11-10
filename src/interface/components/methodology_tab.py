"""Methodology Tab Component for Streamlit Dashboard.

Presents academic background, visual contagion flow pipeline, mathematical formula cards,
scenario benchmark objectives, and research limitations.

# Implements FR-10, FR-10-03, SRS §4.3, §11, §13
"""

import streamlit as st


def render_methodology_tab() -> None:
    """Render the Methodology & Theoretical Foundations Tab.

    # Implements FR-10, FR-10-03
    """
    st.markdown(
        """
        <div style="margin-bottom:1.25rem;">
            <div style="font-size:1.35rem; font-weight:700; color:#0F172A;">Cơ sở lý thuyết và phương pháp luận</div>
            <div style="font-size:0.88rem; color:#64748B; margin-top:0.2rem;">
                Khung mô hình hóa tác tử (Agent-Based Model) khảo sát rủi ro thanh lý chéo và trượt giá AMM trong DeFi Lending.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <div style="font-size:1.05rem; font-weight:700; color:#0F172A; margin-bottom:0.75rem;">
                1. Chu trình lây lan thanh lý chéo (Cascade Pipeline)
            </div>
            <div class="flow-container">
                <div class="flow-card">
                    <div class="flow-step">BƯỚC 01</div>
                    <div class="flow-title">Cú sốc giá ngoại sinh tại Block 1</div>
                    <div class="flow-desc">Giá ETH giảm 15% làm suy giảm giá trị tài sản thế chấp của toàn bộ người vay.</div>
                </div>
                <div class="flow-arrow">↓</div>
                <div class="flow-card">
                    <div class="flow-step">BƯỚC 02</div>
                    <div class="flow-title">Hệ số an toàn suy giảm (Health Factor &lt; 1.0)</div>
                    <div class="flow-desc">Các vị thế có tỷ lệ vay cao (LTV ban đầu 0.65 - 0.72) rơi vào ngưỡng vi phạm an toàn.</div>
                </div>
                <div class="flow-arrow">↓</div>
                <div class="flow-card">
                    <div class="flow-step">BƯỚC 03</div>
                    <div class="flow-title">Thanh lý một phần 50% & Thưởng 5%</div>
                    <div class="flow-desc">Liquidator trả 50% nợ thay người vay và tịch thu tài sản thế chấp với mức chiết khấu 5%.</div>
                </div>
                <div class="flow-arrow">↓</div>
                <div class="flow-card">
                    <div class="flow-step">BƯỚC 04</div>
                    <div class="flow-title">Bán tháo Collateral vào 2 Pool AMM</div>
                    <div class="flow-desc">
                        • <strong>Thế chấp ETH:</strong> Bán thẳng vào Pool A (ETH/USDC) lấy USDC.<br>
                        • <strong>Thế chấp stETH:</strong> Xả vào Pool B (stETH/ETH) lấy ETH, rồi bán tiếp ETH vào Pool A.
                    </div>
                </div>
                <div class="flow-arrow">↓</div>
                <div class="flow-card">
                    <div class="flow-step">BƯỚC 05</div>
                    <div class="flow-title">Trượt giá AMM (Constant Product x·y = k)</div>
                    <div class="flow-desc">Lực bán lớn rút cạn dự trữ USDC ở Pool A và ETH ở Pool B, làm stETH mất peg sâu.</div>
                </div>
                <div class="flow-arrow">↓</div>
                <div class="flow-card flow-card-highlight">
                    <div class="flow-step" style="color:#DC2626;">BƯỚC 06</div>
                    <div class="flow-title" style="color:#991B1B;">Lây lan sang các khối tiếp theo (Domino Effect)</div>
                    <div class="flow-desc">Mức giá mới tiếp tục đẩy các vị thế an toàn trước đó vào vòng xoáy thanh lý mới.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="font-size:1.05rem; font-weight:700; color:#0F172A; margin-bottom:0.75rem;">
                2. Các công thức toán học cốt lõi
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="formula-card">
                <div class="formula-badge">HỆ SỐ AN TOÀN VỊ THẾ</div>
                <div class="formula-title">Health Factor (HF)</div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}")
        st.markdown(
            """
                <div class="formula-desc">
                    Ngưỡng thanh lý quy định <code>LT = 0.80</code> (80%). Vị thế rơi vào diện thanh lý khi <code>HF &lt; 1.0</code>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="formula-card">
                <div class="formula-badge">MÔ HÌNH TẠO LẬP THỊ TRƯỜNG AMM</div>
                <div class="formula-title">Constant-Product Zero-Fee Swap</div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"x \cdot y = k \implies y_{out} = \frac{y \cdot \Delta x}{x + \Delta x}")
        st.markdown(
            """
                <div class="formula-desc">
                    Bảo toàn tích số <code>k</code>. Giá giao ngay <code>P = y / x</code> biến động tự nhiên theo tỷ lệ dự trữ sau swap.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="formula-card">
                <div class="formula-badge">ĐO LƯỜNG MỨC ĐỘ MẤT PEG</div>
                <div class="formula-title">Tỷ lệ chiết khấu stETH (Discount %)</div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\text{Discount}(\%) = \frac{P_{ETH} - P_{stETH}}{P_{ETH}} \times 100\%")
        st.markdown(
            """
                <div class="formula-desc">
                    Đo lường độ lệch giá giữa stETH và ETH do áp lực bán tháo dồn vào Pool B (stETH/ETH).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border:0; border-top:1px solid #E2E8F0; margin:1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:1.05rem; font-weight:700; color:#0F172A; margin-bottom:0.75rem;">
            3. Phân loại mục đích của 3 kịch bản đối chứng
        </div>
        <div class="scenario-grid">
            <div class="scenario-box box-sc01">
                <div class="scenario-tag tag-sc01">SC01: BASELINE</div>
                <div class="scenario-name">Môi trường đối chứng tĩnh</div>
                <div class="scenario-body">Giá ETH giữ nguyên $3,000. Không có biến động giá, xác nhận 0 thanh lý và 0 nợ xấu.</div>
            </div>
            <div class="scenario-box box-sc02">
                <div class="scenario-tag tag-sc02">SC02: DIRECT SHOCK</div>
                <div class="scenario-name">Cú sốc ngoại sinh ban đầu</div>
                <div class="scenario-body">Giá ETH giảm 15% tại Block 1 nhưng không bán vào AMM để cô lập số vị thế vỡ nợ ban đầu (17 người).</div>
            </div>
            <div class="scenario-box box-sc03">
                <div class="scenario-tag tag-sc03">SC03: CASCADE CONTAGION</div>
                <div class="scenario-name">Lây lan thanh lý chéo</div>
                <div class="scenario-body">Bán toàn bộ collateral vào 2 Pool AMM, kích hoạt vòng xoáy trượt giá, depeg stETH và nợ xấu lan rộng.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border:0; border-top:1px solid #E2E8F0; margin:1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:1.05rem; font-weight:700; color:#0F172A; margin-bottom:0.6rem;">
            4. Giả định và giới hạn nghiên cứu (SRS §13)
        </div>
        <div class="limitations-container">
            <ol style="margin:0; padding-left:1.2rem; color:#475569; font-size:0.86rem; line-height:1.65;">
                <li><strong>Mô hình AMM cơ bản (CPMM):</strong> Giả lập Constant-Product x · y = k không phí giao dịch để cách ly độ trượt giá cơ bản; chưa xét đến mô hình thanh khoản tập trung (Concentrated Liquidity như Uniswap v3).</li>
                <li><strong>Không xét Arbitrageur:</strong> Giả định không có tác tử kinh doanh chênh lệch giá bơm vốn cân bằng hai pool; phản ánh trạng thái thị trường chịu căng thẳng thanh khoản cao.</li>
                <li><strong>Thanh lý tức thời trong khối:</strong> Người thanh lý hấp thụ và bán tháo toàn bộ tài sản thế chấp ngay trong khối mà không có độ trễ huy động vốn.</li>
                <li><strong>Chi phí Gas bằng 0:</strong> Không xét phí giao dịch mạng lưới để tập trung vào động lực kinh tế học của việc thanh lý.</li>
                <li><strong>Lãi suất vay cố định:</strong> Chưa mô phỏng biến động lãi suất vay theo tỷ lệ sử dụng vốn (Utilization Rate) trong pool cho vay.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
