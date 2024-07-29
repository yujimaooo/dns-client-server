# dns-client-server

## Overview
This repository contains the implementation of a simplified DNS client-server application using UDP. Developed as part of COMP9331 Computer Networks and Applications course, the project demonstrates socket programming and application layer protocol design.

## Features
🛜 Accepts client queries and responds with appropriate DNS resource records.  
🔊 Simulates network delays and handles multiple client requests concurrently.  
💬 Implements DNS message format and processes A, CNAME, and NS query types.  

## Workflow
```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: Send DNS Query
    Server-->>Client: Acknowledge Receipt
    Server->>Server: Process Query
    Server->>Server: Look up Master File
    Server-->>Client: Send Response
    Client->>Client: Print Response
    Client->>Client: Timeout if no response
