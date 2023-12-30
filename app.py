import dpkt
import socket
import pygeoip #Uses MaxMind's GeoIP database
import requests
import os
from pyshark_capture import capture_webtraffic

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def main():
    #Open captured pcap data
    capture_webtraffic()
    f = open('final_pyshark_capture.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    #Open KML file and create style, header and footer for KML file (this will be passed to google maps)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kml_file=kmlheader+plotIPs(pcap, get_public_ip())+kmlfooter
    download_kml_file(kml_file)
    print(kml_file)

def download_kml_file(kml_data):
    '''Saves a kml file to specified path'''
    try:
        downloads_path = input("Enter kml file download path destination: ")
        filename = 'ip_map.kml'
        # Full path for the new file
        full_path = os.path.join(downloads_path, filename)
        # Writing KML data to a file
        with open(full_path, 'w') as file:
            file.write(kml_data)
    except FileNotFoundError:
        print("No such file or directory. Try again.")
        download_kml_file() 
    print(f"KML file saved to {full_path}")

def plotIPs(pcap, public_ip):
    '''Processes a pcap file to extract source and destination IP addresses, 
    then generates and returns KML line strings for mapping these IPs.'''
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src) # This converts source IP from packed byte to dotted-decimal string format
            dst = socket.inet_ntoa(ip.dst)
            KML = return_KML(dst, src, public_ip)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts

def return_KML(dstip, srcip, public_ip):
    '''Get geolocation to be paired with the IP addresses.
    for the custom google maps map to work an IP addresses needs to be paired with a geolocation '''
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(public_ip) #Need to insert own IP address 
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

def get_public_ip():
    '''Gets public IP address from ipify.org and returns it as a string'''
    try:
        response = requests.get('https://api.ipify.org')
        return response.text  # Returns the external IP address as a string
    except requests.RequestException:
        return "Unable to get IP"

if __name__ =='__main__':
    main()