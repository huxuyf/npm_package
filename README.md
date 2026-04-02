在 npmjs.com 上发布一个包，本质上是把你的本地项目通过 npm CLI 发布到 registry。下面是一个完整、规范的流程（适用于绝大多数 Node.js 包发布场景）：



## 一、前置准备

确保你已经安装：

* Node.js（会自带 npm）
* npm CLI（通常随 Node.js 一起安装）

检查版本：

```bash
node -v
npm -v
```



## 二、登录 npm 账号

在终端执行：

```bash
npm login
```

输入：

* username
* password
* email（可能需要验证码）



## 三、创建一个包（项目初始化）

#### 1）新建项目目录

```bash
mkdir my-package
cd my-package
```

#### 2）初始化 package.json

```bash
npm init
```

按提示填写，关键字段：

* `name`：包名（必须全局唯一）
* `version`：版本号（默认 1.0.0）
* `main`：入口文件（如 index.js）



## 四、编写你的代码

例如创建入口文件：

```bash
touch index.js
```

示例内容：

```js
function hello() {
  return "Hello npm!";
}

module.exports = hello;
```



## 五、（重要）检查包名是否可用

```bash
npm view your-package-name
```

如果报错（not found），说明可以用。



## 六、发布前检查

#### 1）查看将被发布的文件

```bash
npm pack
```

或：

```bash
npm publish --dry-run
```

#### 2）控制上传文件（推荐）

使用 `.npmignore` 或 `files` 字段避免上传：

* node_modules
* 测试文件
* 本地配置



## 七、发布包

```bash
npm publish
```

如果是 scoped 包（例如 @yourname/mypkg）：

```bash
npm publish --access public
```



## 八、发布成功后

你可以在 npm 网站看到：

```
https://www.npmjs.com/package/你的包名
```

或者
```
https://app.unpkg.com/你的包名/
```

其他人可以安装：

```bash
npm install your-package-name
```



## 九、更新版本（很重要）

每次更新必须升级版本号，否则无法发布：

```bash
npm version patch   # 修复 bug (1.0.1)
npm version minor   # 新功能 (1.1.0)
npm version major   # 重大更新 (2.0.0)
```

然后重新发布：

```bash
npm publish
```



## 十、常见坑（务必注意）

1. **包名重复**

   * npm 是全局唯一的

2. **忘记改版本号**

   * 会报错：`You cannot publish over the previously published version`

3. **权限问题**

   * scoped 包默认是 private，需要 `--access public`

4. **文件太大或上传多余文件**

   * 用 `.npmignore` 控制


## 十一、通过Github Action自动发布

```bash
npm version patch
git push
git push origin v1.0.1
```
