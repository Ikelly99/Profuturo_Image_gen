import streamlit as st
import os
import subprocess
import shutil
import requests
import json
from io import BytesIO
import base64
from PIL import Image
from rembg import remove

st.set_page_config(layout="wide", page_title= "Creative Image Gen")
row1_1, row1_2, row1_3 = st.columns(3)
row2_1, row2_2, row2_3 = st.columns(3)
row3_1, row3_2, row3_3 = st.columns(3)

def merge_images(image_path, background_path, output_path, x_val, y_val):
    img = remove(image_path)
    newimg = background_path
    newimg.paste(img, (x_val, y_val), img)
    newimg.save(output_path)
    return newimg

def add_background():
    bg = st.file_uploader("escoge un fondo")
    if bg is not None:
        # To read file as bytes:
        bytes_data = bg.getvalue()
        image_bg = Image.open(BytesIO(bytes_data))
        return image_bg



def add_logo(logo_path, width, height):
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #070f26;
        }
    </style>
    """, unsafe_allow_html=True)
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


def getinfo(url):
    post_req = url + '/info'

    response = requests.post(post_req)
    return response


def txt2img(url, prompt, negative_prompt):
    post_req = url + '/sdapi/v1/txt2img'
    data = f'''{
        "prompt": {str(prompt)},
        "negative_prompt": {str(negative_prompt)},
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "DPM++ SDE",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 6,
        "cfg_scale": 1,
        "width": 1024,
        "height": 1024,
        "restore_faces": true,
        "tiling": false,
        "do_not_save_samples": false,
        "do_not_save_grid": false,
        "eta": 0,
        "denoising_strength": 0,
        "s_min_uncond": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 0,
        "override_settings": "",
        "override_settings_restore_afterwards": true,
        "refiner_switch_at": 0,
        "disable_extra_networks": false,
        "comments": "",
        "enable_hr": false,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": "",
        "sampler_index": "Euler",
        "script_args": [],
        "send_images": true,
        "save_images": false,
        "alwayson_scripts": ""}
'''
    output = subprocess.run(
        ['curl', '-X', 'POST', post_req, '-H', 'accept: application/json', '-H', 'Content-Type: application/json', '-d',
         data],
        capture_output=True,
        text=True)

    url_image = json.loads(output.stdout)["images"][0]
    image_genai = Image.open(BytesIO(base64.decodebytes(bytes(url_image, "utf-8"))))
    return image_genai


def main():
    if 'img_base' not in st.session_state:
        st.session_state.img_base = []
    if 'img_bg' not in st.session_state:
        st.session_state.img_bg = []
    if 'img_history' not in st.session_state:
        st.session_state.img_history = []

    with row1_1:
        st.title('Creative Image Gen')
        st.write("Demo")

    with row1_3:
        st.image("nttdata.png")

    with row2_1:
        prompt_selector = st.selectbox(
            "Que te gustaria generar?", ("prompt1", "prompt2"),
            placeholder="Selecciona...",
        )
        if prompt_selector == "prompt1":
            prompt = "old couple, black and white, infrared, b&W, composition, profesional, golden ratio, real light, at the beach, smiling, happy, retired, real, 4k, dune, movie frame,"
            negative_prompt = "ugly, abhorrent hands, ugly eyes, disformed, fake light, sad"
        else:
            pass
        gen = st.button("genera imagen base")
        if gen:
            st.session_state.img_base = []
            st.write("Describiste: ", prompt)
            image_genai= txt2img("https://o6aiiiu68yi86n-3001.proxy.runpod.net", prompt, negative_prompt)
            st.write("EXITOSO")
            st.session_state['img_base'] = image_genai

        if 'img_base' in st.session_state:
            with row3_1:
                st.image(st.session_state.img_base)

    with row2_2:
        st.session_state["img_bg"] = add_background()
        if 'img_bg' in st.session_state:
            with row3_2:
                st.image(st.session_state.img_bg)

    with row2_3:
        x_val = st.slider("x", 0, 520, 0)
        y_val = st.slider("y", 0, 520, 0)
        result = st.button("Submit values")
        if result:
            with row3_3:
                new_img = merge_images(st.session_state['img_base'], st.session_state.img_bg, "new1.png",
                                   x_val, y_val)
                st.image(new_img)
                st.session_state.img_history = st.session_state.img_history.append(new_img)
                st.download_button("Descargar", data= "new1.png", file_name="mamalucha_gen.png")
            st.write("Resultado: ")

if __name__ == "__main__":
    main()