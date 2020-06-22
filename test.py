import unittest

from youtubelight.channel_info_handler import СhannelInfoHandler
from youtubelight.playlist_handler import PlaylistHandler
from youtubelight.playlist_handler import PlaylistItemHandler
from youtubelight.video_handler import VideoStatisticHandler
from youtubelight.comment_handler import CommentHandler


class YoutubeHandler(unittest.TestCase):

    def setUp(self):
        # need set api key, before run a tests
        self.api_key = ''

    def test_get_channel_info(self):
        obj = СhannelInfoHandler(self.api_key)
        res = obj.get_channel_info_by_name('bbcnews')
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(res['content']['items'][0]['snippet']['title'], 'BBC News')
        res = obj.get_channel_info_by_id('UCsAegdhiYLEoaFGuJFVrqFQ')
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(res['content']['items'][0]['snippet']['title'], 'MotorTrend Channel')

    def test_get_playlist_info(self):
        obj = PlaylistHandler(self.api_key)
        res = obj.get_play_list('UCsAegdhiYLEoaFGuJFVrqFQ')
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(res['content']['pageInfo']['resultsPerPage'], 50)
        res = obj.playlist_next_page()
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(res['content']['pageInfo']['resultsPerPage'], 50)
        res = obj.filter_playlist(res['content']['items'], title='2017 Tuner Battle Week!')
        self.assertEqual(len(res), 26)
        res = obj.get_all_playlists('UC4QobU6STFB0P71PMvOGN5A')
        self.assertEqual(len(res['items']), 1)
        self.assertEqual(len(obj.filter_playlist(res['items'])), 1)

    def test_get_playlist_itm(self):
        obj = PlaylistItemHandler(self.api_key)
        res = obj.get_play_list_itm('PLGvTvFzdMg_OIya3r7lFUJvdvtXSZmdD5', itm_result=30)
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(len(res['content']['items']), 30)
        res = obj.list_itm_next_page()
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(len(res['content']['items']), 30)

    def test_get_video_info(self):
        obj = VideoStatisticHandler(self.api_key)
        res = obj.get_video_info('8IZHDq9SOzM')
        self.assertEqual(len(res['content']['items']), 1)
        res = obj.get_video_info('8IZHDq9SOzM,ogbJT0DHuLI')
        self.assertEqual(len(res['content']['items']), 2)
        res = obj.get_video_info(['8IZHDq9SOzM'])
        self.assertEqual(len(res['content']['items']), 1)
        res = obj.get_video_info(['8IZHDq9SOzM', 'ogbJT0DHuLI'])
        self.assertEqual(len(res['content']['items']), 2)

    def test_get_comment_video_info(self):
        obj = CommentHandler(self.api_key)
        res = obj.get_video_comment('8IZHDq9SOzM')
        self.assertEqual(res.get('status_code'), 200)
        self.assertEqual(len(res['content']['items']), 20)
        res = obj.comments_next_page()
        self.assertEqual(len(res['content']['items']), 20)
        res = obj.filter_comment(res['content'], 'qqqqqqqqq')
        self.assertEqual(len(res), 0)

if __name__ == '__main__':
    unittest.main()
