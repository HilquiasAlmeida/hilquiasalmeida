import os
import requests

token = os.getenv("GH_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}
response = requests.get("https://api.github.com/users/HilquiasAlmeida/repos?sort=updated&per_page=100", headers=headers)
repos = response.json()

table_content = "| Projeto | Descrição | Linguagem | Atualizado |\n|---|---|---|---|\n"

for repo in repos:
    if not repo['fork']:
        name = repo['name']
        url = repo['html_url']
        desc = repo['description'] or "Descrição ainda não informada no repositório."
        lang = repo['language'] or "Não especificada"
        updated = repo['updated_at'].split("T")[0]
        table_content += f"| [{name}]({url}) | {desc} | {lang} | {updated} |\n"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start_tag = "<!-- PROJECTS:START -->"
end_tag = "<!-- PROJECTS:END -->"

if start_tag in readme and end_tag in readme:
    start_idx = readme.find(start_tag) + len(start_tag)
    end_idx = readme.find(end_tag)
    new_readme = readme[:start_idx] + "\n" + table_content + "\n" + readme[end_idx:]
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)
