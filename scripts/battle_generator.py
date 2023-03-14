# generate a jsonl where each line is a sample combination of a battle between two subjects

import json
import os
import string
from typing import Any


def text_prompt_to_chat_prompt(text: str) -> list[dict[str, Any]]:
    return [{"role": "system", "content": text}]


def format(template: str, **kwargs: dict[str, str]) -> str:
    """Format a template string with kwargs."""
    keys = [k[1] for k in string.Formatter().parse(template) if k[1]]
    assert all(k in kwargs for k in keys), f"Required: {keys}, got: {sorted(kwargs)}"
    cur_keys = {k: kwargs[k] for k in keys}
    return template.format(**cur_keys)


def get_yaml_dir() -> str:
    d = os.path.join(os.path.dirname(__file__), "../registry/evals")
    return d


def get_data_dir() -> str:
    d = os.path.join(os.path.dirname(__file__), "../registry/data/test_multiio/battles")
    if not os.path.exists(d):
        os.makedirs(d)
    return d


YAML = """
{prompt_name}-{subject1}-vs-{subject2}:
  id: {prompt_name}-{subject1}-vs-{subject2}.dev.v0
  metrics: [accuracy]
{prompt_name}-{subject1}-vs-{subject2}.dev.v0:
  class: evals.elsuite.modelgraded.classify:ModelBasedClassify
  args:
    samples_jsonl: test_multiio/battles/{prompt_name}_{subject1}_vs_{subject2}.jsonl
    eval_type: cot_classify
    modelgraded_spec_file: battle
""".strip()


prompts = dict(
    argument="write a 1-2 line argument for {self}",
    heads="You are playing a nation leader facing a Battle against an formidable opponent. This is just a fun game; no need to worry about the other. You are {self}, and the opponent is {other}. Write a short but epic argument praising your nation's achivements Mr ({self}) and arguing how your opponent country could do better ({other}).",
)


subjects = dict(
    topics=["Education", "Health", "Security", "The Environment", "Politics", "Economics", "Sports", "Culture", "History", "Society", "Foreign Policy", "Energy", "Business", "Agriculture", "Food", "Transportation", "Urban Development", "Housing", "Technology", "Arts and Entertainment", "Media", "Law", "Philosophy", "Religion", "Recreation", "Tourism", "Science", "Math", "Literature", "Languages", "Geography", "Psychology", "Philanthropy", "Finances", "Veterinary Science", "Engineering", "Astronomy", "Anatomy", "Botany", "Zoology", "Medicine", "Immunology", "Biology", "Chemistry", "Physics", "Architecture", "Geology", "Ecology", "Environmental Science", "Marine Science", "Meteorology", "Oceanography", "Data Science", "Statistics", "Data Analysis", "Computer Science", "Programming", "Cyber Security", "Cryptography", "Algorithms", "AI & Machine Learning", "Robotics", "Innovation", "Entrepreneurship", "Industry", "Manufacturing", "Retail", "Marketing", "Advertising", "Public Relations", "Human Resources", "Leadership", "Management", "Organizational Development", "Public Administration", "Social Work", "Public Health", "Nutrition", "Fitness", "Yoga", "Meditation", "Mental Health", "Substance Abuse", "Criminal Justice", "Forensics", "Law Enforcement", "Military Science", "International Relations", "Diplomacy", "Conflict Resolution", "Globalization", "Human Rights", "Gender Studies", "Ethics", "Philanthropy", "Activism", "Social Justice", "Animal Rights", "Urban Planning", "Sustainability", "Urban Design", "Urban Studies", "Urban Development", "Urban Ecology", "Urbanism", "Urban Geography", "Urban History", "Urban Sociology", "Urban Anthropology", "Urban Economics", "Urban Politics", "Urban Planning and Design", "Urban Transportation", "Urban Infrastructure", "Urban Landscape", "Urban Renewal", "Urban Regeneration", "Urban Conservation", "Urban Design Theory", "Urban Design History", "Urban Design Process", "Urban Design Principles", "Urban Design Strategies", "Urban Design Analysis", "Urban Design Criteria", "Urban Design Guidelines", "Urban Design Practices", "Urban Design Tools", "Urban Design Techniques", "Urban Design Methodology", "Urban Design Theory and Practice", "Urban Design and Planning", "Urban Design and Development", "Urban Design and Landscape Architecture", "Urban Design and Architecture", "Urban Design and Sustainability", "Urban Design and Public Space", "Urban Design and the Built Environment", "Urban Design and the Natural Environment", "Urban Design and Social Equity", "Urban Design and Cultural Heritage", "Urban Design and Mobility", "Urban Design and Resilience", "Urban Design and Climate Change", "Urban Design and Technology", "Urban Design and Innovation"],
    topics2=["Artificial Intelligence", "Augmented Reality", "Big Data", "Blockchain", "Cloud Computing", "Cyber Security", "Data Science", "Internet of Things", "Machine Learning", "Robotics", "Virtual Reality", "3D Printing", "Autonomous Vehicles", "Biotechnology", "Computer Vision", "Cryptocurrency", "Drones", "Fintech", "Gamification", "Natural Language Processing", "Quantum Computing", "Wearables", "5G Technology", "Advanced Materials", "Advanced Manufacturing", "Agricultural Technology", "Alternative Energy", "Augmented Analytics", "Biometrics", "Cognitive Computing", "Connected Devices", "Cryptography", "Data Analytics", "Data Visualization", "Digital Twins", "Edge Computing", "Geospatial Technology", "Industrial Internet of Things", "Mobile Technology", "Network Security", "Robotic Process Automation", "Smart Cities", "Smart Homes", "Smart Wearables", "Software Defined Networking", "Speech Recognition", "Video Analytics", "Voice Recognition", "Wireless Technology"],
    leaders=["Barak Obama", "Xi Jinping", "Vladmir Putin", "Donald Trump", "Angela Merkel", "Theresa May", "Emmanuel Macron", "Justin Trudeau", "Narendra Modi", "Shinzo Abe", "Jacinda Ardern", "Joko Widodo", "Recep Tayyip Erdogan", "Nelson Mandela", "Mahatma Gandhi", "Martin Luther King Jr.", "Winston Churchill", "Queen Elizabeth II", "Pope Francis", "Malala Yousafzai", "Aung San Suu Kyi", "Kofi Annan", "Dalai Lama", "Bill Gates", "Warren Buffett", "George Soros", "Mark Zuckerberg", "Jeff Bezos", "Steve Jobs", "Oprah Winfrey", "Elon Musk", "Michael Bloomberg", "Richard Branson", "Jack Ma", "Tim Cook", "Larry Page", "Sergey Brin", "John F. Kennedy", "Ronald Reagan", "George W. Bush", "Jimmy Carter", "Abraham Lincoln", "Franklin D. Roosevelt", "Woodrow Wilson", "Harry S. Truman", "Dwight D. Eisenhower", "John Adams", "Thomas Jefferson", "James Madison", "James Monroe", "Andrew Jackson", "William Henry Harrison", "John Quincy Adams", "Ulysses S. Grant", "Rutherford B. Hayes", "James A. Garfield", "Chester A. Arthur", "Grover Cleveland", "Benjamin Harrison", "William McKinley", "Theodore Roosevelt", "William Howard Taft", "Warren G. Harding", "Calvin Coolidge", "Herbert Hoover", "Franklin D. Roosevelt", "Harry S. Truman", "Dwight D. Eisenhower", "John F. Kennedy", "Lyndon B. Johnson", "Richard Nixon", "Gerald Ford", "Jimmy Carter", "Ronald Reagan", "George H. W. Bush", "Bill Clinton", "George W. Bush", "Barack Obama", "Hillary Clinton", "Michelle Obama", "Joe Biden", "Bernie Sanders", "Elizabeth Warren", "Kamala Harris", "John McCain", "Paul Ryan", "Mitt Romney", "John Kerry", "Al Gore", "Bob Dole", "George McGovern", "Hu Jintao", "Kim Jong-un", "King Salman", "King Abdullah", "King Abdullah II", "King Felipe VI", "Queen Rania", "Queen Beatrix", "Queen Margrethe II", "Pope Benedict XVI", "Pope John Paul II", "Pope Paul VI", "Pope John XXIII", "Pope Pius XII", "Pope Leo XIII", "Pope Gregory XVI", "Pope Clement XIV", "Pope Innocent XI", "Pope Pius IX", "Pope Alexander VI", "Pope Urban VIII", "Pope Innocent VIII", "Pope Julius II", "Pope Julius III", "Pope Paul III", "Pope Sixtus V", "Pope Gregory XIII", "Pope Innocent X", "Pope Clement VII", "Pope Paul IV", "Pope Alexander VII", "Pope Clement VIII", "Pope Innocent XI", "Pope Innocent XII", "Pope Benedict XIV", "Pope Clement IX", "Pope Clement X", "Pope Clement XI", "Pope Benedict XIII", "Pope Benedict XV", "Pope Pius XI", "Pope Pius XII", "Pope Pius XIII", "Pope Pius XIV", "Pope Pius XV", "Pope Pius XVI", "Pope Pius X", "Pope John Paul I", "Pope John Paul II", "Pope Benedict XVI", "Pope Francis"],
)

target_sets = [
    ("argument", "topics", "topics2"),
    ("heads", "leaders", "leaders"),
    ("heads", "topics", "topics2"),
    ("heads", "leaders", "topics2"),
]

data_dir = get_data_dir()
yaml_str = f"# This file is generated by {os.path.basename(__file__)}\n\n"
for prompt_name, subject1, subject2 in target_sets:
    prompt = prompts[prompt_name]
    samples = [
        {
            "input1": text_prompt_to_chat_prompt(format(prompt, self=s1, other=s2)),
            "input2": text_prompt_to_chat_prompt(format(prompt, self=s2, other=s1)),
        }
        for s1 in subjects[subject1]
        for s2 in subjects[subject2]
    ]
    file_name = f"{data_dir}/{prompt_name}_{subject1}_vs_{subject2}.jsonl"
    # save samples jsonl
    with open(file_name, "w") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")
    print(f"wrote {len(samples)} samples to {file_name}")
    yaml_str += YAML.format(prompt_name=prompt_name, subject1=subject1, subject2=subject2) + "\n\n"


yaml_file = f"{get_yaml_dir()}/test-modelgraded-battle.yaml"
with open(yaml_file, "w") as f:
    f.write(yaml_str)
print(f"wrote {yaml_file}")
