import requests


class vkUser:
    def __init__(self, user_id: str = None, user_info: dict = None):
        self.token = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
        self.main_url = 'https://api.vk.com/method/'
        self.vk_url = 'https://vk.com/'
        self.main_params = {
            'access_token': self.token,
            'v': '5.52'
        }
        try:
            if user_info is None:
                url = f'{self.main_url}users.get'
                params = {**self.main_params, **{'fields': 'domain'}}
                if user_id is not None:
                    params.update({'user_ids': user_id})
                response = requests.get(url, params=params)
                code = response.status_code
                if code // 100 == 2:
                    user_info = dict(response.json()['response'][0])
                else:
                    user_info = dict()
                    print(f'Ошибка {code}')
            self.id = user_info['id']
            self.first_name = user_info['first_name']
            self.last_name = user_info['last_name']
            self.domain = user_info['domain']
        except KeyError:
            print('KeyError')
            self.id = None
            self.first_name = ''
            self.last_name = ''
            self.domain = ''

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.vk_url}{self.domain}'

    def __and__(self, other):
        friends_set_1 = self.get_friends()
        friends_set_2 = other.get_friends()
        if friends_set_1 != -1 and friends_set_2 != -1:
            intersection_friends = [
                user1_friend
                for user1_friend in friends_set_1
                for user2_friend in friends_set_2
                if user1_friend.id == user2_friend.id
            ]
            return intersection_friends
        else:
            print('При получении списка друзей произошла ошибка')
            return -1

    def print_user_info(self):
        """Выводит на экран имя, фамилию и ссылку пользователя"""
        print(f'id: {self.id}\n'
              f'Имя: {self.first_name}\n'
              f'Фамилия: {self.last_name}\n'
              f'Ссылка: {self.vk_url}{self.domain}')

    def get_friends(self):
        """Возвращает список друзей пользователя или -1 в случае ошибки запроса к VK API"""
        url = f'{self.main_url}friends.get'
        params = {
            **self.main_params,
            **{
                'user_id': self.id,
                'fields': 'domain'
            }
        }
        response = requests.get(url, params=params)
        code = response.status_code
        if code // 100 == 2:
            try:
                return list(
                    vkUser(user_info=user_info)
                    for user_info in response.json()['response']['items']
                )
            except KeyError:
                return list()
        else:
            print(f'Ошибка {code}')
            return -1

    def print_user_friends_info(self):
        """Выводит на экран список друзей пользователя"""
        dividing_line = '________________________________'
        friends = self.get_friends()
        print(f'Друзья пользователя {self.first_name} {self.last_name}:')
        print(dividing_line)
        if friends != -1:
            for friend in friends:
                friend.print_user_info()
                print(dividing_line)


def main():
    user1 = vkUser()
    user2 = vkUser('551055895')
    intersection_friends = user1 & user2
    print(f'Общие друзья пользователей {user1.first_name} {user1.last_name} и '
          f'{user2.first_name} {user2.last_name}:')
    if len(intersection_friends) == 0:
        print('не найдено')
    else:
        for friend in intersection_friends:
            print(friend)


if __name__ == '__main__':
    main()
