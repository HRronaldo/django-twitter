from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet


# 注意要加 '/' 结尾，要不然会产生 301 redirect
TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'
TWEET_RETRIEVE_API = '/api/tweets/{}/'


class TweetApiTests(TestCase):

    def setUp(self):

        self.user1 = self.createUser('user1', 'user1@jiuzhang.com')
        self.tweets1 = [
            self.createTweet(self.user1)
            for i in range(3)
        ] 
        self.user1_client = APIClient(enforce_csrf_checks=True)
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.createUser('user2', 'user2@jiuzhang.com')
        self.tweets2 = [
            self.createTweet(self.user2)
            for i in range(2)
        ]

    def test_list_api(self):
        # 必须带user_id
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # 正常request
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user2.id})
        self.assertEqual(len(response.data['tweets']), 2)
        # 检测排序是按照新创建的在前面的顺序来的
        self.assertEqual(response.data['tweets'][0]['id'], self.tweets2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweets2[0].id)

    def test_create_api(self):
        # 必须登录
        response = self.anonymous_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 403)

        # 必须带content
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)

        # 不能为空
        response = self.user1_client.post(TWEET_CREATE_API, {'content': ''})
        self.assertEqual(response.status_code, 400)

        # content不能过长
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # 正常发帖
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': 'Hello World, this is my first tweet!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)        

    def test_retrieve(self):
        # tweet with id=-1 does not exist
        url = TWEET_RETRIEVE_API.format(-1)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 404)

        # 获取某个tweet 的时候会一起把comments 也拿下
        tweet = self.createTweet(self.user1)
        url = TWEET_RETRIEVE_API.format(tweet.id)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['comments']), 0)

        self.createComment(self.user2, tweet, 'holly s***')
        self.createComment(self.user1, tweet, 'hmm...')
        response = self.anonymous_client.get(url)
        self.assertEqual(len(response.data['comments']), 2)

        # tweet 里包含用户的头像和昵称
        profile = self.user1.profile
        self.assertEqual(response.data['user']['nickname'], profile.nickname)
        self.assertEqual(response.data['user']['avatar_url'], None)
        # <HOMEWORK> 补充 Unit tests 来测试 comments, likes 里的 user 如期望的返回
