# ctf-jwt-token

An example about a vulnerability in the early JWT token node.js library.

## Basic Introduction to JWT Token

According to standard [RFC 7519](https://tools.ietf.org/html/rfc7519), JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties.  The claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure or as the plaintext of a JSON Web Encryption (JWE) structure, enabling the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC) and/or encrypted.

## How to Install The Vulnerable Component

The vulnerable component is presented as a simple website which is written in node.js. This application uses username and password to authenticate a login first, then it also generates a JWT token for the user to claim the user role. The token is saved in cookies and checked whenever the user tries to visit some restricted pages.

In this website, there are two different user roles: common user, admin user. The content of the main page after logging in is different. The flag is put on the admin main page. However, a visitor only has a demo account, which is a common user.

### Run The Component in One Step

The vulnerable website has been dockerized and published on [DockerHub](https://hub.docker.com/r/gluckzhang/ctf-jwt-token). You could directly run it with the following command:

```
docker run --rm -p 8080:8080 gluckzhang/ctf-jwt-token
```

After that the website is avaliable via `http://localhost:8080`.

### Build The Docker Image by Yourself

If you would like to make some modifications and build the image by yourself, the source code and Dockerfile are located in folder `target-website`. After updating the files, run the following command to build the image:

```
cd target-website
docker build -t IMAGE_TAG .
```

## How to Conduct The Attack

The goal of this attack is to extract the information which should be only seen by admin users. By default, the attacker could only get a common user account to experience the website. By modifying the JWT token, the attacher spoofs the server that he logs in as a admin.

Use the following script to conduct the attack:

```
python give_me_the_flag.py -l LOGIN_URL -u USERNAME -p PASSWORD
```

A screencast to show every step: TODO

## Background Theory of The Exploit

According to the standard of JWT token, a special algorithm `none` should be always supported. Commonly `none` is used after the integrity of a token is verified. However, some libraries (e.g. node.js jsonwebtoken v0.4.0) always treated tokens signed with the `none` algorithm as valid ones. As a result, everyone could create their own valid tokens with whatever payload they want.

Since the demo website uses a JWT token to claim a login user's role, we will update the token to 1) change the algorithm into `none` and 2) change the user role into `admin`.

Actually there is another vulerability which is related to JWT token[[2]](https://medium.com/101-writeups/hacking-json-web-token-jwt-233fe6c862e6). If the token declares to use `HS256` algorithm to encrypt the payload, the signature will be verified with the public key as secret key. Since it is easy to obtain the website server's public key, we could sign the payload by ourselves. Due to the limited time, this demo project does not implement that case.

## References

- [Critical vulnerabilities in JSON Web Token libraries](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/)
- [Hacking JSON Web Token (JWT)](https://medium.com/101-writeups/hacking-json-web-token-jwt-233fe6c862e6)
- [npm jsonwebtoken v0.4.0](https://www.npmjs.com/package/jsonwebtoken/v/0.4.0)