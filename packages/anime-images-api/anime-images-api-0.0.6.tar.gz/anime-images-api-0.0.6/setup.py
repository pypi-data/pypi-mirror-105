from setuptools import setup, find_packages
discord_name = 'skelly386#1410'
discord_server_inv = 'https://discord.com/invite/WhnmkwgtGb'


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: Free For Educational Use',
    'License :: Free For Home Use',
    'License :: Free for non-commercial use',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='anime-images-api',
    version='0.0.6',
    description='a wrapper for the anime images api',
    long_description="""import anime_images_api

anime = anime_images_api.Anime_Images()

anime.help()

sfw = anime.get_sfw('hug')

nsfw = anime.get_nsfw('hentai')

print(f'sfw image url: {sfw}')

print(f'nsfw image url: {nsfw}')
""",
    url=discord_server_inv,
    author=discord_name,
    author_email='skellymclane@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['python', 'image', 'anime', 'api', 'wrapper', 'py'],
    packages=find_packages(),
    install_requires=['download', 'rich']
)
