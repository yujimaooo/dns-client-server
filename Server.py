import socket
import threading
import time
import random
import sys

# read master file for record information
def load_file(file_path):
    records = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                domain, record_type, data = parts
                if domain not in records:
                    records[domain] = []
                records[domain].append((record_type, data))
    return records

def handle_client(data, addr, server_socket, records):
    query_id, qname, qtype = process_query(data)
    # simulate random processing delay
    delay = random.choice([0, 1, 2, 3, 4]) 
    time.sleep(delay)
    response = generate_response(query_id, qname, qtype, records)
    server_socket.sendto(response.encode('utf-8'), addr)
    log_response("snd", addr, query_id, qname, qtype)

# process client query
def process_query(data):
    query_id = int.from_bytes(data[:2], 'big')
    qname, qtype = data[2:].decode().split()
    return query_id, qname, qtype

def generate_response(query_id, qname, qtype, records):
    response = f"ID: {query_id}\n"
    response += "\nQUESTION SECTION:\n"
    response += f"{qname} {qtype}\n"

    answer_section = "\nANSWER SECTION:\n"
    authority_section = "\nAUTHORITY SECTION:\n"
    additional_section = "\nADDITIONAL SECTION:\n"
    has_answer = False
    has_authority = False
    has_additional = False

    # find matching record in the file
    def find_records(name, type):
        nonlocal has_answer, has_authority, has_additional, answer_section, authority_section, additional_section
        
        if name in records:
            for record in records[name]:
                record_type, record_data = record
                if record_type == type:
                    answer_section += f"{name} {record_type} {record_data}\n"
                    has_answer = True
                elif record_type == "CNAME":
                    answer_section += f"{name} CNAME {record_data}\n"
                    has_answer = True
                    find_records(record_data, type)
            if has_answer:
                return

        # look for NS record
        domain_parts = name.split('.')
        for i in range(len(domain_parts)):
            current_domain = '.'.join(domain_parts[i:])
            if current_domain == '':
                current_domain = '.'
            if current_domain in records:
                for record in records[current_domain]:
                    if record[0] == "NS":
                        authority_section += f"{current_domain} NS {record[1]}\n"
                        has_authority = True
                        # Look for A records for this NS
                        if record[1] in records:
                            for ns_record in records[record[1]]:
                                if ns_record[0] == "A":
                                    additional_section += f"{record[1]} A {ns_record[1]}\n"
                                    has_additional = True
                if has_authority:
                    return

        # look for root server
        if '.' in records:
            for record in records['.']:
                if record[0] == "NS":
                    authority_section += f". NS {record[1]}\n"
                    has_authority = True
                    # Look for A records for this root NS
                    if record[1] in records:
                        for ns_record in records[record[1]]:
                            if ns_record[0] == "A":
                                additional_section += f"{record[1]} A {ns_record[1]}\n"
                                has_additional = True

    find_records(qname, qtype)

    if has_answer:
        response += answer_section
    if has_authority:
        response += authority_section
    if has_additional:
        response += additional_section
    if not has_answer and not has_authority:
        response += "No matching records found.\n"

    return response

# respond to client
def log_response(action, addr, query_id, qname, qtype, delay=0):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.gmtime())[:-3]
    if action == "rcv":
        print(f"{timestamp} {action} {addr[1]}: {query_id} {qname} {qtype} (delay: {delay}s)")
    elif action == "snd":
        print(f"{timestamp} {action} {addr[1]}: {query_id} {qname} {qtype}")

def main():
    if len(sys.argv) != 2:
        print("The format should be: python Server.py <server_port>")
        sys.exit(1)

    server_port = int(sys.argv[1])
    records = load_file('master.txt')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', server_port))

    print(f"Server listening on port {server_port}")

    # handling multithreading, make sure server continuously listen to incoming packets
    while True:
        data, addr = server_socket.recvfrom(2048)
        log_response("rcv", addr, *process_query(data))
        # create new thread for every incoming packet
        threading.Thread(target=handle_client, args=(data, addr, server_socket, records)).start()

if __name__ == "__main__":
    main()