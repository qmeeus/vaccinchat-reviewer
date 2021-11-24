import click
import os
import requests
from pathlib import Path
from playsound import playsound
from tempfile import TemporaryDirectory


@click.command()
@click.option("--limit", "-l", type=click.INT, default=100, help="Number of utterances to review")
def review(limit):

    with open(Path(__file__).parent/"labels.txt") as f:
        authorized_labels = list(filter(bool, map(str.strip, f)))

    url = os.environ["API_ROOT"]
    with TemporaryDirectory() as tmpdir:
        auth = (os.environ["API_USER"], os.environ["API_KEY"])
        click.echo(f"{url} {auth}")
        resp = requests.get(f"{url}/review", auth=auth)
        resp.raise_for_status()
        tasks = resp.json()["utterances"][:limit]
        click.echo(f"Start reviewing {len(tasks)} utterances")
        click.echo(f"authorized_labels: {{}}".format(" ".join(authorized_labels)))
        for utt in tasks:
            filename = utt["filename"]
            filepath = f"{tmpdir}/{filename}"
            with open(filepath, "wb") as f:
                f.write(requests.get(f"{url}/download/{filename}", auth=auth).content)
            click.echo("{filename}\nPrediction: {prediction} ({probability:.3%})".format(**utt))
            playsound(filepath)
            value = click.prompt("Is the prediction correct? If not, please input the correct label (default: yes)")
            value = value.strip().lower()
            label = utt["prediction"] if (not(value) or value.startswith("y")) else value
            if label not in authorized_labels:
                raise TypeError("Label is not one of {authorized_labels}")
            requests.put(f"{url}/put", data={"uttid": utt["uttid"], "label": label}, auth=auth)
            click.echo("Review posted!")


