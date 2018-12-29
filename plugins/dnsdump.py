import re
import requests


def dnsmap(dnsmap_inp):
    domain = dnsmap_inp
    response = requests.Session().get('https://dnsdumpster.com/').text
    csrf_token = re.search(
        r"name='csrfmiddlewaretoken' value='(.*?)'", response).group(1)

    cookies = {'csrftoken': csrf_token}
    headers = {'Referer': 'https://dnsdumpster.com/'}
    data = {'csrfmiddlewaretoken': csrf_token, 'targetip': domain}
    response = requests.Session().post(
        'https://dnsdumpster.com/', cookies=cookies, data=data, headers=headers)

    image = requests.get('https://dnsdumpster.com/static/map/%s.png' % domain)
    if image.status_code == 200:
        image_name = domain.replace(".com","")
        with open('%s.png' % image_name, 'wb') as f:
            f.write(image.content)
            print("\nOpen reconspider/%s.png image to view full Mapping of %s domain" % (image_name, domain))
