import uvicorn
import socket

def find_available_port(start_port=8000, max_port=8010):
    """Cari port yang tersedia mulai dari start_port"""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except socket.error:
                continue
    return None

if __name__ == "__main__":
    port = find_available_port(8000, 8010)
    if port:
        print(f"✅ Starting server on port {port}")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=True
        )
    else:
        print("❌ No available ports found in range 8000-8010")
        print("Try manually: uvicorn app.main:app --reload --port 8001")