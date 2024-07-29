# dns-client-server

## Overview
This repository contains the implementation of a simplified DNS client-server application using UDP. Developed as part of COMP9331 Computer Networks and Applications course, the project demonstrates socket programming and application layer protocol design.

## Features
🛜 Accepts client queries and responds with appropriate DNS resource records.  
🔊 Simulates network delays and handles multiple client requests concurrently.  
💬 Implements DNS message format and processes A, CNAME, and NS query types.  

## Workflow
```mermaid
graph TD
    A[Client Start] --> B[Create Query]
    B --> C[Send Query to Server]
    C --> D[Server Receives Query]
    D --> E[Server Parses Query]
    E --> F[Server Searches Records]
    F --> G{Record Found?}
    G -- Yes --> H[Generate Response]
    G -- No --> I[No Matching Record Response]
    H --> J[Server Sends Response]
    I --> J
    J --> K[Client Receives Response]
    K --> L[Display Response]
    L --> M[Client End]
    J --> N[Server Continues Listening]
