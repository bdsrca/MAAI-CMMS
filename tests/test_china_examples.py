import unittest

from maai_cmms_demo.china_cases import load_china_examples, rank_by_mas_fit, summarize_top_examples


class ChinaExamplesTests(unittest.TestCase):
    def test_china_examples_are_cited_and_scored(self) -> None:
        examples = load_china_examples()
        self.assertGreaterEqual(len(examples), 6)
        for example in examples:
            self.assertTrue(example.sources)
            self.assertTrue(all(source.startswith("http") for source in example.sources))
            self.assertEqual(len(example.scores), 5)
            self.assertGreaterEqual(min(example.scores), 1)
            self.assertLessEqual(max(example.scores), 5)

    def test_rank_by_mas_fit_is_descending(self) -> None:
        ranked = rank_by_mas_fit()
        scores = [example.mas_fit_score for example in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_top_summary_is_compact(self) -> None:
        summary = summarize_top_examples(limit=3)
        self.assertEqual(len(summary), 3)
        self.assertTrue({"company", "mas_fit_score", "sector", "candidate_agents"}.issubset(summary[0]))


if __name__ == "__main__":
    unittest.main()
