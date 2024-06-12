import os
import logging
from datetime import datetime
import numpy
import pandas as pd
import streamlit as st

UPLOAD_FOLDER = 'uploads'

logging.basicConfig(filename='uploads.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(message)s')

st.set_page_config(page_title=f"Excel Validator")
st.header("Simple Excel Validator")

def store_file(f) -> None:
    """Stores an uploaded file in UPLOAD_FOLDER. Replace with apropriate database connection."""

    st.write(f)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base, ext = os.path.splitext(f.name)
    new_file_name = f"{base}_{current_time}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, new_file_name)

    with open(file_path, 'wb') as file:
        file.write(f.read())

    logging.info(f'Anonymous user uploaded {f.name}')

def read_xlsx(x_1) -> pd.DataFrame:
    """Reads and valiades xlsx file"""
    if x_1 is not None:
        store_file(x_1)

        try:
            df = pd.read_excel(x_1)
        except:
            st.error("⚠ Read error. Supported formats: .xlsx")
            return

        validate(df)
        return df

def validate(df) -> None:
    if df.shape[1] > 2:
        st.error("⚠ Too many columns. Supported columns: 2")
        return

    for col in range(df.shape[1]):
        if df.iloc[:, col].apply(lambda x: isinstance(x, str)).any():
            st.error(f"⚠ Type error in column {col}: Column must be numeric only.")
            return
    
    val = sum(df.iloc[:, 0])
    if val == 1:
        st.info("File is valid.")
    else:
        st.error(f"⚠ Value error in column {df.columns[0]}: Sum == {val} doesn't add up to 1.")

x_1 = st.file_uploader("Upload an Excel file to validate.")


if __name__ == "__main__":
    df = read_xlsx(x_1)
    with st.expander("About"):
        st.write("You will never be tracked using this software, but please note that any files you upload will be stored on our servers. Do not upload any personal information.")