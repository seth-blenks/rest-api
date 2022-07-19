# About Worker API

An API is a digital structure that allows applications to interact with information on data servers. This API is related business registry containing workers details.

## Who Would Use the API

The API is a test application. It is accessible to any one who have registered to the system.

## How to Use the API

After registration, your public and private keys will be made available on your dashboard. You can use the keys to make api queries.

## Basic API Query

To receive all the contents of the database you run the following get request with your public key as a parameter passed to the key variable.

`import requests
requests.get(‘https://www.vandies.com/api/v1/employee’,params={‘key’: public_key})
`

response `[{‘username’: ‘<name>’,’email’:’<email>’}, …]`

To update the users information you send a post request with your public and private key

requests.post(‘api.seth-seth.xyz/api/v1/employee’)

Link: api.seth-seth.xyz