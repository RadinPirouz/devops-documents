openssl genrsa -out gitea.key 2048
openssl req -new -key gitea.key -out gitea.csr
openssl x509 -req -in gitea.csr -signkey gitea.key -out gitea.crt
