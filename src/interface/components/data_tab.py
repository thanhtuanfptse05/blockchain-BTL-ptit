"""Data Tab Component for Streamlit Dashboard.

Displays interactive DataFrames for Block Results (12 columns) and Liquidation Events (10 columns),
and provides CSV download buttons.

# Implements FR-09, FR-09-01..FR-09-07, SRS §7.3, §7.4, §11, §15.1
"""

from typing import Dict, Optional
import streamlit as st
from src.domain.simulation_result import SimulationResult
from src.infra.exporter import (
    block_results_to_dataframe,
    liquidation_events_to_dataframe,
    export_block_results_to_csv,
    export_liquidation_events_to_csv,
)


def render_data_tab(results: Optional[Dict[str, SimulationResult]]) -> None:
    """Render the Data Tab in Streamlit with interactive tables and download buttons.

    # Implements FR-09, FR-09-06, FR-09-07

    Args:
        results: Dictionary mapping scenario IDs to SimulationResult objects,
                 or None if simulation has not run yet.
    """
    if not results:
        st.info("Chưa có dữ liệu. Vui lòng bấm 'Chạy mô phỏng' ở thanh bên để bắt đầu.")
        return

    st.markdown("### Dữ liệu chi tiết từng khối (Block Results)")
    st.caption("12 trường dữ liệu chuẩn theo từng khối của 3 kịch bản SC01, SC02, SC03.")

    df_blocks = block_results_to_dataframe(results)
    st.dataframe(df_blocks, width="stretch", height=320)

    csv_blocks = export_block_results_to_csv(results)
    st.download_button(
        label="Tải tệp CSV Block Results",
        data=csv_blocks,
        file_name="block_results.csv",
        mime="text/csv",
        key="btn_download_block_results",
    )

    st.markdown("---")

    st.markdown("### Danh sách sự kiện thanh lý (Liquidation Events)")
    st.caption("Toàn bộ các sự kiện thanh lý vị thế nợ được kích hoạt và thực thi qua từng khối.")

    df_events = liquidation_events_to_dataframe(results)
    if len(df_events) == 0:
        st.info("Không có sự kiện thanh lý nào được ghi nhận.")
    else:
        st.dataframe(df_events, width="stretch", height=280)

    csv_events = export_liquidation_events_to_csv(results)
    st.download_button(
        label="Tải tệp CSV Liquidation Events",
        data=csv_events,
        file_name="liquidation_events.csv",
        mime="text/csv",
        key="btn_download_liquidation_events",
    )
