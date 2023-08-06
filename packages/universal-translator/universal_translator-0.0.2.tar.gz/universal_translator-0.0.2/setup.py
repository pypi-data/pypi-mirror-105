from setuptools import setup, find_packages

from universal_translator import __version__, __package_name__, __description__, __repository_url__


setup(
    name=__package_name__,  # Required
    version=__version__,  # Required
    description=__description__,  # Optional
    # long_description='',  # Optional
    # long_description_content_type='text/markdown',  # Optional (see note above)
    url=__repository_url__,  # Optional
    author='Soroush Omranpour',  # Optional
    author_email='soroush.333@gmail.com',  # Optional
    keywords='nlp, universal, translation, multilingual',  # Optional
    packages=['universal_translator', 'universal_translator.modules'],  # Required
    python_requires='>=3.7, <4',
    install_requires=['numpy', 'tqdm', 'json', 'pytorch_lightning', 'pickle', 'pytorch_fast_transformers', 'sentencepiece'],  # Optional
    # license="MIT license",

    project_urls={  # Optional
        'Bug Reports': __repository_url__ + '/issues',
        'Source': __repository_url__,
    },
)