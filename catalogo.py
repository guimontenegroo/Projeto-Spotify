from typing import List
from musica import Musica
from propaganda import Propaganda

def catalogo_padrao() -> List[Musica]:
    return [
        Musica("Let Down", "Radiohead", "Alternative Rock", 299),
        Musica("Like a Stone", "Audioslave", "Hard Rock", 294),
        Musica("Hino do Santos", "Santos Futebol Clube", "Hino", 180),
        Musica("Tema do GTA 6", "Rockstar Games", "Trilha Sonora", 210),
        Musica("Billie Jean", "Michael Jackson", "Pop", 294),
        Musica("Largado as Tracas", "Ze Neto & Cristiano", "Sertanejo", 197),
    ]

def propagandas_padrao() -> List[Propaganda]:
    return [
        Propaganda("Assine o Premium e ouca sem anuncios", "Spotify POO", 15),
        Propaganda("Oferta de fim de semana", "Mercado Central", 20),
        Propaganda("Peca ja a sua pizza", "Pizzaria do Ze", 12),
    ]
