# TODO: Test and fix this Dockerfile
# TODO: Authenticate container against Cobbler's XMLRPC Container Port 80
FROM python:3.10.9
EXPOSE 69

WORKDIR /cbltftp

RUN pip3 install .

COPY . .

CMD ["sudo", "python3", "src/cobbler_tftp/cbl_tpftp.py"]