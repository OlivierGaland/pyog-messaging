# pyog-messaging
Simple toolbox for communication between server and client

Dependencies : og-log : pip install og-log

Usage :

- UDPClient / TCPClient : client side (udp or tcp), send message with send_suspended (blocking call) or send_nonsuspended (new thread)

- ThreadedTCPServer : tcp server, will close the connection after each query/reply 
- ThreadedPersistentTCPServer : tcp server, keep connection alive for subsequent query/reply 
- ThreadedUDPServer : udp server

Client and Server have a callback to process message on reception : default is _process_msg (will run "return msg.execute") and can be overidden with your custom code (kwarg init key : callback)

- QueryMessage / ReplyMessage : inherit from to create your query/reply message, execute will be the callback on message reception (do process and return reply message for query, and do process -if needed- for reply)
- ErrorMessage : for error management purpose
