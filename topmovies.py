# JOAO PEDRO SIMON FIGUEIRO E RENAN MULLER
import pandas as pd

# Classe para armazenar os filmes
class Movie:
        def __init__(self, id, title, genres, tags, avg_rating, nratings):
            self.id = id
            self.title = title
            self.genres = genres
            self.tags = tags
            self.avg_rating = avg_rating
            self.nratings = nratings

# Classe para armazenar as informacoes de review
class Review:
    def __init__(self, movie, rating):
        self.movie = movie
        self.rating = rating

# Classe para definir uma Ternary Search Tree (TST) e suas operacoes
class TST:
    # Inicializa a TST vazia
    def __init__(self):
        self.root = None

    # Classe interna para representar um no na TST
    class Node:
        def __init__(self, char, left, mid, right, value):
            self.char = char
            self.left = left
            self.mid = mid
            self.right = right
            self.value = value

    # Busca um valor na TST pela chave ou None se ela nao existir
    def get_TST(self, key):
        x = self._get_TST(self.root, key, 0)
        if x is None:
            return None
        return x.value

    # Funcao recursiva auxiliar para buscar na TST
    def _get_TST(self, x, key, d):
        if x is None:
            return None
        c = key[d]
        if c < x.char:
            return self._get_TST(x.left, key, d)
        elif c > x.char:
            return self._get_TST(x.right, key, d)
        elif d < len(key) - 1:
            return self._get_TST(x.mid, key, d + 1)
        else:
            return x
        
    # Insere um valor na TST usando a chave
    def put_TST(self, key, value):
        self.root = self._put_TST(self.root, key, value, 0)

    # Funcao recursiva auxiliar para inserir na TST
    def _put_TST(self, x, key, value, d):
        c = key[d]
        if x is None:
            x = self.Node(c, None, None, None, None)
        if c < x.char:
            x.left = self._put_TST(x.left, key, value, d)
        elif c > x.char:
            x.right = self._put_TST(x.right, key, value, d)
        elif d < len(key) - 1:
            x.mid = self._put_TST(x.mid, key, value, d + 1)
        else:
            x.value = value
        return x
    
    # Busca todas as chaves que comecam com um prefixo
    def keys_with_prefix(self, prefix):
        results = []

        if not prefix:
            return results

        start_node = self._get_TST(self.root, prefix, 0)

        if start_node is None:
            return results 
        if start_node.value is not None:
            results.append(start_node.value)

        self._collect(start_node.mid, prefix, results)
        return results

    # Coleta todas as chaves que comecam com o prefixo a partir de um no
    def _collect(self, x, current_prefix, results):
        if x is None:
            return
        
        self._collect(x.left, current_prefix, results)

        new_prefix = current_prefix + x.char
        if x.value is not None:
            results.append(x.value)

        self._collect(x.mid, new_prefix, results)
        
        self._collect(x.right, current_prefix, results)


# Funcao de hash para calcular o indice na tabla hash
def hash_function(key):
    return key % size

# Funcao para inserir na tabela hash
def insert(key, value):
    index = hash_function(key)
    for pair in hash_table[index]:
        if pair[0] == key:
            pair[1] = value
            return
    hash_table[index].append([key, value])

# Funcao para inserir um filme na tabela hash
def insert_movie(list,row):
    movie_id = (list.loc[row,"movieId"])

    movie = Movie(
        movie_id,
        (list.loc[row,"title"]),
        (list.loc[row,"genres"]).split('|'),
        [],
        notaglobal[movie_id],
        nratings[movie_id]
    )
    insert(movie_id,movie)
    movie_titles.put_TST(movie.title, movie_id)

# Funcao para buscar um valor na tabela hash pela chave
def search(key):
    index = hash_function(key)
    for pair in hash_table[index]:
        if pair[0] == key:
            return pair[1]
    return None


# Funcao para retornar a lista de filmes cujo titulo comeca com uma determinada string
def search_movies_by_prefix(prefix):
    results = movie_titles.keys_with_prefix(prefix)
    for row in range(len(results)):
        results[row] = search(results[row])
    
    # Ordena os filmes por nota global em ordem decrescente usando insertion sort
    for i in range(1, len(results)):
        chave = results[i]
        j = i - 1
        while j >= 0 and (chave.avg_rating > results[j].avg_rating):
            results[j + 1] = results[j]
            j -= 1
        results[j + 1] = chave

    return results

# PESQUISA 1 - prefixo <prefix>
# Dado um prefixo, retorna os filmes cujo titulo comeca com esse prefixo,
# ordenado em ordem decrescente da nota global do filme
def prefixo(prefix):
    array = search_movies_by_prefix(prefix)
    print(f"{'movieID':<6}\t{'title':<80}\t{'genres':<40}\t{'avg_rating':<7}\t{'nratings':<10}")
    for movie in array:
        print(f"{movie.id:<6}\t{movie.title:<80}\t{'|'.join(movie.genres):<40}\t{movie.avg_rating:<7.6f}\t{movie.nratings:<10}")


# Funcao para retornar os 20 melhores filmes de um usuario
def top20user(userId):
    aux = user_ratings[userId]
    for j in range(1,len(aux)):
        chave = aux[j]
        i = j-1
        while i>=0 and (chave[1] > aux[i][1] or (chave[1]==aux[i][1] and chave[2] > aux[i][2])):
            aux[i+1] = aux[i]
            i -= 1
        aux[i+1] = chave
    aux = aux[:20]
    return aux

# PESQUISA 2 - user <userId>
# Dado um userId, retorna os 20 melhores filmes avaliados por esse usuario,
# ordenados pela nota do usuario (primario) e pela nota global do filme (secundario)
def user(userId):
    array = top20user(userId)
    print(f"{'movieID':<6}\t{'title':<80}\t{'genres':<40}\t{'avg_rating':<7}\t{'nratings':<10}\t{'user_rating':<7}")
    for review in array:
        movie = search(review[0])
        print(f"{movie.id:<6}\t{movie.title:<80}\t{'|'.join(movie.genres):<40}\t{movie.avg_rating:<7.6f}\t{movie.nratings:<10}\t{review[1]:<7.6f}")


# Funcao para retornar a lista de filmes de um genero
def search_genre(genre):
    results = movie_genre.get_TST(genre)
    if results is not None:
        return results
    
# Funcao para retornar uma lista com os ids 
# dos N melhores filmes de um genero, 
# considerando apenas filmes com mais de 1000 ratings
# ordenados pela nota global do filme em ordem decrescente
def top_genre(genre,n):
    movies_ids = search_genre(genre)
    genres_to_sort = []
    genres_to_sort_1000 = []
    genres_final = []
    for key in movies_ids:
        genres_to_sort.append((key,search(key).avg_rating,search(key).nratings))
    for aux in genres_to_sort:
        if aux[2] >= 1000:
            genres_to_sort_1000.append(aux)

    aux = genres_to_sort_1000
    for j in range(1,len(aux)):
        chave = aux[j]
        i = j-1
        while i>=0 and chave[1] > aux[i][1]:
            aux[i+1] = aux[i]
            i -= 1
        aux[i+1] = chave

    aux = aux[:n]
    for element in aux:
        genres_final.append(element[0])
    return genres_final

# PESQUISA 3 - top <N> <genre>
# Dado um genero e um numero N, retorna os N melhores filmes desse genero,
# ordenado em ordem decrescente da nota global do filme, 
# considerando apenas filmes com mais de 1000 ratings
def top(n, genre):
    array = top_genre(genre, n)
    print(f"{'movieID':<6}\t{'title':<80}\t{'genres':<40}\t{'avg_rating':<7}\t{'nratings':<10}")
    for number in array:
        movie = search(number)
        print(f"{movie.id:<6}\t{movie.title:<80}\t{'|'.join(movie.genres):<40}\t{movie.avg_rating:<7.6f}\t{movie.nratings:<10}")


# Funcao para retornar a lista de filmes com uma determinada tag
def search_movie_with_tag(tag):
    results = movie_tags.get_TST(tag)
    if results is not None:
        return results
    
# Dada uma lista de tags, retorna a lista de filmes que possuem todas as tags
def intersection_of_tags(list_of_tags):
    if not list_of_tags:
        return []
    
    # Busca os filmes com a primeira tag
    intersection = search_movie_with_tag(list_of_tags[0])
    if intersection is None:
        return []
    
    # Encontra a interseccao dos filmes com as tags restantes
    for tag in list_of_tags[1:]:
        movies_with_tag = search_movie_with_tag(tag)
        if movies_with_tag is None:
            return []
        new_intersection = []
        for movie in intersection:
            if movie in movies_with_tag:
                new_intersection.append(movie)
        intersection = new_intersection
    intersection = [search(movie_id) for movie_id in intersection]

    # Ordena os filmes por nota global em ordem decrescente usando insertion sort
    for i in range(1, len(intersection)):
        chave = intersection[i]
        j = i - 1
        while j >= 0 and (chave.avg_rating > intersection[j].avg_rating):
            intersection[j + 1] = intersection[j]
            j -= 1
        intersection[j + 1] = chave

    return intersection

# PESQUISA 4 - tag <list of tags>
# Dada uma lista de tags, retorna os filmes que possuem todas as tags,
# ordenados pela nota global do filme
def tags(list_of_tags):
    array = intersection_of_tags(list_of_tags)
    print(f"{'movieID':<6}\t{'title':<80}\t{'genres':<40}\t{'avg_rating':<7}\t{'nratings':<10}")
    for movie in array:
        print(f"{movie.id:<6}\t{movie.title:<80}\t{'|'.join(movie.genres):<40}\t{movie.avg_rating:<7.6f}\t{movie.nratings:<10}")


# Funcao principal
if __name__ == '__main__':
    # Tamanhos da tabela hash
    size = 54001
    # Tamanho auxiliar para armazenar filmes e ratings dos usuarios
    sizeaux = 150000 
    
    # Inicializa a tabela hash
    global hash_table
    hash_table = [[] for _ in range(size)]

    # Inicializa as estruturas auxiliares
    filmes = [[0, 0] for _ in range(sizeaux)]
    user_ratings = [[] for _ in range(sizeaux)]
    notaglobal = [0] * sizeaux
    nratings = [0] * sizeaux

    # Inicializa as TST para busca de filmes, tags e gêneros
    global movie_titles
    global movie_tags
    global movie_genre
    movie_titles = TST() 
    movie_tags = TST() 
    movie_genre = TST() 

    # Le as avaliacoes dos usuarios
    ratings = pd.read_csv("ratings.csv") 
    ratings = ratings.drop(columns="date")
    dataratings = ratings.values.tolist()

    # Realiza a soma dos ratings e a contagem de ratings por filme
    for row in dataratings:
        movieId = int(row[1])
        filmes[movieId][0] += float(row[2])
        filmes[movieId][1] += 1

    # Calcula a nota global de cada filme 
    index = 0
    for pair in filmes:
        if pair[1] > 0:
            nratings[index] = pair[1]
            notaglobal[index] = pair[0]/pair[1]
        index += 1

    # Insere os ratings dos usuarios em um vetor
    for row in dataratings:
        movieId = int(row[1])
        user_ratings[int(row[0])].append((movieId,float(row[2]),notaglobal[movieId]))

    # Le os filmes e insere na tabela hash
    # Le os generos dos filmes e os associa aos filmes na TST
    movies = pd.read_csv("movies.csv")
    moviesdata = movies.values.tolist()
    for row in moviesdata:
        genres = row[2].split('|')
        movieId = int(row[0])
        for genre in genres:
            genres_list = movie_genre.get_TST(genre)
            if genres_list is None:
                movie_genre.put_TST(genre,[movieId])
            else:
                if movieId not in genres_list:
                    genres_list.append(movieId)
    for row in range(len(movies)):
        insert_movie(movies, row)

    # Le as tags dos filmes e associa as tags aos filmes na TST
    taglist = pd.read_csv("tags.csv")
    taglist = taglist.drop(columns="timestamp")
    datatags = taglist.values.tolist()
    for row in datatags:
        tag = row[2]
        movieId = int(row[1])
        taglist = movie_tags.get_TST(tag)
        if taglist is None:
            movie_tags.put_TST(tag,[movieId])
        else:
            if movieId not in taglist:
                taglist.append(movieId)

    # Recebe o input do usuario
    while True:
        s = input('\nProxima consulta: ').split(' ')
        try:
            if s[0] == "prefixo":
                prefixo(s[1])
            elif s[0] == "user":
                user(int(s[1]))
            elif s[0].startswith("top"):
                n = int(s[0][3:])
                genre = s[1]
                top(n, genre)
            elif s[0] == "tags":
                tags([tag.strip("'") for tag in s[1:]])
        except Exception as e:
            print(f"Erro: {e}")