from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setup(
    name='lminapi',
    version='0.0.3',
    keywords=("APIView", "Validator", "api"),
    description='基于django 和django rest framework整合简化drf APIView视图类常用方法, 简化传入参数已验证方法',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url='https://github.com/lxb0323/lminapi',
    author='bing0323',
    author_email='ltjlxb@163.com',
    packages= find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['django >= 2.0.5','djangorestframework >= 3.11.0'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ]
)