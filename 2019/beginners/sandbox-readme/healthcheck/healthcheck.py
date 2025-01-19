# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os

import nameko
from nameko.web.handlers import HttpRequestHandler
from nameko.timer import timer
import socket

logger = logging.getLogger('healthcheck')

http = HttpRequestHandler.decorator

state = {
    'healthy': None
}

class HealthcheckService:
  name = 'healthcheck'


  @http('GET', '/')
  def healthcheck_handler(self, request):
    if state['healthy']:
      return 200, 'healthy\n'
    else:
      return 503, 'unhealthy\n'

  @timer(interval=30)
  def healtcheck(self):
    address = os.environ.get('ADDRESS', '127.0.0.01')
    port = int(os.environ.get('PORT', '1337'))

    retries = 5
    while retries > 0:
      health = False
      try:
        health = healthcheck_challenge(address, port)
      except Exception as e:
        logger.warning('Healthcheck exception: {}'.format(e))
      if health:
        break
      logger.info('Retrying...')
      retries -= 1

    if health != state['healthy']:
      if health:
        logger.info('Challenge became healthy.')
      else:
        logger.info('Challenge became unhealthy.')
    state['healthy'] = health

def read_byte(sock):
  buf = sock.recv(1)
  if not buf:
    raise EOFError
  return buf

def read_until(sock, sentinel="\n"):
  s = ""
  while not s.endswith(sentinel):
    try:
      s += read_byte(sock).decode("utf-8")
    except EOFError:
      raise
  return s

# Implement your healthchecking here.
# Beware, this framework uses eventlet - third party I/O libraries might not
# work. Also, this is Python3.

def healthcheck_challenge(address, port):
  s = socket.create_connection((address, port))
  s.settimeout(10)
  read_until(s, '>')
  s.send(b'ls\n')
  read_until(s, 'README.flag')
  return True
