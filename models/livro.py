from dataclasses import dataclass, field, asdict
from datetime import date
from numpy import clip

# Optei por uso de dataclass para dar legibilidade extra á classe, ajudando a manter o código "na linha"
# Lembrando: O Construtor está implícito na dataclass!
@dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    ano: int
    categoria: str
    lido: bool
    avaliacao: int | None = None
    data_cadastro: date = field(default_factory=date.today)

    #######     VALIDAÇÕES    #######
    def __post_init__(self):
        ## Obrigatorias ##
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
            self.avaliacao = clip(self.avaliacao, 1, 5) if self.lido else None


    #### Funções
    def to_dict(self):
        '''Obtem o JSON de um livro'''
        return asdict(self)

    def __str__(self):
        """String com informação legível sobre o objeto Livro."""
        return f'"{self.titulo}" ({self.ano}), {self.autor}.'


    def __repr__(self):
        """String com informação completa sobre o objeto Livro.
        Escrita em forma da linha de código utilizada para instancia este livro."""
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

