#!/usr/bin/env -S PYTHONHASHSEED=1 python3
"""Generate a markdown gallery of all available datasets with examples"""

import os
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import json

import reasoning_gym.code.bf
from reasoning_gym.factory import DATASETS, create_dataset

def make_map_fn(split: str):
    """Create a mapping function to process dataset examples.

    Args:
        split: Dataset split name ('train' or 'test')

    Returns:
        Function that processes individual dataset examples
    """
    def process_fn(example: Dict[str, Any], idx: int, task: str) -> Optional[Dict[str, Any]]:
        instruction ="""Let's think step by step and provide the answer in the following format:
<answer>answer here</answer>
Do not explain your reasoning inside the answer tags, provide only the final answer. When an example is provided, you should strictly follow the format of the output/answer in that example."""
        question = example['question']
        question = f"{question} {instruction}"

        data = {
            "data_source": "reasoning_gym",
            "prompt": [{
                "role": "user",
                "content": question
            }],
            "reward_model": {
                "reasoning_task": task,
                "style": "rule",
                "entry": json.dumps(example),
            },
            "extra_info": {
                'split': split,
                'index': idx,
            }
        }
        return data
    return process_fn


def generate_dataset(local_dir: str, data_size: int = 500, train_frac: float = 0.8) -> str:
   # Add examples for each dataset
    train_data: List[Dict[str, Any]] = []
    for i, name in enumerate(sorted(DATASETS.keys())):
        if os.path.exists(os.path.join(local_dir, f'{name}_train.jsonl')):
            print(f"Skipping {name} dataset ({i+1}/{len(DATASETS)})")
            # load train data cache
            with open(os.path.join(local_dir, f'{name}_train.jsonl'), 'r') as f:
                train_data = [json.loads(line) for line in f]
            continue
        print(f"Generating {name} dataset ({i+1}/{len(DATASETS)})")
        if name == 'sokoban':
            size = 100
            dataset = create_dataset(name,size=size, seed=42)
        else:
            size = data_size
            dataset = create_dataset(name,size=size, seed=42)
        train_size = int(size * train_frac)
        split = 'train'
        for i in range(train_size):
            if name == 'sokoban':
                print(f"processing {name} dataset ({i+1}/{size})")
            map_fn = make_map_fn(split)
            train_data.append(map_fn(dataset[i], i, name))
        # save train data cache
        with open(os.path.join(local_dir, f'{name}_train.jsonl.tmp'), 'w') as f:
            for data in train_data:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        split = 'test'
        test_data: List[Dict[str, Any]] = []
        for i in range(train_size, size):
            if name == 'sokoban':
                print(f"processing {name} dataset ({i+1}/{size})")
            map_fn = make_map_fn(split)
            test_data.append(map_fn(dataset[i], i, name))
            test_df = pd.DataFrame(test_data)
            # Option 1: Add a dummy field if metadata is empty
        with open(os.path.join(local_dir, f'{name}_test.jsonl.tmp'), 'w') as f:
            for data in test_data:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        print(f'saving {name} test data to {local_dir}')
        test_df.to_parquet(os.path.join(local_dir, f'{name}.parquet'))
        print(f"{name} test data size:", len(test_data))

    # Save training dataset
    print("train data size:", len(train_data))

    train_df = pd.DataFrame(train_data)
    train_df.to_parquet(os.path.join(local_dir, 'train.parquet'))


def main():
    """Generate gallery markdown file"""
    # Ensure scripts directory exists
    script_dir = Path(__file__).parent
    local_dir = script_dir.parent / "data"
    if not local_dir.exists():
        local_dir.mkdir(parents=True)
    generate_dataset(local_dir, data_size=500, train_frac=0.8)


if __name__ == "__main__":
    main()
