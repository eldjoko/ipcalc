import ipaddress


def get_all_subnet_masks():
    """get list of all subnet masks"""
    return [str(ipaddress.IPv4Network(f'0.0.0.0/{prefix_length}').netmask) for prefix_length in range(0,33)]


def get_subnet_info(network_str: str):
    try:
        network = ipaddress.ip_network(network_str, strict=False)
        return {
            "Subnet": str(network),
            "Network Address": str(network.network_address),
            "Broadcast Address": str(network.broadcast_address),
            "Number of addresses": network.num_addresses,
            "Number of usables addresses": (
                network.num_addresses - 2
                if network.num_addresses > 2
                else network.num_addresses
            ),
            "Network Range": [(
                str(network.network_address),
                str(network.broadcast_address),
            )],
            "Subnet Mask": str(network.netmask),
            "Wildcard Mask": str(ipaddress.IPv4Address(~int(network.netmask) & 0xFFFFFFFF))
            # "hosts": [str(host) for host in network.hosts()],
        }
    except ValueError:
        return None

def generate_all_subnets(address: str, netmask: str):
    """generate all possible subnets within a prefix

    Args:
        prefix (str): network to generate subnets for
        mask (str): subnet mask or CIDR
    Example:
        generate('192.168.1.0', 23)
    """
    try:
        network = ipaddress.IPv4Network(f"{address}/{netmask}", strict=False)

        # Original prefix length
        original_prefix_length = network.prefixlen

        # List to store all subnets
        all_subnets, all_hosts = [], []
        # Generate subnets for all prefix lengths greater than the original prefix length
        for new_prefix_length in range(original_prefix_length + 1, 33):
            subnets = list(network.subnets(new_prefix=new_prefix_length))
            hosts = list(network.hosts())
            all_subnets.extend(subnets)
            all_hosts.extend(hosts)    
        return {
            'Subnets': all_subnets,
            'Usable Hosts': all_hosts
        }
    except ValueError as e:
        return str(e)
