#!/usr/bin/env python3
"""Regenerate only Lab 4's deterministic synthetic CSVs; no model or report runs."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    link, paper = 'www.example.com/info', 'your printed handout'
    assert len(link) == len(paper)
    topics = ['Class','Library','Team','Event','Club','Course','Ticket','Account','Delivery','Appointment']
    endings = ['before your visit.','for the latest details.','before the next meeting.','when you have a moment.','before tomorrow morning.']
    for batch in ('reference','current'):
        path = ROOT / f'labs/lab4/data/{batch}_sms.csv'
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf-8',newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['record_id','message'])
            for index in range(200):
                url = index % 10 == 0 if batch == 'reference' else index % 10 < 7
                detail = link if url else paper
                message = f'{topics[index % 10]} update {index+1:03d}: Please check {detail} {endings[(index // 10) % 5]}'
                writer.writerow([f'{batch[:3]}-{index+1:03d}',message])
    print('Generated 200 synthetic reference and current messages with identical length distributions.')


if __name__ == '__main__':
    main()
