from flask import Flask, request, redirect, url_for, render_template
from getOcrContentByUrl import getOcrContentByUrl
from getUrlByUploadImage import upload_image_and_get_url
from processWithOpenAI import process_string_with_openai


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        url = upload_image_and_get_url(file)
        ocr_result = getOcrContentByUrl(url)
        formatted_result = process_string_with_openai(ocr_result)  # 调用新的功能
        #formatted_result = ocr_result #取代上面的调用，下次注释掉这一样，换成上一行就行了
        return render_template('result.html', url=url, result=formatted_result)  # 在网页上显示格式化结果

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # 确保在容器中使用正确的端口
