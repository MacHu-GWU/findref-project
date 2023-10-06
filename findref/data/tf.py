# -*- coding: utf-8 -*-

import typing as T
import os
import shutil
import subprocess
import dataclasses

try:
    import markdown
except ImportError:
    import sys
    from pathlib import Path

    bin_python = Path(sys.executable)
    bin_pip = bin_python.parent.joinpath("pip")
    subprocess.run([f"{bin_pip}", "install", "markdown>=3.0.1,<4.0.0"])
    subprocess.run(
        [f"{bin_pip}", "install", "markdown-full-yaml-metadata>=2.0.0,<3.0.0"]
    )
    import markdown

import sayt.api as sayt
import afwf_shell.api as afwf_shell

from ..paths import dir_findref_home
from ..os_platform import IS_WINDOWS
from ..utils import preprocess_query


DATASET_NAME = "tf"

_dir_home = dir_findref_home.joinpath(DATASET_NAME)
_dir_home.mkdir(parents=True, exist_ok=True)

dir_index = _dir_home.joinpath(".index")
dir_cache = _dir_home.joinpath(".cache")
dir_git_repos = _dir_home.joinpath("git_repos")
dir_git_repos.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Provider:
    provider_name: str
    provider_short_name: str
    repo_name: str

    @property
    def dir_repo(self):
        return dir_git_repos.joinpath(self.repo_name)


PROVIDERS = [
    Provider(
        provider_name="AWS",
        provider_short_name="aws",
        repo_name="terraform-provider-aws",
    ),
    Provider(
        provider_name="azurerm",
        provider_short_name="AZ",
        repo_name="terraform-provider-azurerm",
    ),
    Provider(
        provider_name="google",
        provider_short_name="GCP",
        repo_name="terraform-provider-google",
    ),
]

provider_short_name_to_provider_name = {
    provider.provider_short_name: provider.provider_name for provider in PROVIDERS
}


@dataclasses.dataclass
class ItemType:
    item_type: str
    folder_name: str
    url_key: str


ITEM_TYPES = [
    ItemType(
        item_type="Res",
        folder_name="r",
        url_key="resources",
    ),
    ItemType(
        item_type="DS",
        folder_name="d",
        url_key="data-sources",
    ),
]

item_type_to_url_key = {
    item_type.item_type: item_type.url_key for item_type in ITEM_TYPES
}


def git_clone(repo_name: str):
    cwd = os.getcwd()
    os.chdir(str(dir_git_repos))
    print("Please wait, we have to clone git repos to get the terraform docs data ...")
    url = f"https://github.com/hashicorp/{repo_name}"
    subprocess.run(["git", "clone", "--depth", "1", url])
    os.chdir(cwd)


def clone_all_repos_again(skip_if_exists: bool = False):
    """
    Clean up existing git repos (if exists), and clone all repos again.

    :param skip_if_exists: If True, skip cloning if the repo already exists.
    """
    for provider in PROVIDERS:
        dir_repo = dir_git_repos.joinpath(provider.repo_name)
        if skip_if_exists:
            if dir_repo.exists():
                continue
            else:
                git_clone(provider.repo_name)
        else:
            if dir_repo.exists():
                shutil.rmtree(dir_repo)
            git_clone(provider.repo_name)


@dataclasses.dataclass
class Record:
    provider: str  # provider short name aws (Amazone Web Service), az (Azure), gcp (Google Cloud Platform)
    type: str  # res (resource), ds (dataset)
    subcategory: str  # S3, IAM, etc
    item_name: str  # s3_bucket, iam_role, etc
    description: str


def extract_record_for_provider(provider: Provider) -> T.List[Record]:
    md = markdown.Markdown(extensions=["full_yaml_metadata"])
    records = list()
    for item_type in ITEM_TYPES:
        markdown_dir = provider.dir_repo / "website" / "docs" / item_type.folder_name
        for p in markdown_dir.glob("**/*.markdown"):
            item_name = p.name.split(".")[0]
            content = p.read_text()
            md.convert(content)
            subcategory = md.Meta["subcategory"]
            description = md.Meta["description"]
            record = Record(
                provider=provider.provider_short_name,
                type=item_type.item_type,
                subcategory=subcategory,
                item_name=item_name,
                description=description,
            )
            records.append(record)
    return records


def downloader() -> T.List[T.Dict[str, T.Any]]:
    records = list()
    for provider in PROVIDERS:
        records.extend(
            [
                dataclasses.asdict(record)
                for record in extract_record_for_provider(provider)
            ]
        )
    return records


def cache_key_def(
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
):
    return ["findref-tf"]


def extractor(
    record: sayt.T_RECORD,
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
) -> sayt.T_RECORD:
    doc = {
        "provider": record["provider"],
        "type": record["type"],
        "cate": record["subcategory"],
        "cate_ng": record["subcategory"],
        "item": record["item_name"],
        "item_ng": record["item_name"],
        "desc": record["description"],
    }
    return doc


fields = [
    sayt.KeywordField(
        name="provider",
        stored=True,
        lowercase=True,
    ),
    sayt.KeywordField(
        name="type",
        stored=True,
        lowercase=True,
    ),
    sayt.TextField(
        name="cate",
        stored=True,
    ),
    sayt.TextField(
        name="item",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="cate_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.NgramWordsField(
        name="item_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.StoredField(
        name="desc",
    ),
]


dataset = sayt.RefreshableDataSet(
    downloader=downloader,
    cache_key_def=cache_key_def,
    extractor=extractor,
    fields=fields,
    dir_index=dir_index,
    dir_cache=dir_cache,
    cache_expire=365 * 24 * 3600,
)


@dataclasses.dataclass
class Item(afwf_shell.Item):
    def enter_handler(self):
        if IS_WINDOWS:
            subprocess.run(["start", self.arg], shell=True)
        else:
            subprocess.run(["open", self.arg])


def search(query: str) -> T.List[Item]:
    query = preprocess_query(query)

    docs = dataset.search(
        download_kwargs={},
        query=query,
        limit=50,
        simple_response=True,
    )
    return [
        Item(
            uid="{provider} {item_type}: {subcategory} | {item_name}".format(
                provider=doc["provider"],
                item_type=doc["type"],
                subcategory=doc["cate"],
                item_name=doc["item"],
            ),
            title="{provider} {item_type}: {subcategory} | {item_name}".format(
                provider=doc["provider"],
                item_type=doc["type"],
                subcategory=doc["cate"],
                item_name=doc["item"],
            ),
            subtitle=doc["desc"],
            arg="https://registry.terraform.io/providers/hashicorp/{provider}/latest/docs/{url_key}/{item_name}".format(
                provider=provider_short_name_to_provider_name[doc["provider"]],
                url_key=item_type_to_url_key[doc["type"]],
                item_name=doc["item"],
            ),
            autocomplete="{} {} {} {}".format(
                doc["provider"],
                doc["type"],
                doc["cate"],
                doc["item"],
            ),
            variables=doc,
        )
        for doc in docs
    ]


def handler(query: str, ui: afwf_shell.UI):
    if dir_index.exists() is False:
        items = [
            Item(
                uid="uid",
                title="Creating index, it may takes 1-2 minutes ...",
                subtitle="please wait, don't press any key",
            )
        ]
        ui.print_items(items=items)

        items = search(query)
        ui.move_to_end()
        ui.clear_items()
        ui.clear_query()
        ui.print_query()
        return items

    return search(query)


def main():
    clone_all_repos_again(skip_if_exists=True)
    afwf_shell.debugger.enable()
    afwf_shell.debugger.path_log_txt.unlink(missing_ok=True)
    ui = afwf_shell.UI(handler=handler)
    ui.run()
