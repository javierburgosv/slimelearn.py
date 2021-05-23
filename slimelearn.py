from asyncio.events import get_event_loop
from asyncio.tasks import all_tasks
from typing import final
import websockets
import asyncio
import json

import nest_asyncio
nest_asyncio.apply()

__version__ = "0.8.0"

class SlimeLearn:

    ws = None

    req_template = {
        "req": "",
        "payload": {}
    }

    def __init__(self):
        pass

    ###################################################################
    #                   MONO THREAD IMPLEMENTATION                    #
    ###################################################################

    def run(self, uri, config, function):
        """
        Handles the connection, configuration and subscription to the server all at once

        :param uri: The url:port of the server. By default localhost:8080
        :param config: The json containing all the server required configuration
        :param function: The callback function with the logic for the AI
        """

        print(">> Connecting to server...")
        self.ws = asyncio.get_event_loop().run_until_complete(self._connect(uri))        
       
        if self.ws != None:
            print(">> Configuring server...")
            cstatus = asyncio.get_event_loop().run_until_complete(self._configure(config))
        
            if cstatus == 200:
                print(">> Listening to server...")
                asyncio.get_event_loop().run_until_complete(self._listen(function))
        
    async def _connect(self, dir):
        try:
            uri = "ws:" + dir
            ws = await websockets.connect(uri)
    
            return ws
        except Exception as e:
            print("Error. Please make sure JumpSlimeLearn is open and running correctly: ")
            print(e)

    async def _configure(self, config):
        res_code = None
        try:
            await self.ws.send(json.dumps(config))
            res = json.loads(await self.ws.recv())
            
            res_code = res["code"]
            if res_code == 400:
                raise Exception(res["data"]["message"])

        except Exception as e:
            print("Error. Impossible to configure server")
            print(e)
        
        finally:
            return res_code
    
    async def _listen(self, callback):
        try:
            async for msg in self.ws:
                js = json.loads(msg)
                callback(js["data"])

        except Exception as e:
            print(e)

    async def _disconnect(self):
        try:
            await self.ws.close()
        except Exception as e:
            print("Error. Impossible to disconnect:")
            print(e)
    

    ###################################################################
    #                       Requests to Server                        #
    ###################################################################

    def jump(self, angle = None):
        """ 
        Sends a basic action 'JUMP' to the server

        :param angle (optional): The angle for the direction of the jump vector
        """
        temp = {
            "req": "jump"
        }

        if angle != None:
            temp["payload"] = {
                "angle": angle
            }

        packet = json.dumps(temp)        
        asyncio.get_event_loop().run_until_complete(self._askForAction(packet))
    
    def reset(self):
        """ 
        Sends a basic action 'Reset' to the server
        """
        temp = {
            "req": "reset"
        }

        packet = json.dumps(temp)
        asyncio.get_event_loop().run_until_complete(self._askForAction(packet))

    async def _askForAction(self, act: str):
        try:
            await self.ws.send(act)
        except Exception as e:
            print("Error. Impossible to send action " + act)
            print(e)

    
    ###################################################################
    #                           JSON Utiles                           #
    ###################################################################

    def load_config_file(self, file="config.json"):
        """
        Loads the .json file as a Python dic

        :param file: The route of the config file.
        """
        try:
            with open(file) as config_file:
                return json.load(config_file)
        except Exception as e:
            print("Error. Something went wrong opening the configuration file")
            print(e)