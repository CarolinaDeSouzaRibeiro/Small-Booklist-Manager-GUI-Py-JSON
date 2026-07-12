from dataclasses import dataclass, field
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