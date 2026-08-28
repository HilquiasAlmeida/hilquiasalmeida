import os
import requests

token = os.getenv("GH_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

# Usando per_page=100 para garantir que traga todos os repositórios (o padrão é 30)
url = "https://api.github.com/users/HilquiasAlmeida/repos?sort=updated&per_page=100"
response = requests.get(url, headers=headers)
repos = response.json()

# Verifica se a API retornou uma lista válida ou um erro
if not isinstance(repos, list):
    print("Erro ao buscar repositórios na API do GitHub:", repos)
    exit(1)

table_content = "| Projeto | Descrição | Linguagem | Atualizado |\n|---|---|---|---|\n"

for repo in repos:
    if not repo.get("fork", False):
        name = repo["name"]
        url = repo["html_url"]
        desc = repo["description"] or "Descrição ainda não informada no repositório."
        lang = repo["language"] or "Não especificada"
        updated = repo["updated_at"].split("T")[0]
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
    print("README atualizado com sucesso!")
else:
    print("Erro: As tags <!-- PROJECTS:START --> ou <!-- PROJECTS:END --> não foram encontradas no README.md")
