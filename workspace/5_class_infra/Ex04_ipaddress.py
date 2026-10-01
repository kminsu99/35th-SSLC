import ipaddress

# 192.168.1.0/24 대역을 네트워크 객체로 생성합니다
network = ipaddress.ip_network("192.168.1.0/24")
print(f"네트워크 주소 : {network.network_address}")
print(f"브로드캐스트 주소 : {network.broadcast_address}")


target_ip = ipaddress.ip_address("192.168.1.55")
print(f"{target_ip}가 이 대역에 속하는가? {target_ip in network}")


target_ip = ipaddress.ip_address("192.168.0.55")
