import click
import requests_html

@click.command()
@click.option('--year', type=int, help='The year of the proceedings to download.', default=2016)
@click.option('--path', type=str, default="data/download/neurips/{year}.txt", help='The path to save the proceedings to.')
def download(year: int, path: str = "data/download/neurips/{year}.txt") -> None:
    """Download the proceedings for a given year.

    Args:
        year: The year of the proceedings to download.
        path: The path to save the proceedings to. If None, the proceedings will
            be saved to the current working directory.
    """
    url = f'https://proceedings.neurips.cc/paper_files/paper/{year}'
    session = requests_html.HTMLSession()
    response = session.get(url)
    response.raise_for_status()
    paper_titles = list(map(
        lambda tag: tag.text,
        response.html.xpath('//a[@title="paper title"]')
    ))
    session.close()

    path = path.format(year=year) if path=="data/download/neurips/{year}.txt" else path
    with open(path, 'w') as f:
        f.write('\n'.join(paper_titles))

if __name__ == '__main__':
    download()