# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vpic']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'vpic-api',
    'version': '0.2.0',
    'description': 'A client for the United States National Highway Traffic Safety Administration (NHTSA) Vehicle Product Information Catalog (vPIC) API',
    'long_description': '# vpic-api\nPython client library for decoding VINs and querying the United States \nNational Highway Traffic Safety Administration (NHTSA) [Vehicle Product \nInformation Catalog Vehicle Listing (vPIC) API](https://vpic.nhtsa.dot.gov/api/).\n\nUse this to gather information on vehicles and their specifications,\nand to decode VINs to extract information for specific vehicles. vPIC\nhas information about these types of vehicles sold or imported in\nthe USA:\n\n* Bus\n* Incomplete Vehicle\n* Low Speed Vehicle (LSV)\n* Motorcycle\n* Multipurpose Passenger Vehicle (MPV)\n* Passenger Car\n* Trailer\n* Truck\n\nvPIC has information about how manufacturers assign a VIN that\nencodes a vehicle\'s characteristics. Vehicle manufacturers provide this\ninformation to NHTSA under U.S. law 49 CFR Part 565.\n\nThe API available 24/7, is free to use, and does not require registration. NHTSA uses automatic traffic rate controls to maintain the performance of the API and their websites that use the API.\n\nSee https://vpic.nhtsa.dot.gov/api/home/index/faq for more on the API.\n\n## Using vPIC\n\n### Decode a Vehicle Identification Number (VIN)\n\nDecode a 17-digit Vehicle Identification Number (VIN):\n\n```python\nfrom vpic import Client\n\nc = Client()\n\nresult = c.decode_vin("1FA6P8TD5M5100001", 2021)\n```\n\nHere are a few of the 130+ attributes vPIC returns for the VIN:\n\n```json\n{\n    "Doors": "2",\n    "ErrorCode": "0",\n    "ErrorText": "0 - VIN decoded clean. Check Digit (9th position) is correct",\n    "Make": "FORD",\n    "MakeId": "460",\n    "Manufacturer": "FORD MOTOR COMPANY, USA",\n    "ManufacturerId": "976",\n    "Model": "Mustang",\n    "ModelId": "1781",\n    "ModelYear": "2021",\n    "PlantCity": "FLATROCK",\n    "PlantCountry": "UNITED STATES (USA)",\n    "PlantState": "MICHIGAN",\n    "Series": "I4 Coupe",\n    "VIN": "1FA6P8TD5M5100001",\n    "VehicleType": "PASSENGER CAR",\n}\n```\n\n### Get the Models for a Make and Model Year\n\n```python\nresult = c.get_models_for_make("TESLA", 2021)\n```\n\nvPIC returns a list of the models for this make and model year:\n\n```json\n[\n    {\n        "MakeId": 441,\n        "Make": "TESLA",\n        "ModelId": 1685,\n        "Model": "Model S"\n    },\n    {\n        "MakeId": 441,\n        "Make": "TESLA",\n        "ModelId": 10199,\n        "Model": "Model X"\n    },\n    {\n        "MakeId": 441,\n        "Make": "TESLA",\n        "ModelId": 17834,\n        "Model": "Model 3"\n    },\n    {\n        "MakeId": 441,\n        "Make": "TESLA",\n        "ModelId": 27027,\n        "Model": "Model Y"\n    }\n]\n```\n',
    'author': 'David Peckham',
    'author_email': 'dave.peckham@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidpeckham/vpic-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
