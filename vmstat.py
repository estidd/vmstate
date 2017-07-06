import json
import requests
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
requests.packages.urllib3.disable_warnings() # Disable warnings

# Environment configuration variables
controller = "198.18.133.200"
username = 'admin'
password = 'C1sco12345'


def get_token():
    """
    Function to authenticate to the APIC and return an authentication token.
    """

    # Form the API request and send
    url = "https://" + controller + "/api/aaaLogin.xml"

    payload = "<aaaUser name='{0}' pwd='{1}'/>".format(username, password)
    headers = {
        'content-type': "application/xml",
        'cache-control': "no-cache",
        }

    response = requests.post(url, data=payload, headers=headers, verify=False)
    token = ElementTree.fromstring(response.text)[0].attrib['token']

    return token

def get_vms(token):
    """
    Function that returns an XML object containing
    APIC resource names and link states.
    """

    # Form the API request and send
    url = "https://" + controller + "/api/node/mo/comp/prov-VMware/ctrlr-[My-vCenter]-dCloud-DC/hv-host-137.xml"
    querystring = {"rsp-subtree-include": "relations"}
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/xml",
        'Cookie': "APIC-Cookie={0}".format(token)
        }

    # Prepare the response
    response = requests.get(url,verify=False, headers=headers, params=querystring)
    response_xml = ElementTree.fromstring(response.text)

    # Create XML object to return
    result_xml = ElementTree.Element('root')

    # Parse response for VM resources and create resource subelements
    for elem in response_xml.iterfind('compVm'):
        resource = ElementTree.SubElement(result_xml, 'resource')
        resource.set('name', elem.attrib['name'])
        resource.set('state', elem.attrib['state'])

    # Parse response for Hypervisor resources and create resource subelements
    for elem in response_xml.iterfind('compHv'):
        resource = ElementTree.SubElement(result_xml, 'resource')
        resource.set('name', elem.attrib['name'])
        resource.set('state', elem.attrib['state'])

    return result_xml


if __name__ == '__main__':
    token = get_token()
    vms = get_vms(token)
    xmlstr = minidom.parseString(ElementTree.tostring(vms)).toprettyxml(indent="    ")

    with open('vmstat_output.xml', 'w') as f:
        f.write(xmlstr)
