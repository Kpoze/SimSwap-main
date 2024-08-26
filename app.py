import streamlit as st
import os
import subprocess

# Définir les chemins des dossiers
UPLOAD_FOLDER = './demo_file/'
OUTPUT_FOLDER = './output/'
TEMP_FOLDER = './temp_results/'

# Créer les dossiers s'ils n'existent pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Titre de l'application
st.title('Face Swap')
image_path = None
# Choix du type de fichier à télécharger (image ou vidéo)
options = ['Image', 'Vidéo']
choice = st.selectbox('Choisissez le type de fichier à télécharger:', options)

# Sélection de la résolution
resolution = ['224', '512']
resolution_choice = st.selectbox('Choisissez la taille de la résolution:', resolution)

uploaded_file = None
command = ''


if choice == 'Image':
    uploaded_image = st.file_uploader("Upload face", type=['jpg', 'jpeg', 'png'])
    if uploaded_image:
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)
        with open(image_path, 'rb') as f:
            st.image(image_path, caption='Uploaded Image')


    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        uploaded_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(uploaded_path, 'rb') as f:
            st.image(uploaded_path, caption='Uploaded Image')
    
    swap_options_image = ['Simple', 'All', 'Specific']
    if image_path is not None : 
            swap_options_image_choice = st.selectbox('Choisissez votre option:', swap_options_image)
            
            if swap_options_image_choice == 'Simple':
                command = f'python test_wholeimage_swapsingle.py --crop_size {resolution_choice} --use_mask  --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --pic_b_path {uploaded_path} --output_path {OUTPUT_FOLDER}'
                print(command)
            
            elif swap_options_image_choice == 'All':
                command = f'python test_wholeimage_swapmulti.py --crop_size {resolution_choice} --use_mask  --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --pic_b_path {uploaded_path} --output_path {OUTPUT_FOLDER}'
                print(command)
            
            elif swap_options_image_choice == 'Specific':
                uploaded_specific = st.file_uploader("Specific face", type=['jpg', 'jpeg', 'png'])
                specific_path = None
                if uploaded_specific:
                    specific_path = os.path.join(UPLOAD_FOLDER, uploaded_specific.name)
                    with open(specific_path, 'rb') as f:
                        st.image(specific_path, caption='Uploaded Image')
                    
                    command = f'python test_wholeimage_swapspecific.py --crop_size {resolution_choice} --use_mask --pic_specific_path {specific_path} --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --pic_b_path {uploaded_path} --output_path {OUTPUT_FOLDER}'
                    print(command)
        # Exécution du script de swap
    if st.button('Swap'):
        if uploaded_image and uploaded_file and command:
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                st.success('Swap Complete!')
            else:
                st.error('Error during swapping process.')
        else:
            st.error('Please upload both an image and a video.')


elif choice == 'Vidéo':
    output_filename = st.text_input("Entrez le nom du fichier:", value="")
    output_filename = output_filename.strip() + ".mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        # Téléchargement de l'image de base
    uploaded_image = st.file_uploader("Upload face", type=['jpg', 'jpeg', 'png'])
    if uploaded_image:
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)
        with open(image_path, 'rb') as f:
            st.image(image_path, caption='Uploaded Image')

    uploaded_file = st.file_uploader("Upload Video", type=['mp4'])
    if uploaded_file:
        uploaded_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(uploaded_path, 'rb') as f:
            st.video(uploaded_path)

        swap_options_video = ['Simple', 'All', 'Specific']
        if image_path is not None : 
            swap_options_video_choice = st.selectbox('Choisissez votre option:', swap_options_video)
            
            if swap_options_video_choice == 'Simple':
                command = f'python test_video_swapsingle.py --no_simswaplogo --crop_size {resolution_choice} --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --video_path {uploaded_path} --output_path {output_path} --temp_path {TEMP_FOLDER}'
                print(command)
            
            elif swap_options_video_choice == 'All':
                command = f'python test_video_swapmulti.py --no_simswaplogo --crop_size {resolution_choice} --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --video_path {uploaded_path} --output_path {output_path} --temp_path {TEMP_FOLDER}'
                print(command)
            
            elif swap_options_video_choice == 'Specific':
                uploaded_specific = st.file_uploader("Specific face", type=['jpg', 'jpeg', 'png'])
                specific_path = None
                if uploaded_specific:
                    specific_path = os.path.join(UPLOAD_FOLDER, uploaded_specific.name)
                    with open(specific_path, 'wb') as f:
                        f.write(uploaded_specific.getbuffer())
                    st.image(specific_path, caption='Uploaded Image')
                    
                    command = f'python test_video_swapspecific.py --crop_size {resolution_choice} --use_mask --pic_specific_path {specific_path} --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path {image_path} --video_path {uploaded_path} --output_path {OUTPUT_FOLDER} --temp_path {TEMP_FOLDER}'
                    print(command)

    if st.button('Swap'):
        if uploaded_image and uploaded_file and command:
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            command += f' --output_path {output_path}'
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                st.success('Swap Complete!')
            else:
                st.error('Error during swapping process.')
        else:
            st.error('Please upload both an image and a video.')
                    

