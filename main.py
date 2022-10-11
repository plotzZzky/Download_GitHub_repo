import requests
from pathlib import Path
import shutil
import art
import sys
import subprocess


class Downloader:
    def __init__(self):
        self.folder_path = None
        self.user = None
        self.repos = None
        self.downloaded_repos = []

    def wellcome(self):
        art.tprint(f'{" " * 17}GitHub Download', 'tarty2')
        print(f"{'_' * 26}Projeto feito por um estudante python{'_' * 26}")
        print(f"{' ' * 31}https://github.com/plotzZzky\n")
        self.get_user()

    def get_user(self):
        name = input('Digite o nome do usuario do GitHub:\n')
        self.find_user(name)

    def find_user(self, user):
        repos_link = f'https://api.github.com/users/{user}/repos?'
        result = requests.get(repos_link)
        if result.status_code == 200:
            self.user = user
            self.repos = result.json()
            print('Usuario encontrado...\n')
            self.menu()
        else:
            print(f'Usuario {user} não encontrado! Tente novamente.')
            self.get_user()

    def menu(self):
        print(f"{'-' * 36} Menu {'-' * 36}")
        print(f'1- Baixar todos os projetos de {self.user}\n'
              f'2- Baixar projeto especifico\n'
              f'3- Executar projeto\n')
        option = input(f'Digite uma opcao:\n')
        self.check_option(option)

    def check_option(self, option):
        if option == '1':
            self.find_all_repos()
        elif option == '2':
            self.show_all_repos()
        elif option == '3':
            self.run_menu()
        else:
            print('Opcao incorreta!')
            self.menu()

    def show_all_repos(self):
        n = 1
        print('')
        if self.repos is None:
            print('Nenhum repositorio encontrado!')
            self.menu()
        else:
            for repo in self.repos:
                project_name = repo['full_name'].split('/')[1]
                print(f"{n}- {project_name}")
                n += 1
            self.find_single_repo()

    # Procura o repositorio especifico do usuario:
    def find_single_repo(self):
        option = int(input('\nDigite o repositorio escolhido:\n')) - 1
        if option <= len(self.repos):
            self.create_path()
            item = self.repos[option]['full_name']
            self.search_project(item)
            self.menu()
        else:
            print('Opcão incorreta')
            self.show_all_repos()

    def create_path(self):
        home = Path.home()
        self.folder_path = Path(f'{home}/GitHub_Projects/{self.user}')
        self.folder_path.mkdir(parents=True, exist_ok=True)

    # Procura a lista com todos os repositorios do usuario:
    def find_all_repos(self):
        self.create_path()
        if self.repos is None:
            print('Nenhum repositorio encontrado!')
            self.menu()
        else:
            for item in self.repos:
                self.search_project(item['full_name'])
        self.menu()

    def search_project(self, item):
        try:
            url = f'https://github.com/{item}/archive/refs/heads/master.zip'
            project_name = item.split('/')[1]
            file_name = f'{project_name}.zip'
            self.download_project(url, file_name, project_name)
        except FileNotFoundError:
            self.menu()
        except IndexError:
            self.menu()

    def download_project(self, url, file_name, project_name):
        try:
            r = requests.get(url, file_name)
            if r.status_code == 200:
                print(f'Baixando {project_name} aguarde...')
                file = f'{self.folder_path}/{file_name}'
                open(file, "wb").write(r.content)
                self.downloaded_repos.append(project_name)
                self.extract_project(file, project_name)
            else:
                print(f"Erro de conexao - {r.status_code}")
                self.menu()
        except Exception as e:
            print(e)
            self.menu()

    def extract_project(self, file, project_name):
        try:
            shutil.unpack_archive(file, self.folder_path)
            print(f'Download {project_name} concluido.\n')
        except FileNotFoundError:
            self.menu()

    def run_menu(self):
        while True:
            try:
                if self.downloaded_repos:
                    n = 1
                    for repo in self.downloaded_repos:
                        print(f"{n}- {repo}")
                        n += 1
                else:
                    print('Voce precisa baixar os projetos primeiro.')
                    self.menu()
                option = input("digite o numero da opcao ou 'x' para menu inicial:\n")
                if option == 'x':
                    self.menu()
                elif int(option) <= len(self.repos):
                    project = self.downloaded_repos[int(option) - 1]
                    self.run_project(project)
                    self.run_menu()
                else:
                    print('Opcao invalida.')
                    self.run_menu()
            except ValueError:
                print('O valor deve ser um numero')
                self.run_menu()

    def run_project(self, project):
        try:
            folder = f"{self.folder_path}/{project}-master/"
            if sys.platform == 'linux':
                self.run_on_linux(folder)
            elif sys.platform == 'win32':
                self.run_on_windows(folder)
            elif sys.platform == 'darwin':
                print('Não há suporte a OSx no momento, desculpe :(')
                self.menu()
        except Exception as e:
            print(e)
            self.run_menu()

    @staticmethod
    def run_on_linux(folder):
        terminal = input('Digite o comando para o seu terminal:\n'
                         'ex: gnome-terminal, xfce4-terminal, konsole...\n')
        subprocess.call([f"{terminal}", "-x", "sh", "-c", f"cd {folder}; python3 -m venv venv; "
                         "source venv/bin/activate; pip install -r requirements.txt; python main.py"])

    @staticmethod
    def run_on_windows(folder):
        subprocess.call(f'start powershell ; cd {folder}; python -m venv venv; venv\Scripts\Activate.ps1;'
                        'pip install -r requirements.txt; python -m main.py', shell=True)


downloader = Downloader()
if __name__ == '__main__':
    downloader.wellcome()
