import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Endeless", # Replace with your own username
    version="0.1",
    author="Aurbcd",
    author_email="contact.keyofmagic@gmail.com",
    description="Create playlists with seamless music transitions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aurbcd/Endeless",
    packages=setuptools.find_packages(),
    install_requires=[
        'pydub',
        'librosa',
        'numpy >= 1.17.*',
        'pandas',
        'libfmp',
        'requests',
        'beautifulsoup4',
        'mutagen',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Utilities"
    ],
    package_data={'Endeless': ['songs/*','dataset/*']},


    include_package_data=True,

    python_requires='>=3.8',

    keywords=[
        "music",
        "youtube",
        "mp3",
        "playlist",
        "seamless",
    ],

    entry_points={
        "console_scripts": ["Endeless = Endeless.__main__:console_entry_point"]
    }
)