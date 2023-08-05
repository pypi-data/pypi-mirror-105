from setuptools import setup, find_packages

setup(
    name="pistarlab-envs-gym-text",
    version="0.0.1-dev",
    author="piSTAR",
    author_email="pistar3.14@gmail.com",
    description="Text games from OpenAI's gym",
    long_description='This is a pistarlab plugin',
    url="https://github.com/pistarlab/pistarlab/plugins",
    license='',
    install_requires=['gym>=0.17.1','gym[box2d]>=0.17.1'],
    package_data={'pistarlab-envs-gym-text': ['README.md',"*.json"]
      },
    packages=find_packages(),
    entry_points={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
)