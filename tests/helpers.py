def assert_exc_info_msg(exc_info, expected_msg):
    # LHS and RHS intentionally placed so diffs look correct.
    assert expected_msg == str(exc_info.value)
