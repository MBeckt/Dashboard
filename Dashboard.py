from pathlib import Path

import streamlit as st

dir_path = Path(__file__).parent


# Note that this needs to be in a method so we can have an e2e playwright test.
def run() -> None:
    page = st.navigation(
        {
            "Pages": [
                st.Page(
                    dir_path / "hello.py", title="Dashboard", icon=":material/waving_hand:"
                ),
                st.Page(
                    dir_path / "P2SMS.py",
                    title="Power2SMS",
                    icon=":material/table:",
                ),
                st.Page(
                    dir_path / "metrics.py",
                    title="Server Metrics",
                    icon=":material/show_chart:",
                ),
            ]
        }
    )
    page.run()


if __name__ == "__main__":
    run()
