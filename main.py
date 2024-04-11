import PIL.Image
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
from datetime import datetime

st.set_page_config(layout="wide", page_title= "Creative Image Gen")
row1_1, row1_2, row1_3 = st.columns(3)
row2_1, row2_2, row2_3 = st.columns(3)
row3_1, row3_2, row3_3 = st.columns(3)

st.session_state["value"] = 0
def sum_state():
    if st.session_state["value"] == 0:
        print(st.session_state["value"])
        os.remove("files_created")
        os.remove("files_with_logo")
        st.session_state["value"] += 1
        print(st.session_state["value"])
        print("if print")
    else:
        print(st.session_state["value"])
        print("else")

def merge_images(image_path, logo_path, output_path, x_val, y_val):
    img = PIL.Image.open(image_path)
    logo = logo_path
    img.paste(logo, (x_val, y_val), logo)
    img.save(output_path)
    return img

def add_logo(logo_path, width=None, height=None):
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #070f26;
        }
    </style>
    """, unsafe_allow_html=True)
    logo = Image.open(logo_path)
    #modified_logo = logo.resize((width, height))
    return logo


def getinfo(url):
    post_req = url + '/info'

    response = requests.post(post_req)
    return response


def txt2img(url, prompt, negative_prompt=None):
    post_req = url + '/sdapi/v1/txt2img'

    data = """{
        "prompt": "your_prompt" ,
        "negative_prompt": "your_negative_prompt",
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
        "override_settings": {},
        "override_settings_restore_afterwards": true,
        "refiner_switch_at": 0,
        "disable_extra_networks": false,
        "comments": {},
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
        "save_images": true,
        "alwayson_scripts": {}
        }"""
    data = data.replace("your_prompt", prompt)
    data = data.replace("your_negative_prompt", negative_prompt)

    output = subprocess.run(
        ['curl', '-X', 'POST', post_req, '-H', 'accept: application/json', '-H', 'Content-Type: application/json', '-d',
         data],
        capture_output=True,
        text=True)

    url_image = json.loads(output.stdout)["images"][0]
    image_genai = Image.open(BytesIO(base64.decodebytes(bytes(url_image, "utf-8"))))
    return image_genai


def gen_image(prompt, negative_prompt, image_count):
    image_list = []
    while len(image_list) <= image_count:
        st.session_state.img_base = []
        st.write("Describiste: ", prompt)
        image_genai = txt2img("https://o6aiiiu68yi86n-3001.proxy.runpod.net", prompt=prompt,
                              negative_prompt=negative_prompt)
        name = str(datetime.now().strftime("%d-%m-%Y-%H%M%S")) + ".png"
        image_genai.save("files_created/" + name)
        image_list.append(image_genai)
        st.write("EXITOSO")
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
        prompts = ["couple_hiking", "old_guy_alone", "old_lady_coffee","grandparents_grandchildren"]
        prompt_selector = st.selectbox(
            "Que te gustaria generar?", prompts,
            placeholder="Selecciona...",
        )
        if prompt_selector == "couple_hiking":
            prompt = "close up,couple ,latin american, old, nature, hike, happy, smiling, retired, sunset, real, 4k, best quality, contemplative,real, real quality, real person, real skin, real shadows,  no hats, landscape,"
            negative_prompt="ugly, abhorrent hands, ugly eyes, disformed, fake light, sad, ugly arms, bad quality, blurred,bad photo, bad fingers, abnormal, nsfw, sexy, hats, sombreros, headwear, hat, sombrero, caps"

        elif prompt_selector=="old_guy_alone":
            prompt="old guy, at the beach, sitting, happy, smiling, retired, sunset, real, 4k, best quality, contemplative,"
            negative_prompt="ugly, abhorrent hands, ugly eyes, disformed, fake light, sad, ugly arms, bad quality, blurred, bad photo"

        elif prompt_selector=="old_lady_coffee":
            prompt = "old lady, coffee shop, sitting, happy, smiling, retired, sunset, real, 4k, best quality, contemplative, real, real quality, real person, real skin, real shadows"
            negative_prompt= "ugly, abhorrent hands, ugly eyes, disformed, fake light, sad, ugly arms, bad quality, blurred, bad photo, bad fingers, abnormal, nsfw, sexy"
        elif prompt_selector=="grandparents_grandchildren":
            prompt= "grandparents and grandchildren,latin american, nature, happy, smiling, sunset, real, 4k, best quality, contemplative, real, real quality, real person, real skin, real shadows,  no hats, landscape, having fun"
            negative_prompt= "ugly, abhorrent hands, ugly eyes, disformed, fake light, sad, ugly arms, bad quality, blurred, bad photo, bad fingers, abnormal, nsfw, sexy, hats, sombreros, headwear, hat, sombrero, caps"
        pass

        image_count = st.number_input(label="Numero de imagenes a generar", value="min", step=1,
                                           min_value=1)
        gen = st.button("genera imagen base")
        if gen:
            st.session_state['img_base'] = gen_image(prompt, negative_prompt, image_count)
            # sum_state()

        if 'img_base' in st.session_state:
            with row3_1:
                st.image(st.session_state.img_base)

    with row2_2:
        st.session_state["img_logo"] = add_logo("profuturo_logo.png")
        if 'img_logo' in st.session_state:
            with row3_2:
                st.image(st.session_state.img_logo)

    with row2_3:
        x_val = st.slider("x", 0, 1024, 0)
        y_val = st.slider("y", 0, 1024, 0)
        #mass_production = st.button("mass production")
        result = st.button("Submit values")
        if result:
            with row3_3:
                for file in os.listdir("files_created"):
                    new_img = merge_images(image_path= ("files_created/"+file),
                                           logo_path= st.session_state.img_logo,output_path= ("files_with_logo/w_logo_"+ file),
                                       x_val= x_val, y_val= y_val)
                    st.image(new_img)
                    #st.session_state.img_history = st.session_state.img_history.append(new_img)
                    st.write("Resultado: ")

                shutil.make_archive("images_with_logo", 'zip', "files_with_logo")
                with open("images_with_logo.zip", "rb") as file:
                    st.download_button("Descargar imagenes con logo",
                                       data=file, file_name="images_with_logo.zip", key="images_W_logo1234")


if __name__ == "__main__":
    main()
