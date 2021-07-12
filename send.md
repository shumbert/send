# Goal
i want to build a toy end-to-end encrypt file sending service. Typically you would interact with the service via the website:
- Alice clicks on create a new send and selects a single file (or folder), or multiples files or folders
- client-side encrypts files (including filenames) and uploads them to the server
- some nice optional features i could add: link expiration, access count, password
- the website yields a send link which contains a send identifier as well as the encryption key. the encryption key should be in the url fragment
- Alice sends the link to Bob
- Bob clicks the link and sees the contents of the send: list of files and folders along with their size
- the interface should display download links for single files or for the whole send

also you could a cli client (rust) which would have similar functionality:
- create a send
- list files in a send
- download a file, or files, from a send
- optionally the cli client could have a proxy mode for transferring larger files (Alice creates a send and waits for Bob to start the transfer, when Bob starts it data is proxied via the server)

The server would have the following endpoints:
- main page to create a new send
- download page for viewing/downloading a send
- api:
  - create
  - list
  - download

Languages to be used:
- browser client side: javascript
- server side: nodejs???
- cli client: rust

Some other similar services:
- [bitwarden send](https://bitwarden.com/products/send/)
- [magic wormhole](https://magic-wormhole.readthedocs.io/en/latest/welcome.html)
- [wormhole](https://wormhole.app/)

# send structure
a send would actually be composed of:
- a json metadata file: list all files the send, along with filename and size
- one or multiple files

# some notes about crypto
we only need to do symmetric authenticated encryption. We can use libsodium for that purpose, it has bindings for all the languages i plan to use and it looks like it's the golden standard for doing crypto those days

libsodium uses chacha20 (or xsalsa2020) and poly1305 for authenticated encryption

one thing to take care with stream ciphers is not to re-use the nonce (for instance you can use a counter and increment the nonce for each encryption operation). in the present case each new send will have a different key so we don't care. actually we could hard-code the nonce if needed, so we don't need to send it along the encrypted data

fyi here is how some similar services generate send identifiers and encryption keys:
- https://wormhole.app/GqaZM#HVUL4qA-qRt23-2vDJlwtw
- https://send.bitwarden.com/#b05apZyICEiSYK0rACqK9w/BugJ9h22okZyDGMWCnDEqw
- margic wormhole: 7-crossover-clockwork

# what to do next
- do a test run with libsodium, maybe in python
- finalize the structure of the send
- build the server api, test it with the python client
- write the rust cli client
- built the website

# python libsodium test run
https://pynacl.readthedocs.io/en/latest/

one thing to clarify: we want to send the encryption key in the url anchor part of the send link, but the key is pretty long (32 bytes!!). i feel like bitwarden for instance is doing something different, like creating a password and then deriving the encryption key from the password. what is sent as part of the url anchor is the password, not the encryption key

check out bitwarden code to find out!

bitwarden web app code is in here: https://github.com/bitwarden/web. it has a sub repo for the jslib (https://github.com/bitwarden/jslib)

when you navigate to https://vault.bitwarden.com/#/sends it runs the send compoment. when you create a new send it displays a modal with the send addedit component

note that add-edit.component.ts exists in two locations:
- web/src/app/send/add-edit.component.ts
- jslib/angular/src/components/send/add-edit.component.ts

the second one has more interesting stuff, including a submit function which in turn calls encryptSend, which calls the encrypt function from jslib/common/src/services/send.service.ts

submit function appears in compiled main.js at line 104379

encrypt does the following (among other things):
1. create 16 random bytes `model.key = await this.cryptoFunctionService.randomBytes(16);` and create a send key `model.cryptoKey = await this.cryptoService.makeSendKey(model.key);`
2. assign model.key to send.key
3. encrypt the text with model.cryptoKey

makeSendKey uses a hkdf function to derive a 64 bytes symmetric key from model.key

one thing we can do is generate two random 16 bytes value:
- first one wil be the send identifier
- second one will the send key
- the send encrypton key can be derived from send key

# finalize the structure of the send
Each send is identified by a 16 bytes random identifier. It consists of metadata information as well as one or more file blobs.

Metadata information is a JSON structure which contains:
- send id (is that necessary?)
- encrypted data
  - tree structure for files in the send
    - for each file there is a blob id, the name and the size
- hash of send password (optional)
- link expiration (optional)
- access count (optional)

Then each file is encrypted and uploaded to the server.

On the server each send is in its own directory (named using the send idenfitier). Metadata is stored as metadata.json, each file blob is stored in a file named after the blob id.

We use authenticated encryption, i.e. during decryption the mac is checked. If there is any mismatch it will result in an error. That protects againt malicious change of the data but also againt transmission errors.

# Server API
Flask + Gunicorn RESTful api

Operations:
- send: GET/PUT/POST
- file: POST

Using application/json data format

# todo
- finish learning about flask
- write the api part
- learn more about how to write tests
