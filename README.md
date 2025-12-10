# python3-samples
python3.10.x 案例源码

#添加图片模块
pip install Pillow


```shell
# 创建用户组
sudo groupadd <gourpname>
# 添加当前用户进组
sudo usermod -aG <groupname> $(whoami)

 创建 sudoers 文件
echo '%nopasswd ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/nopasswd

# 重新登录或刷新组信息
newgrp <用户组名>
groups $(whoami)
```

```shell
# 1. 创建组
sudo groupadd nopasswd

# 2. 添加当前用户进组
sudo usermod -aG nopasswd $(whoami)

# 3. 创建 sudoers 文件
echo '%nopasswd ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/nopasswd

# 4. 确保权限正确（必须是 440）
sudo chmod 440 /etc/sudoers.d/nopasswd

# 5. 验证语法
sudo visudo -c

# 6. 重新登录或刷新组信息
newgrp nopasswd

# 7. 测试免密是否成功
sudo ls /

```