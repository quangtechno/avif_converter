from PIL import Image
import pillow_avif
import re
import os
def convert_avif(input_path, quality=100):
    try:
       
        img = Image.open(input_path)
        filename=os.path.basename(input_path)
        filename_only, file_ext = os.path.splitext(filename)
        
        current_size = img.size 
        
        current_width, current_height = current_size
        if(current_width>1920 or current_height>1080):
            new_width = 1920
            new_height = round(new_width * current_height / current_width)
            img=img.resize((new_width, new_height))
            filename_only=filename_only.split('-')[0]+f'-{current_width}x{current_height}'+ f'-{new_width}x{new_height}'
            
        output_filename = filename_only + ".avif"
        output_path = os.path.join("./avif_image_folder", output_filename)
        img.save(output_path, format="AVIF", quality=quality)
        
        print(f"✅convert sucessfully: '{input_path}' -> '{output_path}' (quality: {quality})")
        
    except FileNotFoundError:
        print(f"❌ input file not found {input_path}")
    except Exception as e:
        print(f"❌ error during converting to AVIF : {e}")
def found_input_and_convert():
    for root, dirs, files in os.walk('./download_image'):
        for file in files:
            if file.lower().endswith(('.avif', '.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                input_path = os.path.join(root, file)
                
                convert_avif(input_path)
found_input_and_convert()