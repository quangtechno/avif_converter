import requests
import pandas as pd
from urllib.parse import urlparse
import os
def download_image(url, save_path):
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path = os.path.join(save_path, filename)
        response = requests.get(url,stream=True)
        if response.status_code == 200:
            open(save_path, 'wb').write(response.content)
            print(f"Image successfully downloaded: {save_path}")
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print(f"✅ image load {save_path}")
        else:
            print(f"❌ error during image loading{response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ connection error {e}")



def read_image_urls_from_excel(file_path, sheet_name='Too large images', column_name='Image URL'):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if column_name in df.columns:
            url_col= df[column_name].dropna().tolist()
            return url_col
        else:
            return []
    except Exception as e:
        print(f"❌ excel reading error: {e}")
        return []


url_col=read_image_urls_from_excel('./voco_audit.xlsx')
print(len(url_col))
for i, url in enumerate(url_col):
    download_image(url, f'./download_image')
