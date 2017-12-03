import csv

from api.models import Name, Title, KnownFor
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Imports imdb\'s tsv files'

    BATCH_SIZE = 5000
    TITLE_TSV_FIELDS = (
    'tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes',
    'genres')
    NAME_TSV_FIELDS = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles')
    ARRAY_TYPE_FIELDS = ('genres', 'knownForTitles', 'primaryProfession')

    def add_arguments(self, parser):
        parser.add_argument('--titles_path', default='titles.tsv', type=str, help='Path to Titles tsv')
        parser.add_argument('--names_path', default='names.tsv', type=str, help='Path to Names tsv')

    def handle(self, *args, **options):
        """"""
        titles_path = options.get('titles_path')
        names_path = options.get('name_path')

        self.stdout.write('Start processing titles')
        self.process_tsv_file(titles_path, self.process_titles_batch)
        self.stdout.write('Start processing names')
        self.process_tsv_file(names_path, self.process_names_batch)

    def process_tsv_file(self, path, process_lambda):
        """Opens tsv file ."""
        with open(path, 'r') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            tsv_header = next(reader)  # skip header

            batch = []
            count = 0

            for row in reader:
                if len(row) == len(tsv_header):
                    if count >= self.BATCH_SIZE:
                        self.stdout.write(f"Processing {count} batch")
                        process_lambda(batch, tsv_header)
                        batch = []
                        count = 0

                    batch.append(row)
                    count += 1

            if batch:
                process_lambda(batch, tsv_header)

    def process_titles_batch(self, rows, tsv_header):
        titles = map(lambda row: Title(**self.row_to_model(row, self.TITLE_TSV_FIELDS, tsv_header)), rows)
        Title.objects.bulk_create(titles)

    def process_names_batch(self, rows, tsv_header):
        films_lists = []

        def build_name(row):
            attributes = self.row_to_model(row, self.NAME_TSV_FIELDS, tsv_header)
            films_lists.append(Title.objects.filter(tconst__in=attributes.pop('knownForTitles')))

            return Name(**attributes)

        names = list(map(build_name, rows))
        Name.objects.bulk_create(names)

        known_fors = []
        for i, name in enumerate(names):
            for title in films_lists[i]:
                known_fors.append(KnownFor(name=name, title=title))

        KnownFor.objects.bulk_create(known_fors)

    def row_to_model(self, row, model_fields, tsv_header):
        model_args = {}
        for fieldName in model_fields:
            value = row[tsv_header.index(fieldName)]

            if value == '\\N':
                value = None
            if fieldName in self.ARRAY_TYPE_FIELDS:
                if not value:
                    value = []
                else:
                    value = value.split(',')

            model_args[fieldName] = value
        return model_args
