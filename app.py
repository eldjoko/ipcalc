import streamlit as st
import ipaddress as ip
from validators import validate_ip_address
from functions import get_all_subnet_masks, get_subnet_info, generate_all_subnets
import pandas as pd
from st_mui_table import st_mui_table
from st_copy_to_clipboard import st_copy_to_clipboard
# set page config


st.set_page_config(
    page_title="IP Calculator | Home",
    page_icon=":material/hub:",
    layout="wide",
)
with st.sidebar:
    st.write("logo")
# page start
st.title('IP Calculator')

subnet_col, mask_col = st.columns([2,2])

ip_address = subnet_col.text_input('IP Address', placeholder='1.1.1.1')

subnet_mask = mask_col.selectbox('Subnet Mask', get_all_subnet_masks())

if st.button('Submit'):
    try:
        validate_ip_address(ip_address)
        # calculation take place here
        cidr = str((ip.IPv4Network(f'0.0.0.0/{subnet_mask}', strict=False).netmask))
        ip_info = get_subnet_info(f'{ip_address}/{cidr}')
        ip_info_df = pd.melt(pd.DataFrame(ip_info))
        modified_df = ip_info_df.copy()
        modified_df['value'] = modified_df['value'].apply(lambda bold: f"<b>{bold}</b>")
        col_1, col_2 = st.columns([1,2])
        with col_1:
            st_mui_table(
                modified_df,
                showHeaders=False,
                enablePagination=True
                )
        with col_2:
            all_subnets = generate_all_subnets(ip_address, subnet_mask)
            # all_subnets_df = pd.DataFrame(all_subnets)
            # st_mui_table(all_subnets_df)
            st.write(all_subnets)
    except AssertionError as e:
        st.error(f'Validation Error: {e}')
