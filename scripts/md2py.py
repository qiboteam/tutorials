import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument(
    "--md_filepath", 
    default="./test_md.md", 
    help="Path to target markdown file", 
    type=str
)

def main(md_filepath):
    """
    Opens a markdown file, collects python code cells in a python script and 
    executes the python script. 
    """

    file = open(md_filepath)
    script_name = f"{str(Path(md_filepath).with_suffix(''))}.py"
    content = file.readlines()

    copying = False

    # collecting python cells into a python script
    with open(f'{script_name}', 'w') as script:
        for i, line in enumerate(content):
        
            if "```python" in line:
                copying = True
                continue

            elif "```" in line:
                copying = False
                continue

            if copying:
                script.write(line)
    
    # executing the python script
    subprocess.call(f'python {script_name}', shell=True)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)