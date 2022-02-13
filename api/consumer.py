from channels.generic.websocket import AsyncWebsocketConsumer
import json
import requests

class Reports(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name='reports'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        # print (text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'randomFunction',
                'value':text_data,
            }
        )

    async def randomFunction(self,event):

        returned = event['value']
        returnedObject = json.loads(returned)
        latLong = f"{returnedObject['latitude']}, {returnedObject['longitude']}"
        api_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latLong}&result_type=administrative_area_level_2&key=AIzaSyAn90sbAUNy2Em2JDA7iAUy4wO18zfclxc"
        response = requests.get(api_url)
        res = response.json()
        result = res['results'][0]['address_components'][0]['long_name']
        category = returnedObject['category']
        context = {
            "area": result,
            "category": category
        }
        final_result = json.dumps(context)
        await self.send(final_result)
