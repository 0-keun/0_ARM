from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['dofbot_pkg'],  # Python 패키지 이름
    package_dir={'': 'scripts'}   # 패키지 디렉토리 경로
)

setup(**d)
