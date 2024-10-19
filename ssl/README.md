# SSL

## Generate Self-Signed SSL Certificate

### Create Root CA

```shell
openssl genrsa -des3 -out CA.key 4096
openssl req -new -x509 -days 3650 -key CA.key -out CA.crt
# Country Name (2 letter code) [AU]:HU
# State or Province Name (full name) [Some-State]:Budapest
# Locality Name (eg, city) []:Budapest
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:Example Inc.
# Organizational Unit Name (eg, section) []:
# Common Name (e.g. server FQDN or YOUR name) []:Example Root CA
# Email Address []:
```

### Create wildcard cert signed by the CA

```shell
openssl genrsa -out example.com.key 2048
```

```
# example.com.cnf

[req]
default_md = sha256
prompt = no
req_extensions = req_ext
distinguished_name = req_distinguished_name

[req_distinguished_name]
commonName = *.example.com
countryName = HU
stateOrProvinceName = Budapest
localityName = Budapest
organizationName = Example Inc.

[req_ext]
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=critical,serverAuth,clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1=example.com
DNS.2=*.example.com
```

```shell
openssl req -new -nodes -key example.com.key -config example.com.cnf -out example.com.csr
openssl x509 -req -in example.com.csr -CA CA.crt -CAkey CA.key -CAcreateserial -out example.com.crt -days 365 -extfile example.com.cnf -extensions req_ext
```
