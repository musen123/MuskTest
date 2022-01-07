"""
============================
Author:柠檬班-木森
Time:2020/7/16   16:20
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
from setuptools import setup, find_packages

with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='apin',
    version='1.2.0',
    author='MuSen',
    author_email='musen_nmb@qq.com',
    url='https://github.com/musen123/apin',
    description="apin 一个不用写代码的接口自动化测试框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Jinja2==3.0.3",
                      'PyYAML==5.3.1',
                      'requests==2.24.0',
                      'requests-toolbelt==0.9.1',
                      'PyMySQL==1.0.2',
                      'rsa==4.7.2',
                      'jsonpath==0.82',
                      'pyasn1==0.4.8',
                      'colorama==0.4.4',
                      'faker==8.11.0'],

    packages=find_packages(),
    package_data={
        "": ["*.html", "*.md", "*.py", '*.json', "*.yaml"],
    },
    # 指定python版本
    python_requires='>=3.6',

    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    # 安装时生成脚本命令行脚本文件
    entry_points={
        "console_scripts": [
            "apin = apin.manage:main",
        ],
    }
)
