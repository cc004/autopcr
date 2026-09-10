from ..modulebase import *      
from ...core.pcrclient import pcrclient      
from ...model.error import *      
from ...model.enums import *      
from ...model.requests import NbbTopRequest, NbbStartRequest, NbbFinishRequest, ArcadeStoryListRequest, ArcadeReadStoryRequest      
     
@name('新兵训练营小游戏称号（看下面）')      
@default(True)      
@description('需要先通过前两关！！！')      
class nbb_game(Module):      
    async def do_task(self, client: pcrclient):    
        # 检查剧情列表    
        req = ArcadeStoryListRequest()    
        req.arcade_id = 1013    
        story_list = await client.request(req)    
          
        # 获取已读剧情集合  
        read_stories = set(story_list.story_id_list) if hasattr(story_list, 'story_id_list') else set()  
        self._log(f"已读剧情数量: {len(read_stories)}")  
            
        # 只有在剧情未读时才读取  
        if 5142700 not in read_stories:    
            req = ArcadeReadStoryRequest()    
            req.story_id = 5142700    
            await client.request(req)    
            self._log("已读取初始剧情 5142700")  
        else:  
            self._log("初始剧情已读,跳过")  
            
        # 获取初始状态      
        await client.request(NbbTopRequest(from_system_id=6001))      
              
        # 第一局游戏      
        data = await client.request(NbbStartRequest(      
            nbb_chara_type=1,      
            difficulty=3,      
            from_system_id=6001      
        ))      
              
        await client.request(NbbFinishRequest(      
            play_id=data.play_id,      
            kill_score=50000,      
            help_bonus=1500,      
            help_list=[2, 3, 1],      
            clear_flg=0,      
            from_system_id=6001      
        ))      
              
        self._log("完成战狼5W任务")      
              
        # 第二局游戏      
        await client.request(NbbTopRequest(from_system_id=6001))      
        data = await client.request(NbbStartRequest(      
            nbb_chara_type=2,      
            difficulty=3,      
            from_system_id=6001      
        ))      
              
        await client.request(NbbFinishRequest(      
            play_id=data.play_id,      
            kill_score=50000,      
            help_bonus=1500,      
            help_list=[2, 3, 1],      
            clear_flg=0,      
            from_system_id=6001      
        ))      
              
        self._log("完成战病5W任务")