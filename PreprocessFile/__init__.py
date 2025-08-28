import logging
import base64
import json
from io import BytesIO
from docx import Document
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("PreprocessFile function triggered...")

    try:
        req_body = req.get_json()
    except Exception:
        return func.HttpResponse("Invalid JSON body", status_code=400)

    file_name = req_body.get("fileName")
    file_content_base64 = req_body.get("fileContent")

    if not file_name or not file_content_base64:
        return func.HttpResponse(
            "fileName and fileContent are required", status_code=400
        )

    try:
        file_bytes = base64.b64decode(file_content_base64)
        doc = Document(BytesIO(file_bytes))
        extracted_text = "\n".join([p.text for p in doc.paragraphs])

        summary = f"Simulated summary of {file_name}:\n\n{extracted_text[:300]}..."
        return func.HttpResponse(
            json.dumps({"fileName": file_name, "summary": summary}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
