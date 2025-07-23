import os
from http.server import BaseHTTPRequestHandler
from email.parser import BytesParser
from email.policy import default
import re
import io

UPLOAD_DIR = 'map'

def parse_content_disposition(header_value):
    """
    Minimal parser for Content-Disposition headers like:
    'form-data; name="file"; filename="example.txt"'
    """
    parts = header_value.split(';')
    disposition = parts[0].strip().lower()
    params = {}
    for part in parts[1:]:
        if '=' in part:
            key, val = part.strip().split('=', 1)
            params[key.lower()] = val.strip('"')
    return disposition, params

class FileRecieverServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/upload':
            self.send_error(404, "Endpoint not found")
            return

        content_type = self.headers.get('Content-Type')
        if not content_type or not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Invalid content type")
            return

        # Get boundary
        match = re.search('boundary=(.*)', content_type)
        if not match:
            self.send_error(400, "Missing boundary in multipart/form-data")
            return
        boundary = match.group(1)

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        full_message = (
            f"Content-Type: {content_type}\r\n\r\n".encode() + body
        )
        msg = BytesParser(policy=default).parsebytes(full_message)

        for part in msg.iter_parts():
            disposition_header = part.get('Content-Disposition', '')
            disposition, params = parse_content_disposition(disposition_header)

            if disposition != 'form-data' or 'filename' not in params:
                continue

            file_name = os.path.basename(params["filename"])
            file_data = part.get_payload(decode=True)

            os.makedirs(UPLOAD_DIR, exist_ok=True)
            filepath = os.path.join(UPLOAD_DIR, file_name)
            with open(filepath, 'wb') as f:
                f.write(file_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully.")
            return

        self.send_error(400, "No file uploaded")

    def do_GET(self):
        self.send_error(405, "Use POST /upload to upload files")
