import dns.resolver

import httpx

import dns.message
import dns.query
import dns.rdatatype


class DNSManager:
    """DNS Registrar wrapper to standardise DNS management."""

    __civo_ns = ["ns0.civo.com", "ns1.civo.com"]
    __digital_ocean_ns = ["ns1.digitalocean.com", "ns2.digitalocean.com", "ns3.digitalocean.com"]
    __vultr_ns = ["ns1.vultr.com", "ns2.vultr.com"]

    def evaluate_domain_ownership(self, domain_name):
        """
        Check if domain is owned by user
        :return: True or False
        """
        pass

    def evaluate_permissions(self):
        """
        Check if provided credentials have required permissions
        :return: True or False
            """
        pass


def get_domain_ns_records(domain_name: str, name_servers: [str] = ["8.8.8.8"]):
    # dns.name.from_text('www.dnspython.org')
    rv = dns.resolver.Resolver()
    rv.nameservers = name_servers
    answers = rv.resolve(domain_name, dns.rdatatype.NS)
    return [ns.to_text() for ns in answers]


def get_domain_txt_records_dot(domain_name: str, name_servers: [str] = ["8.8.8.8"]):
    rv = dns.resolver.Resolver()
    rv.nameservers = name_servers
    answers = rv.resolve(domain_name, dns.rdatatype.TXT)
    return [txt.to_text() for txt in answers]


def get_domain_txt_records_doh(domain_name: str, name_server: str = "8.8.8.8"):
    with httpx.Client() as client:
        q = dns.message.make_query(domain_name, dns.rdatatype.TXT)
        r = dns.query.https(q, "https://" + name_server, session=client)
        return [txt.to_text() for txt in r]