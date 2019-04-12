# Import modules
import subprocess
import ipaddress

# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# Create file that we will store the IPs in
online_IPs = open("online_IPs.txt", "w+")
offline_IPs = open("offline_IPs.txt", "w+")

# For each IP address in the subnet,
# run the ping command with subprocess.popen interface
for i in range(len(all_hosts)):
    output = subprocess.Popen(['ping', '-n', '1', '-w', '2000', str(all_hosts[i])],
                              stdout=subprocess.PIPE, startupinfo=info).communicate()[0]

    if "Destination host unreachable" in output.decode('utf-8'):
        # print(str(all_hosts[i]), "is Offline")
        offline_IPs.write(all_hosts[i])
        offline_IPs.write("\n")
    elif "Request timed out" in output.decode('utf-8'):
        # print(str(all_hosts[i]), "is Offline")
        offline_IPs.write(str(all_hosts[i]))
        offline_IPs.write("\n")
    else:
        # print(str(all_hosts[i]), "is Online")
        online_IPs.write(str(all_hosts[i]))
        online_IPs.write("\n")

offline_IPs.close()
online_IPs.close()
