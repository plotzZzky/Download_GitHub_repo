import requests
from pathlib import Path
import shutil
import art


class Downloader:
    def __init__(self):
        self.folder_path = None
        self.user = ''
        self.repos = None

    def wellcome(self):
        art.tprint('  GitHub Download', 'tarty2')
        print(f"{'_' * 20}Projeto feito por um estudante python{'_' * 20}")
        print(f"{' ' * 68}@plotzZzky\n")
        self.find_user()

    def find_user(self):
        self.user = input('Digite o nome do usuario do GitHub:\n')
        repos_link = f'https://api.github.com/users/{self.user}/repos?'
        result = requests.get(repos_link)
        self.repos = result.json()
        if result.status_code == 200:
            print('Usuario encontrado...')
            self.menu()
        else:
            print(f'Usuario {self.user} não encontrado! Tente novamente.')
            self.find_user()

    def menu(self):
        print(f'1- Baixar todos os projetos de {self.user}'
              f'\n2- Baixar projeto especifico')
        option = input(f'Digite uma opcao:\n')
        self.check_option(option)

    def check_option(self, option):
        if option == '1':
            self.find_all_repos()
        elif option == '2':
            self.show_all_repos()
        else:
            print('Opcao incorreta!')
            self.menu()

    def show_all_repos(self):
        n = 1
        print('')
        for repo in self.repos:
            print(f"{n}- {repo['full_name']}")
            n += 1
        self.find_single_repo()

    # Procura o repositorio especifico do usuario:
    def find_single_repo(self):
        option = int(input('\nDigite o repositorio escolhido:\n')) - 1
        if option <= len(self.repos):
            self.create_path()
            item = self.repos[option]['full_name']
            self.search_project(item)
        else:
            print('Opcão incorreta')
            self.find_single_repo()

    def create_path(self):
        home = Path.home()
        self.folder_path = Path(f'{home}/GitHub_Projects/{self.user}')
        self.folder_path.mkdir(parents=True, exist_ok=True)

    # Procura a lista com todos os repositorios do usuario:
    def find_all_repos(self):
        self.create_path()
        for item in self.repos:
            self.search_project(item['full_name'])

    def search_project(self, item):
        url = f'https://github.com/{item}/archive/refs/heads/master.zip'
        project_name = item.split('/')[1]
        file_name = f'{project_name}.zip'
        self.download_project(url, file_name, project_name)

    def download_project(self, url, file_name, project_name):
        r = requests.get(url, file_name)
        print(f'Baixando {project_name} aguarde...')
        file = f'{self.folder_path}/{file_name}'
        open(file, "wb").write(r.content)
        self.extract_project(file, project_name)

    def extract_project(self, file, project_name):
        shutil.unpack_archive(file, self.folder_path)
        print(f'Download {project_name} concluido.')


downloader = Downloader()
downloader.wellcome()
