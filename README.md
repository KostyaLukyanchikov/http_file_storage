# http_file_storage
simple http api to store files

    default host: localhost
    default port: 5000

*API:*

    method: GET
    description: Get single file content
    path: /files/<str: hash>

    method: POST
    description: Post file content. Request body must contain binary data
    path: /files

    method: DELETE
    description: delete single file content
    path: /files/<str: hash>

    method: GET
    description: get all files hashes
    path: /files


*Users:*

    1. admin admin
    2. user 1111

*Run server:*
    
    docker-compose up --build