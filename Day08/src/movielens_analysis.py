#!/usr/bin/env python3

import sys
import os
from bs4 import BeautifulSoup
import requests
import collections
import functools
import datetime
import re
import pytest

class Ratings:
    def __init__(self, filepath):
        self.data_path = filepath
        self.data = self.read_data()

    def read_data(self):
        p_data = []
        try :
            with open(self.data_path) as f:
                next(f)
                for line in f:
                    u_Id, m_Id, rating, timestamp = line.strip().split(',')
                    p_data.append({"u_Id": int(u_Id), "m_Id": int(m_Id), "rating": float(rating), "timestamp": int(timestamp)})
        except FileNotFoundError:
            print(f"Ratings filename: '{self.data_path}' not found")
        except Exception as e:
            print(f"Exception in reading rating: ' {e} '")
        return p_data
    
    class Movies:
        def __init__(self, outer):
            self.data = outer.data
        
        def dist_by_year(self):
            years = [datetime.datetime.fromtimestamp(line["timestamp"]).year for line in self.data]
            years_cnt = collections.Counter(years)
            return dict(sorted(years_cnt.items()))
        
        def dist_by_rating(self):
            r_cnt = collections.Counter(line["rating"] for line in self.data)
            return dict(sorted(r_cnt.items()))
        
        def top_by_num_of_ratings(self, n):
            m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
            m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
            ratings_cnt = collections.Counter([m_map[line["m_Id"]] for line in self.data])
            return dict(ratings_cnt.most_common(n))
        
        def top_by_ratings(self, n, metric="average"):
            try:
                metric = metric.lower()
                if metric not in ["average", "median"]:
                    raise AttributeError(f"Unknown metric: '{metric}', available options: 'average|median' ")
                
                m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
                m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
                mp_rat = collections.defaultdict(list)
                for line in self.data:
                    mp_rat[m_map[line["m_Id"]]].append(line["rating"])
                
                for key in mp_rat:
                    if metric == "average":
                        mp_rat[key] = sum(mp_rat[key]) / len(mp_rat[key])
                    else:
                        line_rates = sorted(mp_rat[key])
                        r_len = len(line_rates)
                        mp_rat[key] = line_rates[r_len // 2] if r_len % 2 else (line_rates[r_len // 2] + line_rates[r_len // 2 - 1]) / 2
                    mp_rat[key] = round(mp_rat[key], 2)

                return dict(sorted(mp_rat.items(), key=lambda x: -x[1]))
            except Exception as e:
                print(f"Exception ' {e} '")

        def top_controversial(self, n):
            m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
            m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
            mp_rat = collections.defaultdict(list)
            for line in self.data:
                mp_rat[m_map[line["m_Id"]]].append(line["rating"])
            
            for key in mp_rat:
                mean = sum(mp_rat[key]) / len(mp_rat[key])
                variance = sum((mean - x) ** 2 for x in mp_rat[key]) / len(mp_rat[key])
                mp_rat[key] = round(variance, 2)
            
            return dict(sorted(mp_rat.items(), key=lambda x: -x[1])[:n])
        
    class Users:
        def __init__(self, outer):
            self.data = outer.data

        def dist_by_num_of_ratings(self):
            u_cnt = collections.Counter(line["u_Id"] for line in self.data)
            return dict(sorted(u_cnt.items(), key=lambda x: -x[1]))

        def dist_by_ratings(self, metric='average'):
            try:
                metric = metric.lower()
                if metric not in ["average", "median"]:
                    raise AttributeError(f"Unknown metric: '{metric}', available options: 'average|median' ")

                mp_rat = collections.defaultdict(list)

                for line in self.data:
                    mp_rat[line["u_Id"]].append((line["rating"]))

                user_ratings = {}
                for user_id, ratings_list in mp_rat.items():
                    
                    if metric == "average":
                        user_ratings[user_id] = sum(ratings_list) / len(ratings_list)
                    else:
                        line_rates = sorted(ratings_list)
                        r_len = len(line_rates)
                        user_ratings[user_id] = line_rates[r_len // 2] if r_len % 2 else (line_rates[r_len // 2] + line_rates[r_len // 2 - 1]) / 2
                    
                    user_ratings[user_id] = round(user_ratings[user_id], 2)

                return dict(sorted(user_ratings.items(), key=lambda x: -x[1]))
            except Exception as e:
                print(f"Exception ' {e} '")
        
        def top_by_variance(self, n):
            user_ratings = collections.defaultdict(list)
            
            for rating_record in self.data:
                user_id = rating_record["u_Id"]
                rating = rating_record["rating"]
                user_ratings[user_id].append(rating)
            
            user_variances = {}
            for user_id, ratings in user_ratings.items():
                if len(ratings) > 1:
                    mean = sum(ratings) / len(ratings)
                    variance = sum((mean - x) ** 2 for x in ratings) / len(ratings)
                    user_variances[user_id] = round(variance, 2)
                else:
                    user_variances[user_id] = 0.0 
            
            sorted_users = sorted(user_variances.items(), key=lambda x: x[1], reverse=True)

            return dict(sorted_users[:n])

class Movies:
    def __init__(self, filepath):
        self.data_path = filepath
        self.data = self.read_data()
    
    def read_data(self):
        p_data = []
        try:
            with open(self.data_path) as f:
                next(f)
                for line in f:
                    f_line = line.strip().split(',')
                    m_Id = f_line[0]
                    genres = f_line[-1].split('|')
                    title = ','.join(f_line[1:-1])
                    year = re.search(r"\(([0-9]{4})\)", title)
                    year = int(year.group(1)) if year else "Unknown"
                    p_data.append({"m_Id": int(m_Id), "title": title, "year": year, "genres": genres})
        except FileNotFoundError:
            print(f"Movies filename: '{self.data_path}' not found")
        except Exception as e:
            print(f"Exception: ' {e} '")
        return p_data
    
    def dist_by_release(self):
        year_cnt = collections.Counter([line["year"] for line in self.data])
        return dict(sorted(year_cnt.items(), key=lambda x: -x[1]))
    
    def dist_by_genres(self):
        genres_cnt = collections.Counter([genre for line in self.data for genre in line["genres"]])
        return dict(sorted(genres_cnt.items(), key=lambda x: -x[1]))
    
    def most_genres(self, n):
        return dict(sorted([(line["title"], len(line["genres"])) for line in self.data], key=lambda x: -x[1])[:n])


class Links:
    def __init__(self, filename):
        self.data_path = filename
        self.data = self.read_data()
        self.l_map = self.l_map_create()

    def read_data(self):
        p_data = []
        try:
            with open(self.data_path) as f:
                next(f)
                for line in f:
                    m_id, imdb_id, tmdb_id = line.strip().split(',')
                    p_data.append({"m_id":m_id, "imdb_id":imdb_id, "tmdb_id":tmdb_id})
        except FileNotFoundError:
            print(f"Links filename: '{self.data_path}' not found")
        except Exception as e:
            print(f"Exception: '{e}' ")
        return p_data
    
    def l_map_create(self):
        return {line["m_id"]: line["imdb_id"] for line in self.data}

    def get_imdb(self, list_of_movies, list_of_fields):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}

            def get_director(soup: BeautifulSoup):
                try:
                    return soup.find("li", {"data-testid": "title-pc-principal-credit"}).find(string="Director").find_next("a").get_text(strip=True)
                except AttributeError:
                    return "Not found"
                
            def get_runtime(soup: BeautifulSoup):
                try:
                    return soup.find("li", {"data-testid": "title-techspec_runtime"}).find_next("div").get_text(strip=True)
                except AttributeError:
                    return "Not found"
                
            def get_budget(soup: BeautifulSoup):
                try:
                    return soup.find("li", {"data-testid": "title-boxoffice-budget"}).find_next("span", {"class": "ipc-metadata-list-item__list-content-item"}).get_text(strip=True)
                except AttributeError:
                    return "Not found"
                
            def get_gross(soup: BeautifulSoup):
                try:
                    return soup.find("li", {"data-testid": "title-boxoffice-cumulativeworldwidegross"}).find_next("span", {"class": "ipc-metadata-list-item__list-content-item"}).get_text(strip=True)
                except AttributeError:
                    return "Not found"
                
            f_map = {
                "director": get_director,
                "runtime": get_runtime,
                "budget": get_budget,
                "cumulative worldwide gross": get_gross,         
            }

            ans = []

            for m_id in list_of_movies:
                imdb_id = self.l_map[str(m_id)]
                line = [m_id]
                response =  requests.get(f"https://www.imdb.com/title/tt{imdb_id}", headers=headers)
                if response.status_code != requests.codes.ok:
                    raise Exception(f"Request isn't successful, status code: '{response.status_code}' ")
                soup = BeautifulSoup(response.text, "html.parser")
                for field in list_of_fields:
                    field = field.lower()
                    line.append(f_map[field](soup))
                ans.append(line)

            return ans
        except KeyError as e:
            print(f"Invalid field to parse or m_id not found: '{e}' ")
        except Exception as e:
            print(f"Exception: '{e}' ")

    def top_directors(self, n):
        list_of_movies = [line["m_id"] for line in self.data]
        r_data = self.get_imdb(list_of_movies, ["Director"])
        directors = [line[1] for line in r_data]
        d_cnt = collections.Counter(directors)
        # if "Not found" in d_cnt:
        #     d_cnt.pop("Not found")
        return dict(d_cnt.most_common(n))

    def most_expensive(self, n):
        list_of_movies = [line["m_id"] for line in self.data]
        r_data = dict(self.get_imdb(list_of_movies, ["Budget"]))
        
        m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
        m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
        f_data = {}
        for key in r_data:
            f_data[m_map[int(key)]] = r_data[key]

        for key in f_data:
            num = 0
            for ch in f_data[key]:
                if ch.isdigit():
                    num = num * 10 + int(ch)
            f_data[key] = num
        return dict(sorted(f_data.items(), key=lambda x:-x[1])[:n])
    
    def most_profitable(self, n):
        list_of_movies = [line["m_id"] for line in self.data]
        r_data = self.get_imdb(list_of_movies, ["Budget", "cumulative worldwide gross"])
        
        m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
        m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
        f_data = {}
        for line in r_data:
            line[0] = m_map[int(line[0])]

            budget_atoi = 0
            for ch in line[1]:
                if ch.isdigit():
                    budget_atoi = budget_atoi * 10 + int(ch)
            line[1] = budget_atoi

            gross_atoi = 0
            for ch in line[2]:
                if ch.isdigit():
                    gross_atoi = gross_atoi * 10 + int(ch)
            line[2] = gross_atoi
            f_data[line[0]] = line[2] - line[1]

        return dict(sorted(f_data.items(), key=lambda x: -x[1])[:n])
    
    def longest(self, n):
        list_of_movies = [line["m_id"] for line in self.data]
        r_data = self.get_imdb(list_of_movies, ["Runtime"])
        
        m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
        m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
        for line in r_data:
            line[0] = m_map[int(line[0])]

            t_in_mnts = 0
            tmp = 0
            for ch in line[1]:
                if ch.isdigit():
                    tmp = tmp * 10 + int(ch)
                elif ch == 'h':
                    t_in_mnts += tmp * 60
                    tmp = 0
            t_in_mnts += tmp
            line[1] = t_in_mnts
        
        return dict(sorted(r_data, key=lambda x:-x[1])[:n])
            
    def top_cost_per_minute(self, n):
        list_of_movies = [line["m_id"] for line in self.data]
        r_data = self.get_imdb(list_of_movies, ["Runtime", "budget"])
        
        m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))
        m_map = {line["m_Id"]: line["title"] for line in m_instance.data}
        
        f_data = {}
        for line in r_data:
            line[0] = m_map[int(line[0])]
            
            try :
                t_in_mnts = 0
                tmp = 0
                for ch in line[1]:
                    if ch.isdigit():
                        tmp = tmp * 10 + int(ch)
                    elif ch == 'h':
                        t_in_mnts += tmp * 60
                        tmp = 0
                t_in_mnts += tmp
                line[1] = t_in_mnts
                if not line[1]:
                    raise AttributeError("Runtime not found, calculation aborted")   
            except AttributeError as e:
                print(f"Exception: '{e}' ") 

            budget_atoi = 0
            for ch in line[2]:
                if ch.isdigit():
                    budget_atoi = budget_atoi * 10 + int(ch)
            line[2] = budget_atoi

            f_data[line[0]] = line[2] / line[1]
        
        return dict(sorted(f_data.items(), key=lambda x: -x[1])[:n])


class Tags:

    def __init__(self, filepath):
        self.data_path = filepath
        self.data = self.read_data()

    def read_data(self):
        p_data = []
        try:
            with open(self.data_path) as f:
                next(f)
                for line in f:
                    u_id, m_id, tag, timestamp = line.strip().split(',')
                    p_data.append({"u_id": int(u_id), "m_id": int(m_id), "tag": tag, "timestamp": int(timestamp)})
        except FileNotFoundError:
            print(f"Ratings filename: '{self.data_path}' not found")
        except Exception as e:
            print(f"Exception in reading rating: ' {e} '")
        return p_data
    
    def most_words(self, n):
        res = {line["tag"]: len(line["tag"].split()) for line in self.data}
        return dict(sorted(res.items(), key=lambda x: -x[1])[:n]) 
    
    def longest(self, n):
        res = {line["tag"]: len(line["tag"]) for line in self.data}
        res = dict(sorted(res.items(), key=lambda x: -x[1])[:n])
        return list(res.keys())

    def most_words_and_longest(self, n):
        d_words = set(self.most_words(n))
        d_longest = set(self.longest(n))
        return list(d_words.intersection(d_longest))

    def most_popular(self, n):
        res = [line["tag"].lower() for line in self.data]
        return dict(collections.Counter(res).most_common(n))
    
    def tags_with(self, word):
        res = set(line["tag"] for line in self.data if word.lower() in line["tag"].lower().split())
        return sorted(list(res))


class Tests:
    
    class TestRating:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.r_instance = Ratings(os.path.join(os.path.dirname(__file__), "ml-latest-small/ratings.csv"))

        def test_rating_01(self):
            assert list(self.r_instance.data[0].keys()) == ["u_Id", "m_Id", "rating", "timestamp"]

        def test_rating_02(self, capsys):
            Ratings(os.path.join(os.path.dirname(__file__), "ml-latest-small/ratings.cs"))
            captured = capsys.readouterr()
            assert "not found" in captured.out 

        def test_rating_03(self):
            m_inner_instance = self.r_instance.Movies(self.r_instance)
            assert sorted(list(m_inner_instance.dist_by_year().keys())) == list(m_inner_instance.dist_by_year().keys())

        def test_rating_04(self):
            m_inner_instance = self.r_instance.Movies(self.r_instance)
            assert sorted(list(m_inner_instance.dist_by_rating().keys())) == list(m_inner_instance.dist_by_rating().keys())

        def test_rating_05(self):
            res = self.r_instance.Movies(self.r_instance).top_by_num_of_ratings(100)
            assert isinstance(res, dict)
            assert sorted(list(res.values()), key=lambda x: -x) == list(res.values())

        def test_rating_06(self):
            res = self.r_instance.Movies(self.r_instance).top_by_ratings(100, "average")
            assert isinstance(res, dict)
            assert sorted(list(res.values()), key=lambda x: -x) == list(res.values())

        def test_rating_07(self):
            res = self.r_instance.Movies(self.r_instance).top_by_ratings(100, "median")
            assert isinstance(res, dict)
            assert sorted(list(res.values()), key=lambda x: -x) == list(res.values())

        def test_rating_08(self):
            res = self.r_instance.Movies(self.r_instance).top_controversial(100)
            assert isinstance(res, dict)
            assert sorted(list(res.values()), key=lambda x: -x) == list(res.values())

        def test_rating_09(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.dist_by_num_of_ratings()
            assert isinstance(result, dict)
            assert all(isinstance(k, int) for k in result.keys())
            assert all(isinstance(v, int) for v in result.values())

        def test_rating_10(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.dist_by_num_of_ratings()
            values = list(result.values())
            assert sorted(values, reverse=True) == values

        def test_rating_11(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.dist_by_ratings("average")
            assert isinstance(result, dict)
            assert all(isinstance(v, float) for v in result.values())

        def test_rating_12(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.dist_by_ratings("median")
            assert isinstance(result, dict)
            assert all(isinstance(v, float) for v in result.values())

        def test_rating_13(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.dist_by_ratings("average")
            values = list(result.values())
            assert sorted(values, reverse=True) == values

        def test_rating_14(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.top_by_variance(5)
            assert isinstance(result, dict)
            assert len(result) <= 5
            assert all(isinstance(v, float) for v in result.values())

        def test_rating_15(self):
            u_inner_instance = self.r_instance.Users(self.r_instance)
            result = u_inner_instance.top_by_variance(5)
            values = list(result.values())
            assert sorted(values, reverse=True) == values



    class TestMovies:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.m_instance = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))

        def test_movies_01(self):
            assert isinstance(self.m_instance.data, list)
            assert isinstance(self.m_instance.data[0], dict)
            assert list(self.m_instance.data[0].keys()) == ["m_Id", "title", "year", "genres"]

        def test_movies_02(self, capsys):
            Movies("xyz")
            captured = capsys.readouterr()
            assert "not found" in captured.out

        def test_movies_03(self):
            res = self.m_instance.dist_by_release()
            assert isinstance(res, dict)
            assert list(res.values()) == sorted(list(res.values()), reverse=True)

        def test_movies_04(self):
            res = self.m_instance.dist_by_genres()
            assert isinstance(res, dict)
            assert sorted(list(res.values()), reverse=True) == list(res.values())
        
        def test_movies_05(self):
            res = self.m_instance.most_genres(25)
            assert isinstance(res, dict)
            assert sorted(list(res.values()), reverse=True) == list(res.values())


    class TestTags:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.t_instance = Tags(os.path.join(os.path.dirname(__file__), "ml-latest-small/tags.csv"))

        def test_tags_01(self):
            assert isinstance(self.t_instance.data, list)
            assert isinstance(self.t_instance.data[0], dict)
            assert list(self.t_instance.data[0].keys()) == ["u_id", "m_id", "tag", "timestamp"]

        def test_tags_02(self, capsys):
            Tags("xyz")
            captured = capsys.readouterr()
            assert "not found" in captured.out

        def test_tags_03(self):
            res = self.t_instance.most_words(100)
            assert isinstance(self.t_instance.data, list)
            assert isinstance(self.t_instance.data[0], dict)
            assert len(res) == 100
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_tags_04(self):
            res = self.t_instance.longest(100)
            assert isinstance(self.t_instance.data, list)
            assert len(res) == 100
        
        def test_tags_05(self):
            res = self.t_instance.most_words_and_longest(100)
            assert isinstance(self.t_instance.data, list)

        def test_tags_06(self):
            res = self.t_instance.most_popular(100)
            assert isinstance(self.t_instance.data, list)
            assert isinstance(self.t_instance.data[0], dict)
            assert len(res) == 100
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_tags_07(self):
            res = self.t_instance.tags_with("netflix")
            assert isinstance(res, list)
            assert len(res) != 0
            assert "netflix" in res[0].lower()


    class TestLinks:
        @pytest.fixture(autouse=True)
        def setup(self):
            in_f = os.path.join(os.path.dirname(__file__), "ml-latest-small/links.csv")
            out_f = os.path.join(os.path.dirname(__file__), "sample_data.csv")
            self.list_of_movies = []
            with open(in_f) as input_f, open(out_f, "w") as output_f:
                output_f.write("movieId,imdbId,tmdbId\n")
                lines = input_f.readlines()
                for i in range(1, 6):
                    output_f.write(lines[i])
                    self.list_of_movies.append(str(i))

            self.l_instance = Links(os.path.join(os.path.dirname(__file__), "sample_data.csv"))
        
        def test_links_01(self):
            assert isinstance(self.l_instance.data, list)
            assert isinstance(self.l_instance.data[0], dict)
            assert list(self.l_instance.data[0].keys()) == ["m_id", "imdb_id", "tmdb_id"]

        def test_links_02(self, capsys):
            Links("xyz")
            captured = capsys.readouterr()
            assert "not found" in captured.out

        def test_links_03(self):
            res = self.l_instance.get_imdb(self.list_of_movies, ["director", "RUnTIme", "BUdget", "cumulative worldwide gross"])
            assert isinstance(res, list)
            assert isinstance(res[0], list)
            assert len(res[0]) == 5
            assert len(res) == 5

        def test_links_04(self):
            res = self.l_instance.top_directors(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_links_05(self):
            res = self.l_instance.most_expensive(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_links_06(self):
            res = self.l_instance.most_profitable(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_links_07(self):
            res = self.l_instance.most_profitable(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_links_08(self):
            res = self.l_instance.longest(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())

        def test_links_09(self):
            res = self.l_instance.top_cost_per_minute(5)
            assert isinstance(res, dict)
            assert len(res) == 5
            assert sorted(list(res.values()), reverse=True) == list(res.values())


if __name__ == '__main__':
    pytest.main([__file__, "-v"])

