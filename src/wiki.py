from bs4 import BeautifulSoup as bs
import re, json, requests

class wiki:
    """wikipeida 크롤링"""

    def __init__(self, series:str):
        self.root = 'https://en.wikipedia.org/wiki/'
        game_info = []
        
        soup = self.get_page_source(self.root+series)
        game_list = self.get_game_list(soup)
        for game in game_list:
            game_info.append(self.game_detail(title=game[0], url=game[1]))
        
        with open(f'wiki_{series}.json', 'w') as json_file:
            json.dump(game_info, json_file, indent=4)

    def get_page_source(self, url:str)->bs:
        soup = bs(requests.get(url).text, 'html.parser')
        return soup
    
    def get_game_list(self, soup:bs)->list:
        result = []

        game_table= soup.find('table', {'class':'wikitable'}).find_all('i')

        for game in game_table:
            
            try:
                title = game.find('a')['title']
                url = game.find('a')['href'].replace('/wiki/', '')
                temp = [title,url]
                result.append(temp)

            except:
                pass

        return result
    
    def game_detail(self, url:str, title:str)->dict:
        """wikipedia get game info

        Args:
            url (str): wikipedia in game url → /game title
            title (str): wikipedia in game title → game title

        Returns:
            dict: game details info list retren
        """
        page = self.get_page_source(self.root+url)
        start_tag = page.find(attrs={'id': 'Plot'})
        end_tag = page.find(attrs={'id': 'Development'})
        
        result_dict = {}
        current_key = title
        
        next_element = start_tag.find_next()
        current_key = title
        while next_element != end_tag:
            if 'mw-headline' in next_element.get('class', []):
                current_key = next_element.text
            elif next_element.name == 'p':
                if current_key is not None:
                    text = re.sub(r'\[\d+\]', '', next_element.text)
                    if current_key in result_dict:
                        result_dict[current_key].append(text)
                    else:
                        result_dict[current_key] = [text]
            next_element = next_element.find_next()

        return result_dict

if __name__ == '__main__':
    wiki('Assassin\'s_Creed')

