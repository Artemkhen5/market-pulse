import argparse
from pathlib import Path

from market_pulse.ingestion.pipeline import start

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    import_parser = subparsers.add_parser('import')
    import_parser.add_argument(
        '--dataset',
        choices=['orders'],
        required=True,
    )
    import_parser.add_argument(
        '--dataset-dir',
        type=Path,
        default=PROJECT_ROOT / 'data' / 'raw',
    )

    args = parser.parse_args()
    start(args.dataset, args.dataset_dir)


if __name__ == "__main__":
    main()
