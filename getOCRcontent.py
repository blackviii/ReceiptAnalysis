import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# 设置端点和密钥
endpoint = "https://westus.api.cognitive.microsoft.com/"
key = "8ea5eb87f3c54a08b601f8bd54d655fc"

# 创建客户端
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# 本地图片路径
local_image_path = "/Users/mimashi8888/Downloads/WX20240515-104831@2x.png"

# 打开本地图片文件
with open(local_image_path, "rb") as image_file:
    image_data = image_file.read()

# 开始分析文档
poller = document_analysis_client.begin_analyze_document(
    model_id="prebuilt-receipt", document=image_data
)
receipts = poller.result()

# 输出结果
for idx, receipt in enumerate(receipts.documents):
    print("--------Recognizing receipt #{}--------".format(idx + 1))
    receipt_type = receipt.doc_type
    if receipt_type:
        print("Receipt Type: {}".format(receipt_type))
    merchant_name = receipt.fields.get("MerchantName")
    if merchant_name:
        print("Merchant Name: {} has confidence: {}".format(merchant_name.value, merchant_name.confidence))
    transaction_date = receipt.fields.get("TransactionDate")
    if transaction_date:
        print("Transaction Date: {} has confidence: {}".format(transaction_date.value, transaction_date.confidence))
    if receipt.fields.get("Items"):
        print("Receipt items:")
        for idx, item in enumerate(receipt.fields.get("Items").value):
            print("...Item #{}".format(idx + 1))
            item_description = item.value.get("Description")
            if item_description:
                print("......Item Description: {} has confidence: {}".format(item_description.value, item_description.confidence))
            item_quantity = item.value.get("Quantity")
            if item_quantity:
                print("......Item Quantity: {} has confidence: {}".format(item_quantity.value, item_quantity.confidence))
            item_price = item.value.get("Price")
            if item_price:
                print("......Individual Item Price: {} has confidence: {}".format(item_price.value, item_price.confidence))
            item_total_price = item.value.get("TotalPrice")
            if item_total_price:
                print("......Total Item Price: {} has confidence: {}".format(item_total_price.value, item_total_price.confidence))
    subtotal = receipt.fields.get("Subtotal")
    if subtotal:
        print("Subtotal: {} has confidence: {}".format(subtotal.value, subtotal.confidence))
    tax = receipt.fields.get("TotalTax")
    if tax:
        print("Tax: {} has confidence: {}".format(tax.value, tax.confidence))
    tip = receipt.fields.get("Tip")
    if tip:
        print("Tip: {} has confidence: {}".format(tip.value, tip.confidence))
    total = receipt.fields.get("Total")
    if total:
        print("Total: {} has confidence: {}".format(total.value, total.confidence))
    print("--------------------------------------")

