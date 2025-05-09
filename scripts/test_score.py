import json
import pandas as pd
from reasoning_gym.utils import ScoreAnswer

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is a basic JSON-serializable type
        if isinstance(obj, (int, float, str, list, dict, tuple, set, bool)):
            return super().default(obj)
        # For all other types, convert them to string representation
        return str(obj)



#data = pd.read_parquet('data/train.parquet')
# data = pd.read_parquet('data/acre.parquet')
data = pd.read_parquet('data/boxnet.parquet')
# data = pd.read_parquet('data/game_of_life_halting.parquet')
# data = pd.read_parquet('data/modulo_grid.parquet')


sample = data.iloc[0]
task = sample['reward_model']['reasoning_task']
print(sample['prompt'][0]['content'])
entry = sample['reward_model']['entry']
entry_obj = json.loads(entry)
print(task)
print(entry)

answer = """XXXXXXXXXXXXXXXX<answer>A# B# B# A# A# A#</answer>"""

score_answer = ScoreAnswer()
answer = entry_obj['answer']
if answer is None:
    answer = ""
res = score_answer.score_answer(answer, entry, task)
print(res)
answer2 = f'<answer>{answer}</answer>'
res2 = score_answer.score_answer(answer2, entry, task)
print(res2)
answer3 = f'<answer>bla blue</answer>'
res3 = score_answer.score_answer(answer3, entry, task)
print(res3)

# for key in score_answer.datasets:
#     entry = score_answer.datasets[key][0]
#     entry = json.dumps(entry, cls=CustomEncoder)
#     score = score_answer.score_answer(answer, entry, key)
#     print(key, score)


# response = requests.post("http://localhost:8288/score", json={"answer": answer, "entry": entry, "task": task})
# print(response.json())
