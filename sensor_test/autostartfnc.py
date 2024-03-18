# Filename: install_service.py

import os

def install_service():
    service_name = "sensor_service"
    script_path = "/path/to/original_script.py"  # Update with the path to your original script
    service_content = f"""[Unit]
Description=Sensor Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 {script_path}
WorkingDirectory={os.path.dirname(script_path)}
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
    """
    with open(f"/etc/systemd/system/{service_name}.service", "w") as f:
        f.write(service_content)
    os.system("sudo systemctl daemon-reload")
    os.system(f"sudo systemctl enable {service_name}")
    os.system(f"sudo systemctl start {service_name}")

if __name__ == "__main__":
    install_service()
