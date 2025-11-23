from pathlib import Path
import json

class History:
    HISTORY_LEN = 3
    HISTORY_PATH = '.config/animeworld/'
    HISTORY_FILENAME = 'history.json'

    def __init__(self):
        self.path =  Path.home() / ".config" / "animeworld"
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / self.HISTORY_FILENAME
        self.history_data = []
            
        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")
        
        try:
            self.history_data = json.loads(self.file.read_text(encoding="UTF-8"))
        except json.JSONDecodeError:
            print('» Error while reading history')
            self.history_data = []
            self.file.write_text("[]", encoding="utf-8")
        
        print(self.history_data)

    def save(self, anime_data):
        if(len(self.history_data)) == 3:
            self.history_data.pop(0)
        
        self.history_data.append(anime_data)
        self.file.write_text(
            json.dumps(self.history_data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def get(self):
        return self.history_data[-1]

    def delete(self):
        return

