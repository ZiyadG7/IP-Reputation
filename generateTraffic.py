from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import time
import csv
from mininet.cli import CLI 
import socket

class CustomTopo(Topo):
    def build(self):
        # Add server and its subnet
        server_subnet = self.addSwitch('s1')
        server = self.addHost('server', ip='10.0.0.1/24', ipv6='2001:db8::1/64')
        self.addLink(server, server_subnet)
        
        switch = self.addSwitch('s2')
        self.addLink(switch, server_subnet)  # Connect the switch to the server subnet

        for i in range(2, 7):
            for j in range(1, 101):
                host_ipv4 = f'10.0.0.{(i-2)*100+j+1}/24'  # IPv4 address for each host
                host_ipv6 = f'2001:db8::{(i-2)*100+j+1}/64'  # Unique IPv6 address for each host
                host = self.addHost(f'h{i}{j}', ip=host_ipv4, ipv6=host_ipv6)
                self.addLink(host, switch)


def generate_traffic(net, server, subnets):
    server_ipv6 = '2001:db8::1'
    server_interface = 'server-eth0'
    
    print('Server ip a: ',server.cmd('ip a'))
    # Start tcpdump with increased buffer size and verbose output for debugging
    server.cmd(f'sudo tcpdump -i {server_interface} -w /tmp/traffic_capture.pcap  -s 0 -B 4096 &')

    time.sleep(5)

    with open('/tmp/host_status.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Host', 'IPv6 Address', 'Status'])

        for i, hosts in enumerate(subnets):
            for host in hosts:
                # ipv6_address = host.params['ip'].split('/')[0]
                ipv6_address = host.params['ipv6']
                writer.writerow([host.name, ipv6_address, 'benign'])
                # host.cmd(f'ping6 -c 10 {server_ipv6} &')
                # output = host.cmd('ip a')
                # print('host ip: ',output)
                host.cmd(f'ping6 -c 10 {server_ipv6}  &')
                
            

        malicious_hosts_count = [13, 5, 20, 25, 17]
        num_packets_udp = 10
        packet_data = b"Hello, world!"
        server_port = 80
        
        for i, count in enumerate(malicious_hosts_count):
            for j in range(count):
                host = subnets[i][j]
                ipv6_address = host.params['ipv6']
                writer.writerow([host.name, ipv6_address, 'malicious'])

                                # Number of packets to send
                # num_packets = 1000  # Adjust this number as needed
                
                print(f"Starting ICMPv6 flood to {server_ipv6} with {num_packets} packets.")
                
                # Send the packets
                # for _ in range(num_packets):
                #     send(icmpv6_packet, verbose=0)
                #     time.sleep(0.01)  # Adding a slight delay to control the flood rate
                    
                host.cmd(f'ping6 -c 2 {server_ipv6} &')
                host.cmd(f'echo "Hello, world!" | socat - UDP6:[{server_ipv6}]:80 &')
                
                
                
            
                
                 
            

    time.sleep(70)
    server.cmd('killall tcpdump')

def main():
    setLogLevel('info')
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink, controller=OVSController)
    net.start()

    server = net.get('server')
    
    # Manually add the IPv6 address to the server
    server_ipv6 = '2001:db8::1/64'
    server.cmd(f'ip -6 addr add {server_ipv6} dev server-eth0')
    
    print('server ip: ',server.params["ipv6"].split("/")[0])
    subnets = [[net.get(f'h{i}{j}') for j in range(1, 101)] for i in range(2, 7)]


    
    for host in net.hosts:
        ipv6_global = host.params['ipv6']
        host.cmd(f'ip -6 addr add {ipv6_global} dev {host.name}-eth0')
        host.cmd(f'ip -6 route add default via {server.params["ipv6"].split("/")[0]} dev {host.name}-eth0')

                
        
                

    generate_traffic(net, server, subnets)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()

topos = { 'customtopo': (lambda: CustomTopo()) }
