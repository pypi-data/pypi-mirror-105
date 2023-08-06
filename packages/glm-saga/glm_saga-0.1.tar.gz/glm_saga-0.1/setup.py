from setuptools import find_packages, setup

setup(
    name='glm_saga',
    version='0.1',
    description="A PyTorch solver for elastic net",
    author='Eric Wong',
    author_email='wongeric@mit.edu',
    platforms=['any'],
    license="MIT",
    url='https://github.com/madrylab/glm_saga',
    packages=['glm_saga'],
    install_requires=[
        'torch>=1.0'
    ]
)