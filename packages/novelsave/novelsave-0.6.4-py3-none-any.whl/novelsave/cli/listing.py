import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..database import NovelData, UserConfig
from ..exceptions import MissingSource
from ..sources import parse_source
from ..utils.helpers import url_pattern
from ..utils.ui import ConsoleHandler


class CliListing:
    def __init__(self, plain=True, no_input=False):
        self.user = UserConfig.instance()
        self.console = ConsoleHandler(plain, no_input)

    @staticmethod
    def handle(args):
        listing = CliListing(args.plain, args.no_input)

        if args.novel:
            # checks if the provided url is valid
            if not url_pattern.match(args.novel):
                listing.console.error('Provided url is not valid. Please check and try again')
                sys.exit(1)

            if args.reset:
                listing.reset_novel(args.novel, full=False, skip_confirm=args.yes)
            elif args.delete:
                listing.reset_novel(args.novel, full=True, skip_confirm=args.yes)
            else:
                listing.show_novel(args.novel)
        elif args.reset:
            listing.console.error('flag [--reset] must be used along with argument [--novel NOVEL]')
            sys.exit(2)
        elif args.delete:
            listing.console.error('flag [--delete] must be used along with argument [--novel NOVEL]')
            sys.exit(2)
        else:
            listing.show_all()

    def show_all(self):
        sources = self._get_sources()

        for i, key in enumerate(sources.keys()):

            # print the source title
            self.console.info(f'{i}: {key} ({len(sources[key])})')
            for data in sources[key]:
                # prints minimal novel information
                novel = data.novel.parse()
                self.console.info(f'"{novel.title}" by {novel.author}')
                self.console.list(novel.url)

            self.console.newline()

    def show_novel(self, url):
        data, path = self._open(url)
        if data is None:
            return

        # print basic information about novel
        novel = data.novel.parse()
        self.console.info('Information')
        self.console.list('title:', novel.title)
        self.console.list('by:', novel.author)
        self.console.list('synopsis:', novel.synopsis)
        self.console.list('thumbnail:', novel.thumbnail)
        self.console.list('lang:', novel.lang)
        self.console.list('url:', novel.url)
        self.console.newline()

        # print metadata information about novel
        metadata = data.metadata.all()
        self.console.info(f'Metadata ({len(metadata)})')
        for m in metadata:

            # build others to a more readable format
            others = ' '.join([f'[{key}={value}]' for key, value in m['others'].items()])
            if others:
                others = ' ' + others

            self.console.list(f"{m['name']}: {m['value']}{others}")
        self.console.newline()

        # print chapters of the novel
        chapters = data.chapters.all()
        self.console.info(f'Chapters ({len(chapters)})')
        for c in chapters:
            self.console.list(c.title)
        self.console.newline()

    def reset_novel(self, url, full=True, skip_confirm=False):
        data, path = self._open(url, load=False)
        if data is None:
            return

        action = "Delete" if full else "Reset"
        action_working = 'Deleting' if full else 'Resetting'

        # display a minimal number of information
        novel = data.novel.parse()
        self.console.info(f'{action} "{novel.title}"')
        self.console.list(f'by {novel.author}')
        self.console.list(novel.url)
        self.console.newline()

        if not skip_confirm:
            confirm = self.console.confirm('Are you sure?')
            if not confirm:
                self.console.info(f'{action} cancelled by user')
                return

        try:
            with self.console.line(f'{action_working} "{novel.title}", '):
                if full:
                    # database has to be closed before we delete the files associated with it
                    # lest it throw an OSError
                    data.close()

                    # remove everything
                    shutil.rmtree(path)
                else:
                    # remove chapters
                    shutil.rmtree(data.chapters.path)

                    # remove metadata
                    data.metadata.truncate()
        except PermissionError as e:
            self.console.error(str(e))
            sys.exit(1)

    def _get_sources(self) -> Dict[str, List[NovelData]]:
        novels = {}

        novels_path = Path(self.user.directory.get())
        for source in novels_path.iterdir():
            if not source.is_dir():
                continue

            novels[source.name] = []
            for novel in source.iterdir():
                data = NovelData(novel, load_chapters=False)

                # novel is assumed to exist only if url is not None
                if data.novel.get('url') is not None:
                    novels[source.name].append(data)

        return novels

    def _open(self, url: str, load=True) -> Tuple[Optional[NovelData], Optional[Path]]:
        try:
            source = parse_source(url)
        except MissingSource as e:
            self.console.error(str(e))
            sys.exit(1)

        try:
            path = self.user.directory.get() / Path(source.source_folder_name()) / source.novel_folder_name(url)
            data = NovelData(path, should_create=False, load_chapters=load)
        except FileNotFoundError:
            self.console.error('Record of novel does not exist\n')
            sys.exit(1)

        return data, path
