import socket
import sys
import random

# construct a query from query ID, query name, and query type
def client_query(query_id, qname, qtype):
    # convert query ID to 2-byte sequence
    query = query_id.to_bytes(2, 'big')
    query += f"{qname} {qtype}".encode('utf-8')
    return query

def main():
    # check if have correct input
    if len(sys.argv) != 5:
        print("The format should be: python Client.py <server_port> <qname> <qtype> <timeout>")
        sys.exit(1)

    server_port = int(sys.argv[1])
    qname = sys.argv[2]
    qtype = sys.argv[3]
    timeout = int(sys.argv[4])

    # randomize query ID
    query_id = random.randint(0, 65535)
    query = client_query(query_id, qname, qtype)

    # create UDP socket and set timeout
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)

    try:
        # send query to server
        client_socket.sendto(query, ('127.0.0.1', server_port))
        response, _ = client_socket.recvfrom(2048)
        # print if receive response
        print(response.decode('utf-8'))
    except socket.timeout:
        print("timed out")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()