# import xmltodict
# import json
# import ast
# import requests

# from audetemi.tm_soap_input_constant import (
#     LOGIN_XML,
#     LOGIN_URL
# )

# def cordis_login():
#     data = LOGIN_XML
#     url = LOGIN_URL
#     cordis_response = requests.post(url, data=data)

#     cordis_response = cordis_response.text

#     cordis_response_dict = xmltodict.parse(cordis_response)
#     cordis_response_json = json.dumps(cordis_response_dict)
#     result = ast.literal_eval(cordis_response_json)

#     cordis_token = result.get('SOAP:Envelope').get("SOAP:Body").get(
#         "samlp:Response").get("samlp:AssertionArtifact").get("#text")

#     if cordis_token:
#         return cordis_token
#     return False
