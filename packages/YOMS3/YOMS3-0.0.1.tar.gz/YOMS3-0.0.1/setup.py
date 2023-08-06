
from distutils.core import setup
setup(
  name = 'YOMS3',
  packages = ['YOMS3'],
  version = '0.0.1',
  license='MIT',
  description = 'A PACKAGE TO USE S3 BUCKETS FROM YOM INTEGRATIONS',
  author = 'Camilo Jiménez',
  author_email = 'camilo@youorder.me',
  url = 'https://github.com/user/reponame',
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz', 
  keywords = ['YOM-INTEGRATIONS'],   # Keywords that define your package best
  install_requires=[
    'boto3',
    'botocore',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  python_requires='>=3.6',
)