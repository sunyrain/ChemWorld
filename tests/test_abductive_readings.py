from scripts.summarize_abductive_readings import verify_anchor


def test_later_statement_cannot_be_cited_as_earlier_note_or_cursor():
    session = {
        "versions": [
            {"revision": 1, "public_cursor": 0, "text": "Two explanations remain."},
            {
                "revision": 2,
                "public_cursor": 12,
                "text": "The new result excludes one explanation.",
            },
        ]
    }
    anchor = {
        "stage": "notebook",
        "revision": 1,
        "quote": "The new result excludes one explanation.",
        "public_cursor": 0,
    }
    assert verify_anchor(anchor, session) == "quote_not_in_specified_revision"
    anchor["revision"] = 2
    assert verify_anchor(anchor, session) == "incorrect_public_cursor"
    anchor["public_cursor"] = 12
    assert verify_anchor(anchor, session) is None


def test_post_query_explanation_is_not_source_or_prequery_evidence():
    session = {
        "posttests": {
            "K1": {"payload": {"report": "No path contrast was tested."}},
            "K2": {"payload": {"report": "A future test could change the addition path."}},
        }
    }
    anchor = {"stage": "K1", "quote": "A future test could change the addition path."}
    assert verify_anchor(anchor, session) == "quote_not_in_specified_stage_or_query"
    anchor["stage"] = "K2"
    assert verify_anchor(anchor, session) is None
