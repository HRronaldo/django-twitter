本项目所使用的box为官方hashicorp/bionic64
可使用vagrant init hashicorp/bionic64命令，会自动在线下载hashicorp/bionic64
然后vagrant up启动
如果在线下载过慢，可直接点击链接下载box到本地
https://app.vagrantup.com/hashicorp/boxes/bionic64/versions/1.0.282/providers/virtualbox.box
然后手动配置：
vagrant init hashicorp/bionic64 {你自己的box所在路径}
ps: hashicorp/bionic64后面跟空格，然后直接跟你的box所在路径，不要加大括号