# Shell

本人日常开发时，为解决某些需求而开发的脚本/应用/工具集合。

## App list

| Application Name                 | Usage                                                        |
| -------------------------------- | ------------------------------------------------------------ |
| clipboard_translator(构思、设计) | 1. 修改 `conf/setting.yaml` 编辑 translator.engine.<br/>2. 从 alternative 中选一个翻译引擎，赋值给 active.<br/>3. 也可以不对 active 赋值，按自己想法排序 alternative.<br/>4. 删除 `conf/.secret.yaml.template` 后缀，修改 yaml.<br/>5. 修改翻译引擎项，填入其 api 要求的 id, key...<br/>--------------配置完毕------------<br/>6. 复制需要翻译的文本到剪切板，例如 PDF.<br/>7. 执行程序，自动翻译剪切板内容.<br/>8. 翻译完毕，生成 doc 保存到临时目录并自动打开。 |
|                                  |                                                              |
|                                  |                                                              |



## *Todo list*

- [ ] 实现 彩云小译 Translator，通过单元测试。
- [ ] 按照 clipboard_translator 构思与设计，完成开发。
