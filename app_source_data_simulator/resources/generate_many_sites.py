import json
import random


def random_bizlocation_base() -> str:
    # Organization 0 + 8 digits
    # Sites 4 digits
    # TODO: The fourth digit in the site part should be a proper check digit
    base = random.randint(10000000, 99999999)
    return "0{}".format(base)


def random_bizlocation_sites(bizlocation, number_of_sites, name: str) -> list:
    site_array = []
    for sites in range(number_of_sites):
        random_location = random.randint(1000, 9999)
        gln_site = "{}{}".format(bizlocation, random_location)
        gln_site_name = "{} Site {}".format(name, sites)
        site_object = {
            'name': gln_site_name,
            'gln': gln_site
        }
        site_array.append(site_object)
    return site_array


def generate_organization_tree(name, number_of_sites):
    gln_organization = random_bizlocation_base()
    gln_sites = random_bizlocation_sites(gln_organization, number_of_sites, name)

    template = {
        'organization_name': name,
        'gln': gln_organization,
        'sites': gln_sites
    }
    return template


def generate_organizations():
    file = open('gln_map.txt')
    number_of_sites = 4
    """
    This will generate an array of organizations with the following shape
    
    {
    'organization_name': 'A Cool Name',
    'gln' : '10000000000000',
    'sites':[
                {   
                    'name': 'A Cool Name Site 1',
                    'gln' : '10000000000001'
                },
                {   
                    'name': 'A Cool Name Site 2',
                    'gln' : '10000000000002'
                }
            ]
    }
    """
    location_map = []
    organizations = file.readlines()
    for org in organizations:
        location_map.append(generate_organization_tree(org[:-1], number_of_sites))
    print(json.dumps(location_map, indent=2))
    location = open('location_map.json', 'w')
    location.write(json.dumps(location_map, indent=2))
    location.close()


if __name__ == '__main__':
    generate_organizations()
