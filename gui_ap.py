import streamlit as st
from PIL import Image
import numpy as np
import io

def compress_color_image(img_array, k):
    compressed_img = np.zeros_like(img_array)
    for channel in range(3):
        U, S, V = np.linalg.svd(img_array[:, :, channel], full_matrices=False)
        S = np.diag(S)
        compressed_img[:, :, channel] = np.dot(U[:, :k], np.dot(S[:k, :k], V[:k, :]))
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)
    return compressed_img

st.title("Color Image Compression")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_array = np.array(img)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    k = st.number_input("Enter k (number of singular values to retain):", min_value=1, value=10)
    if st.button("Compress Image"):
        compressed_img = compress_color_image(img_array, k)
        compressed_img_pil = Image.fromarray(compressed_img)
        
        buf = io.BytesIO()
        compressed_img_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(compressed_img_pil, caption='Compressed Image', use_column_width=True)
        st.download_button(
            label="Download Compressed Image",
            data=byte_im,
            file_name="compressed_image.png",
            mime="image/png"
        )
