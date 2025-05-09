import json
import pandas as pd
from reasoning_gym.utils import ScoreAnswer

data = pd.read_parquet('data/train.parquet')

sample = data.iloc[0]
task = sample['reward_model']['reasoning_task']
print(sample['prompt'][0]['content'])
entry = sample['reward_model']['entry']
print(task)
print(entry)

answer = """XXXXXXXXXXXXXXXX<answer>A# B# B# A# A# A#</answer>"""

score_answer = ScoreAnswer()
for key in score_answer.datasets:
    entry = score_answer.datasets[key][0]
    entry = json.dumps(entry)
    score = score_answer.score_answer(answer, entry, key)
    print(key, score)


# response = requests.post("http://localhost:8288/score", json={"answer": answer, "entry": entry, "task": task})
# print(response.json())