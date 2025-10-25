# SHADOWHACKER-GOD: scripts/restore_data.py (Python 3)

import sys, os, requests, base64

def restore_data(gist_id, token, target_dir):
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/gists/{gist_id}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("ERROR: Could not fetch Gist.")
        return
        
    gist_data = response.json()
    
    # 1. تحديد الملف المخزن (الذي يحمل اسم fixed_data.b64)
    file_content = gist_data['files'].get('fixed_data.b64', {}).get('content', '')
    
    if file_content:
        # 2. فك تشفير Base64 (بافتراض أن الملف مُشفر لحفظه كملف نصي)
        try:
            compressed_data = base64.b64decode(file_content)
            # 3. حفظ البيانات المضغوطة (يجب أن تكون بتنسيق tar.gz)
            with open("restored_data.tar.gz", "wb") as f:
                f.write(compressed_data)
            
            # 4. فك الضغط (يتطلب أمر tar من نظام التشغيل)
            os.system(f"tar -xzf restored_data.tar.gz -C {target_dir}")
            print("SUCCESS: Data restored from Gist.")
            
        except Exception as e:
            print(f"WARNING: Could not decode/extract data: {e}")
            
if __name__ == "__main__":
    restore_data(sys.argv[1], sys.argv[2], sys.argv[3])
