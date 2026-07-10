import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_PATH = REPO_ROOT / 'huggingface' / 'synthetic-routing-eval' / 'examples.jsonl'
sys.path.insert(0, str(REPO_ROOT / 'lightone_v2_django'))

from lightone.utils.qs_calculator import determine_routing


def test_synthetic_routing_examples_match_product_rule():
    examples = [json.loads(line) for line in EXAMPLES_PATH.read_text(encoding='utf-8').splitlines() if line]

    assert examples
    for example in examples:
        assert example['data_origin'] == 'synthetic'
        assert determine_routing(
            example['qs_score'],
            example['pain_level'],
            safety_flags=example['safety_flags'],
        ) == example['expected_route']


def test_synthetic_routing_examples_exclude_direct_identifiers_and_free_text():
    prohibited_keys = {
        'address',
        'email',
        'image',
        'member_name',
        'note',
        'phone',
        'photo',
        'video',
    }

    for line in EXAMPLES_PATH.read_text(encoding='utf-8').splitlines():
        example = json.loads(line)
        assert prohibited_keys.isdisjoint(example)
