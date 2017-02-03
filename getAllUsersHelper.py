import socket
import ipaddress

# Helper function: Convert list from unicode to string
def convertList(list):
    for i in range(len(list)):
        list[i] = str(list[i])

# Helper function: Validate IPv4 address
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

# Helper function: Validate IPv6 address
def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

# Helper function that sorts lists of IP addresses
def sortIPList(ips):
    # Convert list of strings into list of IP address objects
    ipaddress.ip_address('203.59.166.123')
    listOfIPObjects = []
    for i in range(len(ips)):
        print ips[i]
        listOfIPObjects[i] = ipaddress.ip_address(ips[i])
    sorted(listOfIPObjects)
    for i in range(len(ips)):
        ips[i] = str(listOfIPObjects[i])

    # for i in range(len(ips)):
    #     ips[i] = "%3s.%3s.%3s.%3s" % tuple(ips[i].split("."))
    # ips.sort()
    # for i in range(len(ips)):
    #     ips[i] = ips[i].replace(" ", "")
