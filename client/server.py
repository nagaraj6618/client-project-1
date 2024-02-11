import subprocess
import webbrowser

PORT = 8000

def serve_html_file(html_file_path):
    # Start the HTTP server in a separate subprocess
    server_process = subprocess.Popen(["python", "-m", "http.server", str(PORT)])
    
    # Open the HTML file in the default web browser
    webbrowser.open(f"http://localhost:{PORT}/{html_file_path}")

    # Wait for the server process to terminate
    server_process.wait()

if __name__ == "__main__":
    html_file_path = "index.html"
    serve_html_file(html_file_path)
