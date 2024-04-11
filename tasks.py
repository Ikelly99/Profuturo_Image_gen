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

def merge_images(image_path, background_path, output_path, x_val, y_val):
    img = remove(image_path)
    newimg = background_path
    newimg.paste(img, (x_val, y_val), img)
    newimg.save(output_path)
    return newimg

def add_logo():
    bg = "profuturo_logo.png"
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