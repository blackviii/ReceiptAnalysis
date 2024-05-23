import os
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# 设置端点和密钥
endpoint = "https://westus.api.cognitive.microsoft.com/"
key = "8ea5eb87f3c54a08b601f8bd54d655fc"

# 创建客户端
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def getOcrContentByUrl(url: str) -> str:
    print(url)
    # 从URL获取图片数据
    response = requests.get(url)
    image_data = response.content

    # 开始分析文档
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-receipt", document=image_data
    )
    receipts = poller.result()

    # 收集输出结果
    output = []
    for idx, receipt in enumerate(receipts.documents):
        output.append(f"--------Recognizing receipt #{idx + 1}--------")
        receipt_type = receipt.doc_type
        if receipt_type:
            output.append(f"Receipt Type: {receipt_type}")
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            output.append(f"Merchant Name: {merchant_name.value} has confidence: {merchant_name.confidence}")
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            output.append(f"Transaction Date: {transaction_date.value} has confidence: {transaction_date.confidence}")
        if receipt.fields.get("Items"):
            output.append("Receipt items:")
            for idx, item in enumerate(receipt.fields.get("Items").value):
                output.append(f"...Item #{idx + 1}")
                item_description = item.value.get("Description")
                if item_description:
                    output.append(f"......Item Description: {item_description.value} has confidence: {item_description.confidence}")
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    output.append(f"......Item Quantity: {item_quantity.value} has confidence: {item_quantity.confidence}")
                item_price = item.value.get("Price")
                if item_price:
                    output.append(f"......Individual Item Price: {item_price.value} has confidence: {item_price.confidence}")
                item_total_price = item.value.get("TotalPrice")
                if item_total_price:
                    output.append(f"......Total Item Price: {item_total_price.value} has confidence: {item_total_price.confidence}")
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            output.append(f"Subtotal: {subtotal.value} has confidence: {subtotal.confidence}")
        tax = receipt.fields.get("TotalTax")
        if tax:
            output.append(f"Tax: {tax.value} has confidence: {tax.confidence}")
        tip = receipt.fields.get("Tip")
        if tip:
            output.append(f"Tip: {tip.value} has confidence: {tip.confidence}")
        total = receipt.fields.get("Total")
        if total:
            output.append(f"Total: {total.value} has confidence: {total.confidence}")
        output.append("---------------------------------------")
    
    # 返回结果字符串
    return "\n".join(output)

# 示例调用
#url = "https://example.com/path/to/your/image.png"
#result = getOcrContentByUrl(url)
#print(result)
