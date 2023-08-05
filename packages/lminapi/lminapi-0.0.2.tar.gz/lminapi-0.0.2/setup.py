from setuptools import setup, find_packages
 
setup(
    name='lminapi',
    version='0.0.2',
    keywords=("APIView", "Validator", "api"),
    description='基于django 和django rest framework整合简化drf APIView视图类常用方法, 简化传入参数已验证方法',
    long_description="整合简化drf APIView视图类常用方法, 简化传入参数已验证方法",
    license="MIT Licence",
    url='https://github.com/lxb0323/lminapi',
    author='bing0323',
    author_email='ltjlxb@163.com',
    packages= find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['django','djangorestframework'],
)