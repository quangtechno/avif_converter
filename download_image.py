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
            print(f"✅ Tải ảnh thành công: {save_path}")
        else:
            print(f"❌ Lỗi khi tải ảnh. Mã trạng thái: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối: {e}")



def read_image_urls_from_excel(file_path, sheet_name='Too large images', column_name='Image URL'):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if column_name in df.columns:
            url_col= df[column_name].dropna().tolist()
            return url_col
        else:
            print(f"❌ Cột '{column_name}' không tồn tại trong sheet '{sheet_name}'.")
            return []
    except Exception as e:
        print(f"❌ Lỗi khi đọc file Excel: {e}")
        return []
def main():
    excel_file_path = 'image_urls.xlsx'  # Đường dẫn tới file Excel
    sheet_name = 'Too large images'  # Tên sheet chứa URL ảnh
    column_name = 'Image URL'  # Tên cột chứa URL ảnh

    image_urls = read_image_urls_from_excel(excel_file_path, sheet_name, column_name)

    for index, url in enumerate(image_urls):
        save_path = f'image_{index + 1}.jpg'  # Đặt tên file ảnh theo chỉ số
        download_image(url, save_path)

url_col=read_image_urls_from_excel('./voco_audit.xlsx')
print(len(url_col))
for i, url in enumerate(url_col):
    download_image(url, f'./download_image')
