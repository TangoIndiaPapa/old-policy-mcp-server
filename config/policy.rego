package policy

default allow = false

deny_phrases := [
    "where is waldo",
    "high frequency trading",
    "hft algorithm",
    "two sum",
    "brute force",
    "anonymous function",
    "monkey patch",
    "suck",
    "idiot",
    "stupid",
    "hate you",
    "shut up",
    "dumb",
    "moron",
    "loser",
    "fool",
    "bastard",
    "jerk",
    "screw you",
    "worthless",
    "useless"
]

# Allow Carmen Sandiego queries
allow if {
    contains_lower(input.action, "carmen sandiego")
}

# Block if any deny phrase is present
allow if {
    not any_deny_phrase_present
}

any_deny_phrase_present if {
    phrase := deny_phrases[_]
    contains_lower(input.action, phrase)
}

# Helper function for case-insensitive substring
contains_lower(str, substr) if {
    lower(str) != null
    lower(substr) != null
    contains(lower(str), lower(substr))
}
