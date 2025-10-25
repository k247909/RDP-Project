# SHADOWHACKER-GOD: scripts/save_data.py (Python 3)

import sys, os, requests, base64

def save_data(gist_id, token, source_dir):
    # 1. ضغط المجلد بالكامل (tar/gzip)
    os.system(f"tar -czf saved_data.tar.gz -C {os.path.dirname(source_dir)} {os.path.basename(source_dir)}")
    
    # 2. تشفير الملف المضغوط إلى Base64
    with open("saved_data.tar.gz", "rb") as f:
        encoded_data = base64.b64encode(f.read()).decode('utf-8')
        
    # 3. إرسال البيانات المحدثة إلى Gist API
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/gists/{gist_id}"
    
    payload = {
        "description": "AEON RDP Persistent Data Backup",
        "files": {
            "fixed_data.b64": {
                "content": encoded_data
            }
        }
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("SUCCESS: Data saved persistently to GitHub Gist.")
    else:
        print(f"FATAL ERROR: Could not save data. Status: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    save_data(sys.argv[1], sys.argv[2], sys.argv[3])
