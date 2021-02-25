{
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4-final"
  },
  "orig_nbformat": 2,
  "kernelspec": {
   "name": "python3",
   "display_name": "Python 3",
   "language": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2,
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import mechanicalsoup\n",
    "browser = mechanicalsoup.StatefulBrowser()"
   ]
  },
  {
   "source": [
    "## Trying to Connect"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# USING THE ETL\n",
    "def extract():\n",
    "#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}\n",
    "    url = f'https://myanimelist.net/'\n",
    "    try:\n",
    "        browser.open(url)\n",
    "        soup = browser.get_current_page()\n",
    "    except Exception as e:\n",
    "        print(f'check your internet connection {e}')\n",
    "    return soup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "page = extract()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "bs4.BeautifulSoup"
      ]
     },
     "metadata": {},
     "execution_count": 7
    }
   ],
   "source": [
    "type(page)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "20"
      ]
     },
     "metadata": {},
     "execution_count": 18
    }
   ],
   "source": [
    "divs = page.find_all('li', class_='ranking-unit')\n",
    "\n",
    "len(divs)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [],
   "source": [
    "def transform_soup(div):\n",
    "    title, rank, anime_type, episode_count, rating, members = [], [], [], [], [], []\n",
    "    for item in divs:\n",
    "        rank.append(item.find('span', class_='rank').text.strip())\n",
    "        title .append(item.find('a', class_='title').text.strip())\n",
    "        anime_type.append(item.find('span', class_='info pt8').text.strip().split()[0].replace(',', ''))\n",
    "        episode_count.append(item.find('span', class_='info pt8').text.strip().split()[1])\n",
    "        rating.append(item.find('span', class_='info pt8').text.strip().split()[-1])\n",
    "        members.append(item.find('span', class_='members pb8').text.strip().split()[0])\n",
    "\n",
    "    column_names = ['title', 'rank', 'anime_type', 'episode_count', 'rating', 'members']\n",
    "    data = zip(title, rank, anime_type, episode_count, rating, members)\n",
    "\n",
    "    df = pd.DataFrame(data, columns=column_names)\n",
    "\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "                                               title rank anime_type  \\\n",
       "0               Shingeki no Kyojin: The Final Season    1         TV   \n",
       "1  Re:Zero kara Hajimeru Isekai Seikatsu 2nd Seas...    2         TV   \n",
       "2                                Yuru Camp△ Season 2    3         TV   \n",
       "3                                           Horimiya    4         TV   \n",
       "4                                   Holo no Graffiti    5        ONA   \n",
       "\n",
       "  episode_count rating  members  \n",
       "0            16   9.16  766,370  \n",
       "1            12   8.64  340,872  \n",
       "2            13   8.60  101,386  \n",
       "3            13   8.59  378,402  \n",
       "4             0   8.58   18,167  "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>title</th>\n      <th>rank</th>\n      <th>anime_type</th>\n      <th>episode_count</th>\n      <th>rating</th>\n      <th>members</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>Shingeki no Kyojin: The Final Season</td>\n      <td>1</td>\n      <td>TV</td>\n      <td>16</td>\n      <td>9.16</td>\n      <td>766,370</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>Re:Zero kara Hajimeru Isekai Seikatsu 2nd Seas...</td>\n      <td>2</td>\n      <td>TV</td>\n      <td>12</td>\n      <td>8.64</td>\n      <td>340,872</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>Yuru Camp△ Season 2</td>\n      <td>3</td>\n      <td>TV</td>\n      <td>13</td>\n      <td>8.60</td>\n      <td>101,386</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>Horimiya</td>\n      <td>4</td>\n      <td>TV</td>\n      <td>13</td>\n      <td>8.59</td>\n      <td>378,402</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>Holo no Graffiti</td>\n      <td>5</td>\n      <td>ONA</td>\n      <td>0</td>\n      <td>8.58</td>\n      <td>18,167</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 57
    }
   ],
   "source": [
    "df = transform_soup(divs)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ]
}