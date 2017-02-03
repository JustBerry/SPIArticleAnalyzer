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
    listOfIPv4Objects = []
    listOfIPv6Objects = []
    for i in range(len(ips)):
        if (is_valid_ipv4_address(ips[i])):
            listOfIPv4Objects.append(ipaddress.ip_address(unicode(ips[i])))
        else:
            listOfIPv6Objects.append(ipaddress.ip_address(unicode(ips[i])))
    listOfIPv4Objects = sorted(listOfIPv4Objects)
    listOfIPv6Objects = sorted(listOfIPv6Objects)
    for j in range(len(listOfIPv4Objects)):
        ips[j] = str(listOfIPv4Objects[j])
    for k in range(len(listOfIPv6Objects)):
        ips[len(listOfIPv4Objects)+k] = str(listOfIPv6Objects[k])
