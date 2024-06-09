import ipaddress as ip



def validate_ip_address(ip_address: str):
    """validate ip address"""
    assert ip_address
    assert ip.ip_address(ip_address)