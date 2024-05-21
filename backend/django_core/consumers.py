from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from surveybuilder.views import survey_view
from surveybuilder.models import Survey, Block
import asyncio

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['id']
        await self.accept()

        # 使用sync_to_async将同步数据库操作转换为异步操作
        self.survey = await sync_to_async(Survey.objects.get)(pk=self.room_id)
        self.blocks = await sync_to_async(Block.objects.filter)(survey=self.survey.id)
        self.survey_data = await sync_to_async(survey_view.get_survey_data)(self.survey, self.blocks)

        # 发送第一次的survey_data广播
        await self.send(json.dumps({
            'survey_data': self.survey_data
        }))

        # 开始定时任务，每2秒查询一次数据库并进行广播
        self.task = asyncio.ensure_future(self.broadcast_survey_data())
        
    async def disconnect(self, close_code):
        # 在连接断开时取消定时任务
        self.task.cancel()

    async def receive(self):
        await self.send(json.dumps({
            'reply': 'Received message: ' + str(self)
        }))

    import json

    async def broadcast_survey_data(self):
        while True:
            try:
                self.survey = await sync_to_async(Survey.objects.get)(pk=self.room_id)
                self.blocks = await sync_to_async(Block.objects.filter)(survey=self.survey.id)
                self.survey_data = await sync_to_async(survey_view.get_survey_data)(self.survey, self.blocks)
                new_survey_data = await sync_to_async(survey_view.get_survey_data)(self.survey, self.blocks)
                await self.send(json.dumps({
                    'survey_data': new_survey_data
                }))
            
                # 等待2秒
                await asyncio.sleep(10)
            
            except asyncio.CancelledError:
                break
