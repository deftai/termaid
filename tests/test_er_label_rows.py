"""An ER relationship's label keeps its own row between the two cardinalities."""
from termaid import render


def _rows(source, **options):
    return [row.strip() for row in render(source, **options).splitlines()]


def test_tight_gap_keeps_label_off_the_cardinality_row():
    source = "erDiagram\n  SESSION ||--o{ MESSAGE : holds"
    rows = _rows(source, padding_x=2, padding_y=0, gap=2)
    assert "│1" in rows and "│ holds" in rows and "│0..*" in rows
    assert not any("1holds" in row for row in rows)
    assert rows.index("│1") < rows.index("│ holds") < rows.index("│0..*")


def test_default_gap_is_unchanged():
    source = "erDiagram\n  SESSION ||--o{ MESSAGE : holds"
    rows = _rows(source)
    assert rows.index("│1") < rows.index("│ holds") < rows.index("│0..*")


def test_unlabelled_relationships_keep_the_tight_gap():
    tight = render("erDiagram\n  A ||--o{ B : x", padding_y=0, gap=2).splitlines()
    unlabelled = render('erDiagram\n  A ||--o{ B : ""', padding_y=0, gap=2).splitlines()
    assert len(unlabelled) == len(tight) - 1  # one row fewer: no label row needed
