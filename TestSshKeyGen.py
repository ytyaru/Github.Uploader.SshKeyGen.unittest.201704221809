import unittest
from SshKeyGen import SshKeyGen
import os
class TestSshKeyGen(unittest.TestCase):
    def test_GenerateAndGet(self):
        g = SshKeyGen()
        username = 'user0'
        type = 'rsa'
        bits = '4096'
        passphrase = ''
        comment = '{0}@mail.com'.format(username)
        file_path = '/tmp/{type}_{bits}_{username}'.format(type=type, bits=bits, username=username)
        # Generate()テスト
        stdout = g.Generate(type=type, bits=bits, passphrase=passphrase, comment=comment, file_path=file_path)
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(os.path.isfile(file_path + '.pub'))
        self.assertTrue(0 < len(stdout))
        # GetTypeAndBit()テスト
        data = g.GetTypeAndBit(file_path)
        self.assertTrue('type' in data.keys())
        self.assertTrue('bits' in data.keys())
        self.assertEqual(type, data['type'])
        self.assertEqual(bits, data['bits'])
        # 後始末
        os.remove(file_path)
        os.remove(file_path + '.pub')
    def test_CheckSshConnect(self):
        # ********* このテストはアカウント所有者でないと成功しない *********
        # アカウントとそのSSH秘密鍵を公開しない限りテスト成功しないと思う。
        # * GitHubに所定のアカウントが登録されていること
        # * GitHubに所定のSSH公開鍵が設定されていること
        # * テスト実行PCの~/.ssh/configに所定のHost設定があること
        # * Host設定にあるSSH鍵ファイルが存在すること(GitHubに設定した鍵と同一であること)
        g = SshKeyGen()
        self.assertTrue(g.CheckSshConnect('github.com.ytyaru', 'ytyaru'))
    def test_CheckSshConnect_Error(self):
        g = SshKeyGen()
        host = '非存在Host名'
        username = '任意GitHubユーザ名'
        with self.assertRaises(Exception) as e:
            g.CheckSshConnect(host, username)
            self.assertTrue(e.msg.startswith('SSH接続に失敗しました。接続できているのに失敗と判断する場合があります。このSSH接続確認はsshコマンドの標準出力値で行っているため、その出力値が開発した時点から変更されていると誤って失敗と判断してしまいます。sshコマンド出力値(英語)から目視で判断してください。出力値: '))
            # 出力値: ssh: Could not resolve hostname \351\235\236\345\255\230\345\234\250host\345\220\215: Name or service not known
            # 出力値以降はsshコマンドの領分なのでテストしない。
