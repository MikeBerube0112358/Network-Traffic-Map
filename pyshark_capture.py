import pyshark
import subprocess
import tempfile
import os


def capture_webtraffic():
    """ Captures network traffic from a specified interface ('Wi-Fi') for a given duration (10 seconds),
    saves it to a temporary pcapng file, then converts it to a standard pcap format.
    The temporary file is subsequently deleted after conversion."""
    interface = 'Wi-Fi'
    temp_output_file = "temp_pyshark_capture.pcapng"  # Temporary file for PyShark output
    final_output_file = "final_pyshark_capture.pcap"  # Converted file

    # Capture packets and save to a temporary file
    with pyshark.LiveCapture(interface=interface, output_file=temp_output_file) as capture:
        capture.sniff(timeout=10)

    # Convert the temporary file to standard .pcap format using editcap
    subprocess.run(['editcap', '-F', 'pcap', temp_output_file, final_output_file])
    # Delete temp file
    os.remove(temp_output_file)
