import argparse
import yaml
import json
from dataclasses import dataclass
from pprint import pprint
from datetime import datetime

@dataclass
class Employment():
    title: str
    start: int
    end: int
    location: int
    lineItems: list

def read_config(config_path):
    with open(config_path, 'r') as file:
    #     resume_data = yaml.safe_load(file)
        resume_data = json.load(file)
    return resume_data

def parse_employment(resume_data):
    employment_data = resume_data['employment']
    employment_list = []
    for title, data in employment_data.items():
        print(title)
        employment = Employment(
            title='dffd',
            start=1,
            end=1,
            location=1,
            lineItems=[1,2]
            )
        employment_list.append(employment)
    return employment_list

def main(args):
    config_path = args.config
    config = read_config(config_path)
    employment_list = parse_employment(config)
    print(employment_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    main(args)
