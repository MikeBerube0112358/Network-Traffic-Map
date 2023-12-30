# Network-Traffic-Map
Maps network traffic using google maps

This Python script captures and visualizes network traffic geographically, using PyShark for packet capture. By processing pcap data, it extracts IP addresses and uses the pygeoip library to map these to their respective geolocations. The script then generates a KML file, which can be imported into mapping services like Google Maps for a geographical representation of network traffic. Additionally, the script includes functionality to fetch the user's public IP address.

This project was built with help from "Violent Python A Cookboook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers", and from "Python Cybersecurity— Network Tracking using Wireshark and Google Maps" by Vinsloev
https://medium.com/vinsloev-academy/python-cybersecurity-network-tracking-using-wireshark-and-google-maps-2adf3e497a93
and 

To generate map go to this link:  https://www.google.com/mymaps  and go to > Create a New Map > Add Layer > Import. Upload kml file.
