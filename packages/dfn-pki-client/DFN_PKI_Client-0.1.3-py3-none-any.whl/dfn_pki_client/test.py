#!/usr/bin/env python

import click

from public_service import PublicServicePKI
from registration_service import RegistrationService
from utils import get_wsdl


@click.command()
@click.version_option()
def main():

    proxy = {"http": "http://proxy.charite.de:8080", "https": "http://proxy.charite.de:8080"}

    pki = PublicServicePKI("../config.ini", proxy=proxy)
    ca_info = pki.get_ca_info(510)

    # print(ca_info)

    with open("PN_Robert_Graetz_-_Charite_Teilnehmerservice_Berlin_2021-01-04.p12", 'rb') as pkcs12_file:
        pkcs12_data = pkcs12_file.read()

        print(pkcs12_data)
        print(type(pkcs12_data))
    pkcs12_password = "5+k,%yyy"
    rs = RegistrationService("../config.ini", proxy, pkcs12_data, pkcs12_password)

    print(rs.get_ca_info())


if __name__ == '__main__':
    main()
