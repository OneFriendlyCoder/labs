#!/usr/bin/env python3
import os
import http.server
import socketserver

# Serve and create the file in /tmp instead of /home/.evaluationScripts
FILE_DIR = "/tmp"
FILE_NAME = os.path.join(FILE_DIR, "system_update")
PORT = 30001
FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
TEXT_DATA = b"This is a system update file. "  # bytes pattern to write

def create_dummy_file():
    """
    Create a 'system_update' file of 100MB filled with TEXT_DATA if it does not already exist.
    Uses an atomic write (temp file + rename).
    """
    os.makedirs(FILE_DIR, exist_ok=True)
    tmp_path = FILE_NAME + ".tmp"

    try:
        if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) == FILE_SIZE:
            print(f"File '{FILE_NAME}' already exists with the correct size.")
            return
    except Exception:
        pass

    print(f"Creating file '{FILE_NAME}' with size {FILE_SIZE} bytes...")
    try:
        with open(tmp_path, "wb") as f:
            written = 0
            chunk = TEXT_DATA
            while written < FILE_SIZE:
                to_write = min(len(chunk), FILE_SIZE - written)
                f.write(chunk[:to_write])
                written += to_write
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, FILE_NAME)  # atomic move
        print(f"File '{FILE_NAME}' created.")
    except Exception as e:
        # cleanup tmp if something went wrong
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
        raise

class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Serve only the /system_update path by streaming the FILE_NAME contents.
    """
    def do_GET(self):
        if self.path != "/system_update":
            self.send_error(404, "Not Found")
            return

        if not os.path.isfile(FILE_NAME):
            self.send_error(404, "File not found")
            return

        try:
            file_size = os.path.getsize(FILE_NAME)
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Length', str(file_size))
            self.end_headers()

            # Stream file in chunks
            with open(FILE_NAME, "rb") as f:
                chunk_size = 64 * 1024
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except BrokenPipeError:
                        # client disconnected
                        break
        except Exception:
            self.send_error(500, "Internal Server Error")

def run_server():
    """
    Run a simple HTTP server on the hardcoded port, serving only the 'system_update' file.
    """
    # Allow address reuse (helps when restarting the server quickly)
    class ReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReuseTCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving file '{FILE_NAME}' on port {PORT} (http://localhost:{PORT}/system_update) ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    create_dummy_file()
    run_server()
