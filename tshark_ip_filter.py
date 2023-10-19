import subprocess
from datetime import datetime

def capture_and_extract_packets(ip_address, capture_duration):
    # Get the current date and time to append to the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"Packets_{ip_address.replace('.', '_')}_{timestamp}.csv"

    # Define the tshark command to capture and filter
    cmd = [
        'tshark',
        '-a', f'duration:{capture_duration}',  # Capture duration
        '-Y', f'ip.addr == {ip_address}',  # Filter for specific IP address
        '-T', 'fields',  # Export as fields
        '-e', 'frame.number',
        '-e', 'frame.time',
        '-e', 'ip.src',
        '-e', 'ip.dst',
        '-e', 'ip.proto',
        '-e', 'frame.len',
        '-E', 'header=y',  # Include headers in the CSV
        '-E', 'separator=,',  # Set CSV separator as comma
        '-E', 'quote=d',  # Quote all fields with double quotes
        '-o', 'gui.column.format:"No.","%m","Time","%Yt","Source","%us","Destination","%ud","Protocol","%p","Length","%L"',
        '>', output_file  # Redirect output to the desired CSV file
    ]

    # Execute the command
    subprocess.run(' '.join(cmd), shell=True)
    return output_file

if __name__ == "__main__":
    target_ip = input("Enter the IP address to filter: ")

    # Ensure the provided duration is a valid number
    while True:
        try:
            capture_time = int(input("Enter the duration (in seconds) for packet capture: "))
            break
        except ValueError:
            print("Please enter a valid number for the duration.")

    print(f"Capturing packets from {target_ip} for {capture_time} seconds...")
    output_filename = capture_and_extract_packets(target_ip, capture_time)
    print(f"Data extracted to {output_filename} successfully!")
