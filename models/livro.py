from dataclasses import dataclass, asdict
from datetime import date
from numpy import clip as np_clip # usado no tratamento de avaliação
from util.id_codification import id_encode

# Uso de dataclass para legibilidade extra.
# Lembrando: O Construtor está implícito na dataclass!
@dataclass
class Livro:
    titulo: str
    autor: str
    ano: int
    categoria: str
    lido: bool
    avaliacao: int | None = None
    data_cadastro: str | None = None #recebida em ISO (ou vazio, caso não seja um livro cadastrado anteriormente)
    id: int | None = None

    #######    VALIDAÇÕES/ETC    #######
    def __post_init__(self):
        ## Atributos Obrigatorios ##
        if not (self.titulo and self.autor and self.categoria):
            raise ValueError(f'\nErro fatal na criação do livro "{self.titulo}" ({self.ano}):\nTítulo, autor e categoria são obrigatórios.')

        ### Ano ##
        if self.ano > date.today().year:
            raise ValueError(
                f'\nErro fatal na criação do livro "{self.titulo}" ({self.ano}):\nAno de publicação fornecido ({self.ano}) é um ano futuro.'
                )

        ### Avaliação ###
        if self.lido and self.avaliacao is None: #Livro lido sem avaliação..
            raise ValueError(
                f'\nErro fatal na criação do livro "{self.titulo}" ({self.ano}):\nLivro marcado como lido, mas sem avaliação fornecida.'
                )

        try: #Tratáveis, uso try/except
            if not self.lido and self.avaliacao is not None:
                raise ValueError(f'\nErro na criação do livro "{self.titulo}" ({self.ano}):\nAvaliação não pode ser fornecida á livros não lidos.\nAvaliação será automaticamente mudada para None.')
            if self.lido and not 1 <= self.avaliacao <= 5:
                raise ValueError(f'\nErro na criação do livro "{self.titulo}" ({self.ano}):\nAvaliação fornecida ({self.avaliacao}) está fora do intervalo permitido (1 a 5)\nAvaliação será automaticamente mudada para o valor mais proximo válido.')
        except ValueError as e:
            print(e) #Informa tratamentos
            self.avaliacao = np_clip(self.avaliacao, 1, 5) if self.lido else None

        ### Data de cadastro
        if self.data_cadastro is None: self.data_cadastro = date.today()

        ### ID
        if self.id is None:
            self.id = id_encode(f'{self.titulo}{self.autor}')

    #### Funções
    def to_dict(self):
        '''Obtem o JSON de um livro'''
        livro_dict = asdict(self)
        livro_dict["data_cadastro"] = self.data_cadastro.isoformat()
        del livro_dict["id"]
        return {self.id: livro_dict}

    def __str__(self):
        """String com informação legível sobre o Livro."""
        return f'"{self.titulo}" ({self.ano}), {self.autor}.'


    def __repr__(self):
        """String com informação completa sobre o Livro.
        Escrita em forma da linha de código utilizada para instanciar este livro."""
        return f'Livro(id={self.id}, titulo={self.titulo}, autor={self.autor}, ano={self.ano}, avaliacao={self.avaliacao}, categoria={self.categoria}, lido={self.lido}, data_cadastro={self.data_cadastro})'

    def __eq__(self, outro_livro):
        """Compara o Livro com outro objeto Livro.

        São considerados iguais ao ter os mesmos:
        + Titulo
        + Autor
        + Ano
        """
        if not isinstance(outro_livro, Livro):
            raise TypeError(f'Erro fatal na comparação no livro "{self.titulo}" ({self.ano}):\nNão é possível comparar um objeto Livro com um objeto do tipo{type(outro_livro)}.')

        return self.titulo == outro_livro.titulo and self.autor == outro_livro.autor and self.ano == outro_livro.ano


    #### MÉTODOS DE CLASSE
    @classmethod
    def from_dict(cls, livro_dict):
        """Cria e retorna uma instância de Livro a partir de um dicionário.
        """
        #Converte data
        data_cadastro = livro_dict["data_cadastro"]
        data_cadastro = date.fromisoformat(data_cadastro) if data_cadastro is not None else None
        livro_dict["data_cadastro"] = data_cadastro
        

        return cls(**livro_dict)

